import sys, csv, math
"""
    It takes a list of file names, and creates two files, one with the raw data from the lidar, and one
    with the x,y coordinates of the lidar.
    
    :param fileNames: a list of two strings, the first is the name of the file to save the data in the
    lidar format, the second is the name of the file to save the data in the position format
"""
from rplidar import RPLidar
from main_sol import process, SCOPE, process_matrix


PORT_NAME = '/dev/ttyUSB0'
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
            if(scan[1]==15 and scan[3] <= SCOPE):
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
    #gui(fileNames[1])

def create(fileName, data):
    file = open(fileName, 'w')
    print("I save my data ")
    for elm in data:
        file.write(str(elm[0])+" , "+str(elm[1]))
        file.write("\n")
    file.close()
   
if __name__ == '__main__':
    fileName1 = "data-lidar.csv"
    fileName2 = "data-position.csv"
    while True:
        run([fileName1, fileName2])
        #process()
        process_matrix()