# Duplicate Finder

Following guide on https://realpython.com/fingerprinting-images-for-near-duplicate-detection/

Modified to suit my needs.

Wanted a fast solution for finding duplicate pictures in a folder.

## How it works

Creates a hash for all of the pictures in the folder.
Compares the hashes looking for duplicates.
Creats a list of the duplicate pictures.
Finds the largest image (assumed best quality)
Moves the duplicate pictures to a sub folder 'Duplicates'
Creats a database of the hashes and a txt file with the list of files.

## Use
python3 dupeFinder.py -d /Path/To/Pictures/

## To do:
- Split into a more stand alone application
- Make database in directory for images
- Error handling
- Other image file types