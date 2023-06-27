# Script to quickly look at a RAW MapIR image

from MapIR import MapIR_RAW as mraw

def main():
    print('File Process: ')
    directory = input()
    image = mraw(directory)
    image.display(hist=False)

if __name__ == '__main__':
    main()