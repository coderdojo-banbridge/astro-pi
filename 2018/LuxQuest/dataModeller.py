from mcpi import minecraft
import csv
from time import sleep

# Constant values
tungsten=45
tnt = 7
static_lava = 11
gold_ore = 14
fieldnames = ['time', 'lat', 'long', 'photo', 'lux'] # Same fields we wrote to the file
resultsDirectory = '/home/pi/luxquestdata/'

# Creates our minecraft objects and displays start message
# Returns our initialized minecraft
def initMineCraft():
    mc = minecraft.Minecraft.create()
    mc.postToChat("Hello world")
    return mc

# Based on the lux value, we want to display blocks as different types
# Returns integer representing block to use
def blockToUse(lux):
    blockToPlace = 1
    if lux >= 0 and lux <= 20:
        blockToPlace = tnt
    elif lux >= 21 and lux <= 50:
        blockToPlace = tungsten
    elif lux >= 256:
        blockToPlace = static_lava
    else:
        blockToPlace = gold_ore
    return blockToPlace

# Creates our results reader and skips the headers from the file
# Returns our initialized reader
def initCsvReader(csvfile):
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    next(reader) # this lets us skip the header row
    return reader

# Main block of code that runs entire program
def main():
    mc = initMineCraft()
    x, y, z = mc.player.getPos()
        
    with open(resultsDirectory + 'results.csv') as csvfile:
        
        for row in reader:
            lux = int(float(row['lux'])) # here we are just interested in the lux column
            mc.postToChat('Lux value: ' + str(lux))
            mc.setBlocks(x+1, y+1, z+1, x+1, y+lux, z+1, blockToUse(lux))
            x += 1

            # Things to do:
            # 1) Add exception handling, i.e. what if results file isn't there
            # 2) Determine different block types we want to use
            # 3) Is it better to use players current position or to start somewhere like 0,0,0?
            # 4) Can we do anything extra with the data, e.g. keep track or brightest and darkest places
            #    or look up locations of brightest/darkest. Can we open the picture with brightest and
            #    darkest results?

# Run our awesome code!
main()
