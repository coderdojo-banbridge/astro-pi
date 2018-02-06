class Config:
    fieldnames = ['time', 'lat', 'long', 'photo', 'lux']
    resultsDirectory = '/home/pi/luxquestdata/'
    dateTimeFormat = '%Y-%m-%d-%H-%M-%S'
    issLine1 = '1 25544U 98067A   17332.28575632  .00003326  00000-0  57234-4 0  9993'
    issLine2 = '2 25544  51.6431 300.2614 0004099 158.9129 343.4648 15.54248554 87274'
    isoValue = 400
    recordingLoopDelay = 1
    maxStackHeight = 120
    maxRowLength = 120
