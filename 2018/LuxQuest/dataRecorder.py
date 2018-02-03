# Team Lux Quest
import ephem
import math
from sense_hat import SenseHat
import time
import picamera
import io
from PIL import Image
from PIL import ImageStat
import csv
import datetime as dt
import os

# Constant values
sun = ephem.Sun()
twilight = math.radians(-6)
fieldnames = ['time', 'lat', 'long', 'photo', 'lux'] # the different elements we store in each row
resultsDirectory = '/home/pi/luxquestdata/'

# Creates our senseHat object and displays start message
# Returns our initialized senseHat
def initSenseHat():
    sense = SenseHat ()
    sense.show_message ("Hello ISS from Team LUX Quest", 0.05)
    sense.show_message ("Our aim is to measure light pollution", 0.05)
    return sense

# Creates our ISS object using Two Line Element Data
# Returns our initialized iss
def initIss():
    name = "ISS (ZARYA)"
    line1 = "1 25544U 98067A   17332.28575632  .00003326  00000-0  57234-4 0  9993"
    line2 = "2 25544  51.6431 300.2614 0004099 158.9129 343.4648 15.54248554 87274"
    iss = ephem.readtle(name, line1, line2)
    return iss

# Creates our camera object with set of default values for annotation
# Returns our initialized camera
def initCamera():
    camera = picamera.PiCamera()
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text_size = 50
    ## Code below is to ensure we get consistent images
    ## as we found during testing that the camera was adjusting
    ## the white balance which meant results were varying for a
    ## stable image
    camera.iso = 800
    camera.resolution = (640, 480)
    camera.framerate = 30
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    g = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = g
    return camera

# Create our results directory if it doesn't exist
def initResultsDirectory():
    if not os.path.exists(resultsDirectory):
        os.makedirs(resultsDirectory)

# Determines if it is nighttime (True) or daytime (False) under the ISS
# Returns a boolean
def isNight(iss):
    observer = ephem.Observer()
    observer.lat = iss.sublat
    observer.long = iss.sublong
    observer.elevation = 0
    sun.compute(observer)
    sun_angle = math.degrees(sun.alt)
    day_or_night = True if sun_angle < twilight else False
    return day_or_night

# Creates our results file and writes out the headers into file
# Returns our initialized writer
def initCsvWriter(csvfile):
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames) # create writer with fields
    writer.writeheader() # write out the fields as headers on the file so itmakes sense to us humans :D
    return writer

# Main block of code that runs entire program
def main():
    senseHat = initSenseHat()
    iss = initIss()
    cam = initCamera()
    initResultsDirectory()
    cam.start_preview(fullscreen=False)
    time.sleep(2)
    with open(resultsDirectory + 'results.csv', 'w') as csvfile: # open the file for writing
        writer = initCsvWriter(csvfile)

        while True: # Keep looping as ESA will stop program when times runs out
            iss.compute() # Get latest position of ISS
            if isNight(iss):
                timeNow = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
                cam.annotate_text = timeNow # Put time on photo capture
                photoName = resultsDirectory + timeNow + "LuxQuest.jpg"
                cam.capture(photoName) # Take photo of Earth
                image = Image.open(photoName).convert('L') # convert image to monochrome
                lux = ImageStat.Stat(image).mean[0] # calculate mean brightness/lux of image
                senseHat.show_message (str(int(lux)), 0.05)
                writer.writerow({'time': timeNow, 'lat': math.degrees(iss.sublat), 'long': math.degrees(iss.sublong), 'photo': '/home/pi/luxquestdata/' + photoName, 'lux': lux})
            else:
                senseHat.show_message ("Daylight", 0.05)
            time.sleep(1)
            
# Run our awesome code!
main()
