# Main Processing for MapIR Data start to finish

from MapIR.mapir import MapIR
from pathlib import Path

def process(base_directory):
    bd = Path(base_directory)

    # Create a new directory to contain processed files if it doesn't exist
    processed_directory = bd / '_processed'
    raw_directory = bd / 'raw'

    # Rename all files in base directory for easier processing
    for raw_file in raw_directory.iterdir():
        if raw_file.suffix in ['.JPG', '.RAW']:
            # Split the filename by underscores
            split_stem = raw_file.stem.split('_')
            # Get the last segment after the last underscore
            new_name = split_stem[-1] + raw_file.suffix
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
            # Create MapIR Object
            image = MapIR(file)
            # Band_Correction

            # Radiance_Calibration

            # Reflectance Calibration

            # Georectification
            # image.extract_GPS('tiff')
            # image.export_tiff()
            # Analysis


if __name__ == '__main__':
    # base_directory = '../Data/MapIR/AC Summer 23/Wheat Field/6-20'
    # base_directory = '../Data/MapIR/AC Summer 23/Main Sub Field/6-20'
    base_directory = '../Data/MapIR/Test'

    process(base_directory)