import sys
import xml.etree.ElementTree as ET
from configparser import ConfigParser
from os import path
from random import randint
from PIL import Image, ImageDraw, ImageColor

# CONFIG DATA
configur = ConfigParser()
configur.read('config.ini')

class col:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
def message(msg):
    print("• " + str(msg))
def failed(msg):
    print(col.FAIL + "✗ " + str(msg) + col.ENDC)
    exit()
def success(msg):
    print(col.OKGREEN + "✓ " + str(msg) + col.ENDC)
def getColorRandom():
    randHex = hex(randint(60, 220))[2:]
    return str(randHex).zfill(2)

metaName = configur.get('meta', 'name')
metaVersion = configur.get('meta', 'version')
metaAuthor = configur.get('meta', 'author')
metaLink = configur.get('meta', 'link')

arguments = len(sys.argv) - 1
amount = 1;
if (arguments < amount):
    failed("Not enough arguments! >:(")
elif (arguments > amount):
    failed("Too much arguments... :|")
folder = configur.get('options', 'folder') + '/'
file = sys.argv[1]
file = folder + file

xmlTree = ET.parse(file)
xmlRoot = xmlTree.getroot()
sqrRange = []
for tag in xmlRoot:
    sqrPath = tag.attrib
    sqrRange += [[(int(sqrPath.get('x')), int(sqrPath.get('y'))), (int(sqrPath.get('x')) + int(sqrPath.get('width')), int(sqrPath.get('y')) + int(sqrPath.get('height')))]]

imgName = folder + xmlRoot.attrib.get('imagePath')
if (path.exists(imgName)):
    imgData = Image.open(imgName)
    imgSize = imgData.size
    imgMode = "RGBA"
    imgFill = 0
else:
    failed("No image file with XML was found.")

with Image.new(imgMode, imgSize, imgFill) as img:
    for sqr in sqrRange:
        sqrNow = [sqr[0], (sqr[1][0]-1, sqr[1][1]-1)]
        draw = ImageDraw.Draw(img)
        draw.rectangle(sqrNow, "#" + getColorRandom() + getColorRandom() + getColorRandom())

    img.save(imgName.replace('.png', '-map.png'), "PNG")
    success("File saved as " + imgName.replace('.png', '-map.png') + ".\n")
    message("Credits not required, but greatly appriciated!")
    message(metaName+" "+metaVersion+" by "+metaAuthor+"\n")
    message(metaLink)