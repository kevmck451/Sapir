# Script to quickly look at a RAW MapIR image

from MapIR import MapIR_RAW as mraw
import os

# directory = '/Volumes/KM1TBS/Orlando Files/MapIR/Decoy Middle Select'
directory = 'Datasets/'

def main():

    print('Processing...')
    # directory = input()

    file: str

    for filename in os.listdir(directory):
        if filename.endswith(".RAW"):  # you can use this to filter the files
            file = os.path.join(directory, filename)
            image = mraw(file)
            image.export_all()
        else:
            continue

if __name__ == '__main__':
    main()