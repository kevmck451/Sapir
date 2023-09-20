# Main Processing for MapIR Data start to finish

import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')

from MapIR.mapir import MapIR
from pathlib import Path
from process import process_single
from Data_Paths.data_filepaths import *

# Rename image files to their last digits
## FIX ME: #9630 +?????
def rename_files(directory_arg):
    directory = Path(directory_arg)

    # Rename all files in base directory for easier processing
    for raw_file in directory.iterdir():
        if raw_file.suffix in ['.JPG', '.RAW']:
            # Split the filename by underscores
            split_stem = raw_file.stem.split('_')
            # Get the last segment after the last underscore
            new_name = split_stem[-1] + raw_file.suffix
            # Create the full new file path
            new_file_path = directory / new_name

            if new_file_path.exists():
                new_name = '9' + split_stem[-1] + raw_file.suffix
                # Create the full new file path
                new_file_path = directory / new_name

            # Rename the file
            raw_file.rename(new_file_path)

# If directory does exist, make it
def make_directory(directory_arg):
    directory = Path(directory_arg)
    # if _processed folder doenst exist, make it
    if not directory.exists():
        directory.mkdir()

# Function for processing a dataset that's been set up
def process_directory(base_directory):
    bd = Path(base_directory)

    # Create a new directory to contain processed files if it doesn't exist
    processed_directory = bd / '_processed'
    raw_directory = bd / 'raw'

    # Only first time dataset is processed
    rename_files(raw_directory)

    # Needed for Exporting Files
    make_directory(processed_directory)

    # Process Image
    for file in raw_directory.iterdir():
        if file.suffix == '.RAW':
            process_single(file, processed_directory)


if __name__ == '__main__':

    process_directory(active_dataset)

