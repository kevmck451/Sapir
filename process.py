# Processing for MapIR Data

from raw import MapIR_RAW
from pathlib import Path

def process(base_directory):
    bd = Path(base_directory)

    # Create a new directory to contain processed files if it doesn't exist
    processed_directory = bd / '_processed'
    raw_directory = bd / 'raw'

    # Rename all files in base directory for easier processing
    for raw_file in raw_directory.iterdir():
        if raw_file.suffix in ['.JPG', '.RAW']:
            # Get the last 3 characters of the filename, excluding the suffix
            new_name = raw_file.stem[-3:] + raw_file.suffix
            # Create the full new file path
            new_file_path = raw_directory / new_name
            # Rename the file
            raw_file.rename(new_file_path)

    # if _processed folder doenst exist, make it
    if not processed_directory.exists():
        processed_directory.mkdir()

    # Process Image
    for file in raw_directory.iterdir():
        if file.suffix == '.RAW':
            image = MapIR_RAW(file)
            image.extract_GPS('tiff')
            image.export_tiff()


if __name__ == '__main__':
    base_directory = '../Data/MapIR/AZ 22'
    process(base_directory)