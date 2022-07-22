from astar_sol import astar

import serial
import time

ser = serial.Serial('/dev/ttyACM0')
SCOPE = 1000
gridSize = 150
defaultSize = 30

keyBoard = {
    'UP': ('z', (0, -1)), #0,1
    'DOWN': ('s', (0, 1)), #0,-1
    'LEFT': ('q', (1, 0)), # Test2: 0, -1
    'RIGHT': ('d', (-1, 0)) # Test2: 0, 1
}


def getNodes(fileName):
    with open(fileName) as f:
        lines = f.readlines()
        nodes = []
        for line in lines:
            splited = line.split(' , ')
            nodes.append((float(splited[0]), float(splited[1])))
        
        return nodes

def toInt(nodes):
    return [(int(x[0]), int(x[1])) for x in nodes]

def printMatrix(matrix):
    for i in matrix:
        print(i)

def convertToListOfPositive(nodes, xMin, yMin):
    xPositiveMin = xMin
    if xMin < 0:
        xPositiveMin *= -1

    yPositiveMin = yMin
    if yMin < 0:
        yPositiveMin *= -1

    return [(x[0]+xPositiveMin, x[1] + yPositiveMin) for x in nodes]

def writeInstructions(fileName, instructions):
    with open(fileName, 'w') as f:
        for i in instructions:
            f.write(i+'\n')

def getInstructions(path, currentPosition):
    inst = []
    for p in range(1, len(path)):
        direction = (path[p][0]-currentPosition[0], path[p][1]-currentPosition[1])
        if direction == keyBoard['UP'][1]:
            inst.append(keyBoard['UP'][0])
        if direction == keyBoard['DOWN'][1]:
            inst.append(keyBoard['DOWN'][0])
        if direction == keyBoard['LEFT'][1]:
            inst.append(keyBoard['LEFT'][0])
        if direction == keyBoard['RIGHT'][1]:
            inst.append(keyBoard['RIGHT'][0])
        currentPosition = path[p]

    return inst

def control(inst):
    if inst[0] == 's' or inst[0] == 'z':
        i = 0
        while i<10:
            i += 1
            time.sleep(0.1)
            ser.write(inst[0].encode())

    if inst[0] == 'q' or inst[0] == 'd':
        i = 0
        while i<30:
            i += 1
            time.sleep(0.1)
            ser.write(inst[0].encode())
    #i = 0
    #while i<10:
    #    i += 1
    #    time.sleep(0.1)
    #    ser.write(inst[1].encode())
        

def process():
    nodes = getNodes('data-position.csv')
    nodes = toInt(nodes)

    xMin = min(x[0] for x in nodes)
    xMax = max(x[0] for x in nodes)
    yMin = min(x[1] for x in nodes)
    yMax = max(x[1] for x in nodes)

    xPositiveMin = xMin
    if xMin < 0:
        xPositiveMin *= -1

    yPositiveMin = yMin
    if yMin < 0:
        yPositiveMin *= -1

    nodes = convertToListOfPositive(nodes, xMin, yMin)
    #print(nodes)
    w, h = (xMax - xMin + defaultSize*gridSize)//gridSize, (yMax - yMin + defaultSize*gridSize)//gridSize
    if xMax - xMin < SCOPE:
        w = SCOPE // gridSize
    if yMax - yMin < SCOPE:
        h = SCOPE // gridSize

    matrix = [[0 for i in range(w)] for j in range(h)]

    #for i in range(0,w):
    #    for j in range(0,h):
    #        if (i == 0 or i == w or j == 0 or j == h ):
    #            matrix[i][j] = 1


    for node in nodes:
        matrix[int(node[1]//gridSize)][int(node[0]//gridSize)] = 1

    #matrix[4][12] = 1
    #matrix[yPositiveMin//gridSize][xPositiveMin//gridSize] = 0    
    #matrix[h//2][w-1] = 0  

    printMatrix(matrix)

    start = (yPositiveMin//gridSize, xPositiveMin//gridSize)
    
    end = (h-1, xPositiveMin//gridSize)

    path = astar(matrix, start, end)

    print(start, end)
    print(path)

    inst = getInstructions(path, start)
    #writeInstructions('instructions.txt', inst)
    print(inst)
    control(inst)


def transform_matrix(matrix, start, end):
    pass

def process_matrix():
    nodes = getNodes('data-position.csv')
    nodes = toInt(nodes)

    w, h = 2*SCOPE//gridSize + 1, 2*SCOPE//gridSize + 1

    matrix = [[0 for i in range(h)] for j in range(w)]

    start = (0, SCOPE//gridSize) # index
    end = (SCOPE//gridSize-1, SCOPE//gridSize) # index
    pointExtremeMinimun = (-SCOPE, -SCOPE) # coordonnees (y,x)

    for node in nodes:
        #if node[1] < 0:
        #    continue
        index = ((node[1]-pointExtremeMinimun[1])//gridSize, (node[0] - pointExtremeMinimun[0])//gridSize) # (y,x)
        #print(node, index)
        matrix[int(index[0])][int(index[1])] = 1

    #matrix[0][13] = 1
    #matrix[1][12] = 1
    #matrix[2][13] = 1

    printMatrix(matrix)

    #start = (0, (h-1)//2)
    start = (SCOPE//gridSize, SCOPE//gridSize)
    #end = (w-2, (h-1)//2)
    i = 0
    while matrix[i][0] == 1:
        i += 1
    end = (i, 0)

    #matrix, start, end = transform_matrix(matrix, start, end)

    path = astar(matrix, start, end)

    print(start, end)
    print(path)

    inst = getInstructions(path, start)
    print(inst)
    control(inst)

if __name__ == '__main__':
    #process()
    process_matrix()