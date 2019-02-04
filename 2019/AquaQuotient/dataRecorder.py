import logging
import logzero
from logzero import logger
from sense_hat import SenseHat
import ephem
from picamera import PiCamera
import datetime
import time
from time import sleep
import random
import math
import os

# Constant values
sun = ephem.Sun()
twilight = math.radians(-6)
dir_path = os.path.dirname(os.path.realpath(__file__))

# define some colours - keep brightness low

g = [0,50,0]
o = [0,0,0]

# define a simple image
img1 = [
    g,g,g,g,g,g,g,g,
    o,g,o,o,o,o,g,o,
    o,o,g,o,o,g,o,o,
    o,o,o,g,g,o,o,o,
    o,o,o,g,g,o,o,o,
    o,o,g,g,g,g,o,o,
    o,g,g,g,g,g,g,o,
    g,g,g,g,g,g,g,g,
]

# Set a logfile name
logzero.logfile(dir_path+"/data01.csv")

# Set a custom formatter
formatter = logging.Formatter('%(asctime)-15s, %(message)s');
logzero.formatter(formatter)

 # Connect to the Sense Hat
def initSenseHat():
    sense = SenseHat()
    return sense

# Latest TLE data for ISS location
def initIss():
    name ="ISS (ZARYA)"
    l1 = "1 25544U 98067A   19033.27351531  .00001422  00000-0  29623-4 0  9998"
    l2 = "2 25544  51.6433 312.1797 0005043 343.6440 154.8135 15.53218636154298"
    iss = ephem.readtle(name, l1, l2)
    return iss

# Set up camera
def initCamera(): 
    cam = PiCamera()
    cam.resolution = (1296,972)
    return cam

# define a function to update the LED matrix
def active_status(senseHat):
    """
    A function to update the LED matrix regularly
    to show that the experiment is progressing
    """
    # a list with all possible rotation values
    orientation = [0,90,270,180]
    # pick one at random
    rot = random.choice(orientation)
    # set the rotation
    senseHat.set_rotation(rot)
    senseHat.set_pixels(img1)

def isNight(iss):
    observer = ephem.Observer()
    observer.lat = iss.sublat
    observer.long = iss.sublong
    observer.elevation = 0
    sun.compute(observer)
    sun_angle = math.degrees(sun.alt)
    day_or_night = True if sun_angle < twilight else False
    return day_or_night

def main():
    senseHat = initSenseHat()
    iss = initIss()
    cam = initCamera()
    cam.start_preview(fullscreen=False)
    senseHat.set_pixels(img1)
    time.sleep(2)
    recordingLoopDelay = 3
    photoCounter = 1
    while True: # Keep looping as ESA will stop program when times runs out
        iss.compute() # Get latest position of ISS
        if isNight(iss):
            senseHat.show_message ("Skipping at night", text_colour=g, scroll_speed=0.05)
            time.sleep(5)
        else:
            logger.info("%s,%s,%s", photoCounter, math.degrees(iss.sublat), math.degrees(iss.sublong) )
            # use zfill to pad the integer value used in filename to 3 digits (e.g. 001, 002...)
            cam.capture(dir_path+"/photo_"+ str(photoCounter).zfill(3)+".jpg")
            photoCounter+=1
        time.sleep(recordingLoopDelay)
        active_status(senseHat)
        time.sleep(recordingLoopDelay)
        
try:
    main()
except Exception as ex:
    print("Something bad happened! Exception as follows:")
    print(ex)
except KeyboardInterrupt:
    print("User requested program end. Thank you for running our code!")
