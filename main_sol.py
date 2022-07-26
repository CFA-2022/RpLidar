from astar_sol import astar

import serial
import time

ser = serial.Serial('/dev/ttyACM0')
SCOPE = 1000
gridSize = 150
defaultSize = 30

keyBoard = {
    'UP': ('z', (0, -1)), 
    'DOWN': ('s', (0, 1)), 
    'LEFT': ('q', (-1, 0)), 
    'RIGHT': ('d', (1, 0)) 
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
    timings = (7, 15)
    timing = timings[1]
    if inst[0] in [keyBoard['UP'][0], keyBoard['DOWN'][0]]:
        timing = timings[0]

    i = 0
    while i < timing:
        i += 1
        time.sleep(0.1)
        ser.write(inst[0].encode())
        

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
    w, h = (xMax - xMin + defaultSize*gridSize)//gridSize, (yMax - yMin + defaultSize*gridSize)//gridSize
    if xMax - xMin < SCOPE:
        w = SCOPE // gridSize
    if yMax - yMin < SCOPE:
        h = SCOPE // gridSize

    matrix = [[0 for i in range(w)] for j in range(h)]

    for node in nodes:
        matrix[int(node[1]//gridSize)][int(node[0]//gridSize)] = 1

    printMatrix(matrix)

    start = (yPositiveMin//gridSize, xPositiveMin//gridSize)
    
    end = (h-1, xPositiveMin//gridSize)

    path = astar(matrix, start, end)

    print(start, end)
    print(path)

    inst = getInstructions(path, start)
    print(inst)
    control(inst)


def process_matrix():
    nodes = getNodes('data-position.csv')
    nodes = toInt(nodes)

    w, h = 2*SCOPE//gridSize + 1, 2*SCOPE//gridSize + 1

    matrix = [[0 for i in range(h)] for j in range(w)]

    start = (0, SCOPE//gridSize) # index
    end = (SCOPE//gridSize-1, SCOPE//gridSize) # index
    pointExtremeMinimun = (-SCOPE, -SCOPE) # coordonnees (y,x)

    for node in nodes:
        index = ((node[1]-pointExtremeMinimun[1])//gridSize, (node[0] - pointExtremeMinimun[0])//gridSize) # (y,x)
        matrix[int(index[0])][int(index[1])] = 1

    printMatrix(matrix)

    start = (SCOPE//gridSize, SCOPE//gridSize)
    i = (w-1)//2
    while matrix[i][0] == 1:
        i += 1
    end = (i, 0)

    path = astar(matrix, start, end)

    print(start, end)
    print(path)

    inst = getInstructions(path, start)
    print(inst)
    control(inst)

if __name__ == '__main__':
    #process()
    process_matrix()