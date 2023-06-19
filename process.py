# Processing for MapIR Data
# Output should be files ready to be georectified for further analysis

'''
To Process a Directory it must contain:
    - a folder named 'raw' with the .RAW and .JPG files in it
    - .raw file of reflectance target named ref_tar.RAW

    Base Directory:
        - raw
        - ref_tar.RAW

    Once process runs:
    - files in the raw folder will be renamed for easier processing
    - files will be unpacked, corrected, and calibrated
    - processed files will be saved in _processed folder in directory
    - processed files will contain a geo.txt used for georectification

'''


from MapIR_RAW import MapIR_RAW
from pathlib import Path
import os


def main(base_directory):
    bd = Path(base_directory)

    # Create a new directory to contain processed files if doesnt exist
    processed_directory = base_directory + '/_processed'

    raw_directory = base_directory + '/raw'

    # Rename all files in base directory for easier processing
    for filename in os.listdir(raw_directory):
        if filename.endswith('.JPG') or filename.endswith('.RAW'):
            # Get the file extension (suffix)
            suffix = os.path.splitext(filename)[1]

            # Get the last 3 characters of the filename, excluding the suffix
            new_name = filename[-len(suffix) - 3:-len(suffix)] + suffix

            # Create the full old and new file paths
            old_file_path = os.path.join(raw_directory, filename)
            new_file_path = os.path.join(raw_directory, new_name)

            # Rename the file
            os.rename(old_file_path, new_file_path)

    pd = Path(processed_directory)
    if not pd.exists():
        pd.mkdir()


    for file in bd.iterdir():
        p = f'{processed_directory}/{file.stem}'
        p = Path(p)
        if file.suffix == '.RAW':
            if not p.exists():
                image = MapIR_RAW(file)
                image.extract_GPS('tiff')
                image.export_tiff()
                # image.export_png()
                # image.export_jpg()


if __name__ == '__main__':
    base_directory = '../Data/MapIR/AC Summer 23/Wheat Field/6-8'
    main(base_directory)