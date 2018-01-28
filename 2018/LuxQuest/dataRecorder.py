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
    sense.show_message ("Hello ISS from Team LUX Quest")
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
    startTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    print("Time this program started at {0}".format(startTime))
    senseHat = initSenseHat()
    iss = initIss()
    cam = initCamera()
    initResultsDirectory()

    with open(resultsDirectory + 'results.csv', 'w') as csvfile: # open the file for writing
        writer = initCsvWriter(csvfile)

        while True: # Keep looping as ESA will stop program when times runs out
            iss.compute() # Get latest position of ISS

            print("Lat:\t%s\tLong:\t%s\t%s" % (iss.sublat, iss.sublong, isNight(iss)))

            timeNow = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

            print("Time now is {0}".format(timeNow))

            cam.annotate_text = timeNow # Put time on photo capture

            photoName = resultsDirectory + timeNow + "Team LuxQuest.jpg"

            cam.capture(photoName) # Take photo of Earth
            image = Image.open(photoName).convert('L') # convert image to monochrome
            lux = ImageStat.Stat(image).mean[0] # calculate mean brightness/lux of image
            print("Brighness of image: ", lux)

            writer.writerow({'time': timeNow, 'lat': iss.sublat, 'long': iss.sublat, 'photo': '/home/pi/luxquestdata/' + photoName, 'lux': lux}) # write data to the row. see use of random integers

            time.sleep(1)

            # Things to do:
            # 1) Only take photo when it is dark
            # 2) Update photo with lux value if needed
            # 3) Display lux value on SenseHat
            # 4) Capture any exceptions (places where code goes wrong) so program doesn't crash
            # 5) Figure out a good delay between photos
            # 6) Relax and enjoy finished program
            
# Run our awesome code!
main()
