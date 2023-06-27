# Script to band_correction RAW files, extract GPS data from jpg and export in format that can be georectified

from MapIR import MapIR_RAW
from pathlib import Path
import os


def main():
    base_directory = '../Data/MapIR/AC Summer 23/Wheat Field/6-8'

    # Create a new directory to contain processed files if doesnt exist
    processed_directory = base_directory + '/_processed'

    bd = Path(base_directory)

    # Rename all files in base directory for easier processing
    for filename in os.listdir(base_directory):
        if filename.endswith('.JPG') or filename.endswith('.RAW'):
            # Get the file extension (suffix)
            suffix = os.path.splitext(filename)[1]

            # Get the last 3 characters of the filename, excluding the suffix
            new_name = filename[-len(suffix) - 3:-len(suffix)] + suffix

            # Create the full old and new file paths
            old_file_path = os.path.join(base_directory, filename)
            new_file_path = os.path.join(base_directory, new_name)

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
                image = MapIR_RAW(file, stats=False)
                image.extract_GPS('jpg')
                # image.export_tiff()
                # image.export_png()
                image.export_1()








if __name__ == '__main__':
    main()

    # file = '../Data/AC Summer 23/Wheat Field/6-8/503.RAW'
    # image = MapIR_RAW(file, stats=False)
    # image.extract_GPS()
    # image.NDVI()
    # print(image.data)
    # print(image.data.dtype)