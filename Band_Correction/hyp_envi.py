import os
import pathlib
import mmap
import sys
from dataclasses import dataclass
from typing import Tuple, Optional

import numpy as np

# map from ENVI specified byte order codes to array protocol characters
_BYTE_ORDER_CODE2CHAR = {
    0: "<", # little endian
    1: ">", # big endian
}
_BYTE_ORDER_CHAR2CODE = {v: k for k, v in _BYTE_ORDER_CODE2CHAR.items()}

# map from ENVI specified data type codes to array protocol characters
_DATA_TYPE_CODE2CHAR = {
     1: "u1", # unsigned byte
     2: "i2", # signed 16 bit integer
     3: "i4", # signed 32 bit integer
     4: "f4", # 32 bit float
     5: "f8", # 64 bit float
    12: "u2", # unsigned 16 bit integer
    13: "u4", # unsigned 32 bit integer
    14: "i8", # signed 64 bit integer
    15: "u8", # unsigned 64 bit integer
}
_DATA_TYPE_CHAR2CODE = {v: k for k, v in _DATA_TYPE_CODE2CHAR.items()}

def _parse_header_lines(line_list):
    # ENVI files are, more or less, name=value pairs. sometimes the value can be
    # enclosed in {} in which case it is a list and can span multiple lines.
    # sometimes there are nominally name=value pairs inside this "list" but
    # we punt on that for now and make it the application's problem...

    header = {}
    line_num = 0
    while line_num < len(line_list):
        line = line_list[line_num]
        if line.strip() == "":
            line_num += 1
            continue
        try:
            name, value = [v.strip() for v in line.split("=", maxsplit=1)]
        except ValueError:
            # line has no equals, ignore it
            line_num += 1
            continue

        if value.startswith("{"): # the start of a list
            the_list = []
            line_list[line_num] = value[1:] # chop out the opening {
            while line_num < len(line_list):
                line = line_list[line_num]
                line_num += 1
                values = [v.strip() for v in line.split(",")]
                if values[-1].endswith("}"): # last line of the list
                    values[-1] = values[-1][:-1].strip() # chop out the }
                    the_list.extend((v for v in values if v != ""))
                    break
                else:
                    the_list.extend((v for v in values if v != ""))
            else: # did not break -> never saw the end of the list
                raise ValueError("unterminated list")
            header[name] = the_list
        else:
            header[name] = value
            line_num += 1

    return header

def _parse_data_type(byte_order, data_type):
    # turn the data type attribute numbers into a numpy datatype object

    byte_order = int(byte_order)
    bo_char = _BYTE_ORDER_CODE2CHAR.get(byte_order)
    if bo_char is None:
        raise ValueError(f"unknown byte order {byte_order}")

    data_type = int(data_type)
    dt_char = _DATA_TYPE_CODE2CHAR.get(data_type)
    if data_type is None:
        raise ValueError(f"unknown data type {data_type}")

    return np.dtype(bo_char+dt_char)

def _get_interleave_shape(interleave, bands, lines, samples):
    if interleave == "bil":
        return (lines, bands, samples)
    elif interleave == "bip":
        return (lines, samples, bands)
    elif interleave == "bsq":
        return (bands, lines, samples)
    else:
        raise ValueError(f"bad interleave setting {interleave}")

def _parse_header_attrs(header):
    # parse core attributes out of the header (and remove them in the process_single)
    dtype = _parse_data_type(
        header.pop("byte order", 0), # assume little endian by default
        header.pop("data type"))

    def dim(which):
        val = header.pop(which)
        val = int(val)
        if val < 0:
            raise ValueError(f"invalid {which} value {val}")
        return val

    bands = dim("bands")
    lines = dim("lines")
    samples = dim("samples")

    interleave = header.pop("interleave")
    shape = _get_interleave_shape(interleave, bands, lines, samples)

    wavelength = header.pop("wavelength", None)
    if wavelength is not None:
        wavelength = np.array([float(v) for v in wavelength],
                dtype=np.float64)

    return CubeAttributes(
        dtype, bands, lines, samples,
        shape, interleave, wavelength
    )

