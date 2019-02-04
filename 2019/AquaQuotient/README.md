## Aqua Quotient

### Idea

This is a multi-phase project that will aim to determine the ratio of water to land in a given photo from the ISS. We aim to then compare against existing satellite images to determine if there has been any radical changes in water availability.

#### Phase I - Data Gathering I

Onboard the ISS we want to take a series of photos on the earth during the daytime. During the two orbits we hope to pass over at least some regions that will have rivers/lakes etc.

#### Phase II - Data Gathering II

During this phase we aim to capture existing satellite images from Google earth and use them to write the program to calculate water and land ratios.

#### Phase III - Comparison of images

When we get the images back from the ISS we aim to use the program from phase to to calculate the land/water ratios of the images and then use the latitude/longitude information of the images to look up the locations in Google earth to perform a similar calculation and then see if there has been a noticeable difference between the two.

### Code

#### Phase I

##### Requirements

The following commands need to be run in order to have code run the data recorder as expected in **space**:

`pip install pyephem`

#### dataRecorder.py

This is the code that will run in space. To run it do the following at the command line:

`python dataRecorder.py`

