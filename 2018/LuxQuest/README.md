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

The following commands need to be run in order to have code run the data recorder as expected in **space**:

`pip install pyephem`

`sudo apt-get install libjpeg-dev`

`pip install pillow`

And for the modeller:

`pip install geopy`

`pip install pandas`

#### dataRecorder.py

This is the code that will run in space. To run it do the following at the command line:

`python dataRecorder.py`

#### dataModeller.py

This is the code that will when the results are returned. To run it enter the following at the command line:

`python dataModeller.py`

#### config.py

This config class is common to both recorder and modeller and allows us to change various settings, e.g. where results are recorded/read & how long we pause between each photo. It does not needed to be run, merely be in the same directory as our recorder & modeller code. 

## Update: Viewing results

The results were sent through from the team at **Astro Pi** on the 8th of May. We'll demo the solution to the dojo at the session on the 19th but the following instructions show how anyone can access the results and run them on their own Pi!

### Fetching the results

We've stored our entire Astro-Pi project including the results up on Github so these steps will detail 
how to pull them down onto your Pi.

First, create a folder to work with the code:

```
mkdir results
```

Next, pull the code down from Github:

```
git clone https://github.com/coderdojo-banbridge/astro-pi.git
```

This will create a folder called `astro-pi` and you'll see it mirrors the structure of https://github.com/coderdojo-banbridge/astro-pi

### Looking at the results

The results are stored under `results/astro-pi/2018/LuxQuest/luxquestdata/3435_Lux Quest/61` and if you do a quick ` ls *.jpg | wc -l` you'll see that 1860 images were captured. 

There is also a `Lux Quest_console.log` which captured any output (print statements etc) from the program.

And finally there is the `Lux Quest_results.csv` file which recorded all of our results!

Let's take a look at one of those rows in the csv:

time	| lat	| long	| photo	| lux
------|-----|-------|-------|----
2018-04-28-00-34-37	| -44.8390546746369	| -83.8707068565246	| /home/pi/Transfer/3435_Lux Quest/61/2018-04-28-00-34-37LuxQuest.jpg	| 5.35385091145833

So, all the data we expected, i.e. when photo was taken, where it was taken (lat & long), the photo that was taken and finally the measure of brightness of the image.

If you take one more look at the the photo entry, you can see if has stored the photo in a different location, `/home/pi/Transfer/3435_Lux Quest/61/2018-04-28-00-34-37LuxQuest.jpg` to where we've pulled out code from github. We've a few options here:
* Using LibreOffice, open the csv file and do a find and replace of `/Transfer/` with `/results/astro-pi/2018/LuxQuest/luxquestdata/`
* Copy your data from `results/astro-pi/2018/LuxQuest/luxquestdata` to `Transfer`
* Or simply create a link from `Transfer` to `results/astro-pi/2018/LuxQuest/luxquestdata`

The last option is what you will get if you do the following:

```
cd /home/pi
ln -s ~/results/astro-pi/2018/LuxQuest/luxquestdata Transfer
```

We want to rename the results file from `Lux Quest_results.csv` to `results.csv`

```
mv /home/pi/Transfer/3435_Lux\ Quest/61/Lux Quest_results.csv /home/pi/Transfer/3435_Lux\ Quest/61/results.csv 
```

Then finally update the config.py in `/home/pi/results/astro-pi/2018/LuxQuest` to point to where the results.csv file is. You can use whatever your favourite python editor is for this and change the following line:

```
    resultsDirectory = '/home/pi/luxquestdata/'
```

to: 

```
    resultsDirectory = '/home/pi/Transfer/3435_Lux Quest/61/'
```

### Run the Modeller and View results in Minecraft

Remember, you need to have Minecraft running, so start that first of all. Also, you need to have installed all the required packages and libraries too.

Then run our programme. We're going to assume we're in the right directory, e.g. `/home/pi/results/astro-pi/2018/LuxQuest`

```
python dataModeller.py

```
