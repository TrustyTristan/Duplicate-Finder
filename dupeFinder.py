# Import
from PIL import Image
import imagehash
import argparse
import shelve
import operator
import os
from pathlib import Path

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "path to input dataset of images")
args = vars(ap.parse_args())

# Variables
workingDir = Path(args['dataset'])
setName = os.path.basename(workingDir)
fileTypes = ('.jpg', '.png', '.jpeg')
duplicateDictionary = {}
analysedTotal = 0
duplicateList = []
keepList = []

# Change Working Directory
os.chdir(workingDir)

print('Analysing: ', workingDir)

# open the shelve database
db = shelve.open(f'{setName}.shelve', writeback = True)


for filePath in os.scandir(workingDir):
	analysedTotal += 1
	filePath = Path(filePath)
	fileName = Path(filePath.name)

	# If file is not a file but a directory or a system file,
	# ignore and continue
	if filePath.is_dir() or str(fileName).startswith("."):
		continue

	fileExt = fileName.suffix.lower()

	if fileExt in fileTypes:

		imageFile = Image.open(filePath)

		# Create hash for image
		imgHash = str(imagehash.dhash(imageFile))
		print(f'Made hash {imgHash} for {fileName}')

		# Write to database
		db[imgHash] = db.get(imgHash, []) + [filePath]


# Find duplicates in database
for filePath in db:
	if len(db[filePath]) > 1:
		for image in db[filePath]:
			imageDictionary = {}
			# get the hight and width of each picture
			duplicateList.append(image)
			imageFile = Image.open(image)
			h, w = imageFile.size
			# store hight and width of picture to full filepath
			imageDictionary[image] = h * w
			duplicateDictionary.setdefault(filePath,{})
			# add to key value of hash
			duplicateDictionary[filePath].update(imageDictionary)

# Close the shelf database
db.close()


print('\nMatching hashes\n')


for picHash, fileName in duplicateDictionary.items():
	print(f'{picHash} has {str(len(fileName))} matches')
	bestFile = max(fileName.items(), key=operator.itemgetter(1))[0]
	keepList.append(bestFile)


def Difference(li1, li2):
	return (list(set(li1) - set(li2)))


removeList = Difference(duplicateList,keepList)
print(f'\nAnalysed {analysedTotal} images.\nFound {analysedTotal-len(removeList)} unique images.\nFound {len(keepList)} images with duplicates.\nMoving {len(removeList)} duplicate images.\n')

def MoveDuplicates(list):
	duplicateDir = Path(os.path.join(workingDir,'Duplicates'))
	duplicateDir.mkdir(exist_ok=True)
	removedText = open('DuplicateList.txt','a')
	for each in list:
		fileName = os.path.basename(each)
		filePath = os.path.join(workingDir,fileName)
		newPath = os.path.join(duplicateDir,fileName)
		print(f'Moving duplicate to {newPath}')
		os.rename(filePath, newPath)
		removedText.write(f'{each}\n')
	removedText.close()


MoveDuplicates(removeList)
