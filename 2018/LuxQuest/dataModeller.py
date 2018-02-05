from mcpi import minecraft
from mcpi import block
import csv
from time import sleep
import pandas as pd
import math
from geopy.geocoders import Nominatim
import pygame

# Constant values
maxStackHeight = 120
maxRowLength = 120
fieldnames = ['time', 'lat', 'long', 'photo', 'lux'] # Same fields we wrote to the file
resultsDirectory = '/home/pi/luxquestdata/'
geolocator = Nominatim()
        
# Creates our minecraft objects and displays start message
# Returns our initialized minecraft
def initMineCraft():
    mc = minecraft.Minecraft.create()
    ## clear all blocks down to lowest level
    mc.setBlocks(-128,-64,-128,128,64,128,block.AIR.id)
    ## set bottom yer to build blocks on
    mc.setBlocks(-128,-64,-128,128,-64,128,block.SANDSTONE.id)
    ## move player to corner to start
    mc.player.setPos(-126, -62, -126)
    mc.postToChat("Reset world for Lux Quest!")
    return mc

# Based on the lux value, we want to display blocks as different types
# Returns integer representing block to use
def blockToUse(lux):
    blockToPlace = 1
    if 0 <= lux <= 10:
        blockToPlace = block.BRICK_BLOCK.id
    elif 11 <= lux <= 20:
        blockToPlace = block.IRON_BLOCK.id
    elif 21 <= lux <= 30:
        blockToPlace = block.GOLD_BLOCK.id
    elif 31 <= lux <= 40:
        blockToPlace = block.LAPIS_LAZULI_BLOCK.id
    elif 41 <= lux <= 50:
        blockToPlace = block.DIAMOND_BLOCK.id
    elif 51 <= lux <= 60:
        blockToPlace = block.MELON.id
    elif 61 <= lux <= 70:
        blockToPlace = block.GLOWSTONE_BLOCK.id
    elif 71 <= lux <= 80:
        blockToPlace = block.CLAY.id
    elif 81 <= lux <= 90:
        blockToPlace = block.OBSIDIAN.id
    elif 91 <= lux <= 100:
        blockToPlace = block.GLOWING_OBSIDIAN.id
    elif 101 <= lux <= 110:
        blockToPlace = block.GLASS_PANE.id
    else:
        blockToPlace = block.SNOW_BLOCK.id
    return blockToPlace

# Creates our results reader and skips the headers from the file
# Returns our initialized reader
def initCsvReader(csvfile):
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)
    next(reader) # this lets us skip the header row
    return reader

# Creates our results reader and skips the headers from the file
# Returns our initialized reader
def initPandas(csvfile):
    df = pd.read_csv(resultsDirectory + 'results.csv')
    return df

def getLocString(lat, long):
    location = geolocator.reverse((lat, long))
    if location.address is None:
        return "Not over a known location"
    else:
        return location.address

# Use PyGame top display the image
def displayImage(imageLocation, caption):
    img = pygame.image.load(imageLocation)
    pygame.display.set_caption(caption)
    screen = pygame.display.set_mode((640,480))
    screen.blit(img, (0,0))
    pygame.display.flip()
    
# Main block of code that runs entire program
def main():
    try:
        mc = initMineCraft()
    except ConnectionRefusedError:
        print("Issue connecting to Minecraft! Make sure Minecraft has started!")
    else:
        pygame.init()
        x, y, z = mc.player.getPos()            
        with open(resultsDirectory + 'results.csv') as csvfile:
            reader = initCsvReader(csvfile)
            df = initPandas(csvfile)
            maxValue = df.ix[df.lux.idxmax(), 'lux']
            maxLoc = getLocString(df.ix[df.lux.idxmax(), 'lat'], df.ix[df.lux.idxmax(), 'long'])
            scale = math.ceil(maxValue / maxStackHeight)
            minValue = df.ix[df.lux.idxmin(), 'lux']
            minLoc = getLocString(df.ix[df.lux.idxmin(), 'lat'], df.ix[df.lux.idxmin(), 'long'])
            print("To fit all results, we'll use a scale of " + str(scale))
            print("Max brightness = " + str(maxValue))
            print("Min brightness = " + str(minValue))
            print("Average brightness = " + str(df['lux'].mean()))
            print("Max brightness recorded at: " + maxLoc)
            print("Min brightness recorded at: " + minLoc)
            for row in reader:
                lux = int(float(row['lux'])) # here we are just interested in the lux column
                mc.postToChat('Lux value: ' + str(lux))
                mc.setBlocks(x+1, y+1, z+1, x+1, y+(lux/scale), z+1, blockToUse(lux/scale))
                x += 1
                if x >= maxRowLength: # If we get to the end of the world jump
                    x = -126          # back to the other edge and shift over 
                    z += 5            # a few blocks before continuing
            displayImage(df.ix[df.lux.idxmax(), 'photo'], "Brightest Image")
            sleep(10)
            pygame.quit()

# Run our awesome code!
main()
