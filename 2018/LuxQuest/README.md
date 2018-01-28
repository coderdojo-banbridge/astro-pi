## Lux Quest

### Idea

Light pollution Detector to determine areas of high light pollution. 
It will use the Pi NoIR camera to capture images when ISS is over land in darkness. 
It will post process the images and determine biggest offenders of light pollution. 
The results may be displayed in a minecraft model and also displayed on the Sense Hat LED display.

### Code

The code is broken into two parts. One will run in the ISS and take the measurements. 
The other will run on earth after the data is returned and model the findings.

Both projects use the same folder structure & files for the results:

`/home/pi/luxquestdata/results.csv`

And it also expects the photos to be stored in the same directory:

`/home/pi/luxquestdata/`

**Note:** One improvement here could be to pass this location in as an argument to the programs below

#### Requirements

The following commands need to be run in order to have code run as expected:

`pip install pyephem`
`sudo apt-get install libjpeg-dev`
`pip install pillow`

#### dataRecorder.py

This is the code that will run in space. To run it do the following at the command line:

`python dataRecorder.py`

#### dataModeller.py

This is the code that will when the results are returned. To run it enter the following at the command line:

`python dataModeller.py`