def _parse_header_fp(fd):
    magic = fd.readline()
    if not magic.strip() == "ENVI":
        raise ValueError("not an ENVI header file")

    try:
        header = _parse_header_lines(list(fd.readlines()))
    except Exception as e:
        raise ValueError("failed to parse header") from e

    try:
        attrs = _parse_header_attrs(header)
    except Exception as e:
        raise ValueError("failed to parse header attributes") from e

    return header, attrs

def _generate_header_lines(header, attrs):
    # generate the header lines from cube attributes

    # get codes for data type and byte order
    code = np.dtype(attrs.dtype).str
    bo_char, dt_char = code[:1], code[1:]
    if bo_char not in "><": # not applicable or native
        bo_char = "<" if sys.byteorder == "little" else ">"

    lines = ["ENVI",
        f"interleave = {attrs.interleave}",
        f"byte order = {_BYTE_ORDER_CHAR2CODE[bo_char]}",
        f"data type = {_DATA_TYPE_CHAR2CODE[dt_char]}",
        f"lines = {attrs.lines}",
        f"samples = {attrs.samples}",
        f"bands = {attrs.bands}",
        f"wavelength = {{{', '.join(str(float(w)) for w in attrs.wavelength)}}}"
    ]
    lines.extend([f"{k} = {str(v)}" for k, v in header.items()])

    return lines

@dataclass(frozen=True)
class CubeAttributes:
    """Core attributes that describe a data cube."""
    dtype: np.dtype
    bands: int
    lines: int
    samples: int

    shape: Tuple[int, int, int]
    interleave: str

    wavelength: Optional[np.ndarray]

class Cube:
    def __init__(self, attrs, header=None, data=None, data_fp=None):
        self._attrs = attrs

        if header is None:
            self.header = {}
        else:
            self.header = header

        self.data = data
        self._data_fp = data_fp

    def __getattr__(self, name):
        return getattr(self._attrs, name)

    @classmethod
    def new(cls, dtype, bands, lines, samples,
            interleave="bsq", wavelength=None):
        attrs = CubeAttributes(
            dtype, bands, lines, samples,
            _get_interleave_shape(interleave, bands, lines, samples),
            interleave, wavelength
        )

        data = np.zeros(attrs.shape, dtype=attrs.dtype)

        return cls(attrs, data=data)

    @classmethod
    def from_path(cls, path):
        path = pathlib.Path(path)
        header_fp = (path.parent/(path.name+".hdr")).open("r")
        data_fp = path.open("rb")

        return cls.from_fp(header_fp, data_fp)

    @classmethod
    def from_fp(cls, header_fp, data_fp):
        try:
            header, attrs = _parse_header_fp(header_fp)
        finally:
            header_fp.close()

        return cls(attrs, header=header, data_fp=data_fp)

    def read(self, as_mmap=False, madvise=None):
        if self.data is not None:
            raise RuntimeError("cube data is already loaded")

        self._as_mmap = as_mmap
        offset = int(self.header.get("header offset", 0))
        if as_mmap:
            dtype, shape = self.dtype, self.shape

            length = dtype.itemsize*shape[0]*shape[1]*shape[2]

            self._mmap = mmap.mmap(self._data_fp.fileno(), length,
                prot=mmap.PROT_READ, offset=0)
            if hasattr(self._mmap, "madvise"):
                if madvise is None:
                    madvise = mmap.MADV_NORMAL
                self._mmap.madvise(madvise)

            data = np.frombuffer(self._mmap, dtype=dtype, offset=offset)
            self.data = data.reshape(shape)
        else:
            self.data = np.empty(self.shape, dtype=self.dtype)
            self._data_fp.seek(offset, os.SEEK_CUR)
            self._data_fp.readinto(self.data)

        return self.data

    def write_fp(self, header_fp=None, data_fp=None):
        if header_fp is not None:
            header_lines = _generate_header_lines(self.header, self._attrs)
            header_fp.write("\n".join(header_lines).encode("ascii"))

        if data_fp is not None:
            if not self.data.flags['C_CONTIGUOUS']:
                data_fp.write(self.data.tobytes('C'))
            else:
                data_fp.write(self.data)

    def close(self):
        self.data = None

        if self._as_mmap:
            self._mmap.close()
            self._mmap = None

        self._data_fp.close()
        self._data_fp = None

    def closest_band(self, wavelength):
        return np.argmin(np.abs(self.wavelength-wavelength))

