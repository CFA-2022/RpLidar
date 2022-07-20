import sys, numpy as np, csv, math, matplotlib.pyplot as plt
    """
    It takes a list of file names, and creates two files, one with the raw data from the lidar, and one
    with the x,y coordinates of the lidar.
    
    :param fileNames: a list of two strings, the first is the name of the file to save the data in the
    lidar format, the second is the name of the file to save the data in the position format
    """
from turtle import color
from rplidar import RPLidar


PORT_NAME = 'COM4'
DIMENSION_GRID = 40 # dimension of the grid
#PORT_NAME = '/dev/tty.usbserial-0001'

def run(fileNames):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    data = []
    dataPos = []
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for scan in lidar.iter_measurments():
            if(scan[1]==15 and scan[3] <= 500):
                teta = math.radians(scan[-2])
                x = scan[-1] * math.cos(teta)
                y = scan[-1] * math.sin(teta)
                data.append([scan[-2],scan[-1]])
                dataPos.append([x,y])
            if ( len(data) > 300 ):
                break
            #create(fileName, data)
            #print(data)

    except KeyboardInterrupt:
        print('Stoping.')
        
    lidar.stop()
    lidar.disconnect()
    print(data)
    create(fileNames[0], data)
    create(fileNames[1], dataPos)
    gui(fileNames[1])

def create(fileName, data):
    file = open(fileName, 'w')
    print("I save my data ")
    for elm in data:
        file.write(str(elm[0])+" , "+str(elm[1]))
        file.write("\n")
    file.close()

def gui(filename):
    x_values = [x * 40 for x in range(10)]
    y_values = [y * 40 for y in range(10)]
    fig, ax = plt.subplots()
    x = []
    y = []
    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            x.append(float( (row[0].strip()) ))
            y.append(float((row[1].strip())))
    print(x)
    print(y)
    plt.plot(x, y,".")
    plt.plot([0], [0], "x", color='red')
    ax.set_xticks(np.arange(-300, len(x)+1, 40))
    ax.set_yticks(np.arange(-300, len(y)+1, 40))
    plt.grid()
    plt.show()
    
    
if __name__ == '__main__':
    fileName1 = "data-lidar.csv"
    fileName2 = "data-position.csv"
    run([fileName1, fileName2])