import sys
import os
import pprint # for console printing
import yaml

from workbookbuilder import WorkbookBuilder
from lilypondfilebuilder import LilypondFileBuilder
from instrumentdata import InstrumentData

def cleanFilename(filename):
    forbiddenChars = ["/", "\\", "?", "%", "*", ":", "\'", "\"", "|", ">", "<", "."]

    cleanName = filename.lower()
    cleanName = cleanName.replace(" ", "-")

    for fChar in forbiddenChars:
        cleanName = cleanName.replace(fChar, "")

    return cleanName


pPrinter = pprint.PrettyPrinter(indent=2, width=120)
workbookBuilder = WorkbookBuilder()
lilypondFileBuilder = LilypondFileBuilder()

print " _____ _         _     _____         "
print "|   __| |_ _ _ _| |___|   __|___ ___ "
print "|   __|  _| | | . | -_|  |  | -_|   |"
print "|_____|_| |___|___|___|_____|___|_|_|\n"

# Determine if we're using Test mode
testMode = False
if len(sys.argv) > 0:
    for arg in sys.argv:
        if(arg.lower() == "test"):
            print "Creating documents in Test mode..."
            testMode = True
            break

if testMode == False:
    print "Creating documents in Normal mode..."


# Loading configuration file
fileDir = os.path.dirname(os.path.realpath(__file__))
cfgFilePath = os.path.join(fileDir, 'config.yaml')

try:
    stream = file(cfgFilePath, 'r')
    yamlData = yaml.load(stream)
    if testMode:
        print "\nCONFIGURATION SETTINGS:"
        pPrinter.pprint(yamlData)
        print ""
except:
    print "YAML configuration failed to load!"
    raise


# Define the list of keys
majorKeyListTest = ['A', 'Eb']
minorKeyListTest = ['F#', 'C',]


# Create the etudes!
for rawInstrument in yamlData['instruments']:
    instrument = InstrumentData(rawInstrument['name'], rawInstrument['clef'], rawInstrument['lowerLimit'], rawInstrument['upperLimit'])

    # Set up the key list
    majorKeyListFull = rawInstrument['majorKeys'].split(' ')
    minorKeyListFull = rawInstrument['minorKeys'].split(' ')
    majKeyList = majorKeyListTest if testMode else majorKeyListFull
    minKeyList = minorKeyListTest if testMode else minorKeyListFull

    # Set up file data
    lilypondFileBuilder.filename = cleanFilename("music-workbook-for-" + instrument.name)
    lilypondFileBuilder.instrument = instrument.name
    lilypondFileBuilder.clef = instrument.clef
    workbookBuilder.lowerLimit = instrument.lowerLimit
    workbookBuilder.upperLimit = instrument.upperLimit

    lilypondFileBuilder.forceAccidentals = rawInstrument["forceAccidentals"]
    lilypondFileBuilder.showSolfege = rawInstrument["showSolfege"]

    # For each key, create the scale and arpeggio exercises
    for majorKey in majKeyList:
        keyData = workbookBuilder.buildKeyData(majorKey, "major")
        lilypondFileBuilder.addLilypondKeyBlock(keyData)

    for minorKey in minKeyList:
        keyData = workbookBuilder.buildKeyData(minorKey, "minor")
        lilypondFileBuilder.addLilypondKeyBlock(keyData)

    # Write the results to files, using Lilypond
    print "Writing file..."
    lilypondFileBuilder.writeLilypondFile()

lilypondFileBuilder.buildEtudeDocuments()
