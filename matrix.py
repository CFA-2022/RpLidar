# matrix taille 
#sX = 2 * SCOPE // gridSize

#sY == SCOPE // gridSize

#Position de robo: matrix[0][SCOPE//gridSize]


from astar_sol import astar

import serial
import time

#ser = serial.Serial('/dev/ttyACM0')
SCOPE = 500
gridSize = 40

keyBoard = {
    'UP': ('z', (1, 0)), #0,1
    'DOWN': ('s', (-1, 0)), #0,-1
    'LEFT': ('q', (0, 1)), # Test2: 0, -1
    'RIGHT': ('d', (0, -1)) # Test2: 0, 1
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
    for i in range(len(matrix)-1, -1, -1):
        print(matrix[i])

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
            #ser.write(inst[0].encode())

    if inst[0] == 'q' or inst[0] == 'd':
        i = 0
        while i<30:
            i += 1
            time.sleep(0.1)
            #ser.write(inst[0].encode())        

def process():
    nodes = getNodes('data-position.csv')
    nodes = toInt(nodes)

    w, h = SCOPE//gridSize + 1, 2*SCOPE//gridSize + 1

    matrix = [[0 for i in range(h)] for j in range(w)]

    start = (0, SCOPE//gridSize) # index
    end = (SCOPE//gridSize-1, SCOPE//gridSize) # index
    pointExtremeMinimun = (-SCOPE, 0) # coordonnees (y,x)

    for node in nodes:
        #if node[1] < 0:
        #    continue
        index = ((node[1]-pointExtremeMinimun[1])//gridSize, (node[0] - pointExtremeMinimun[0])//gridSize) # (y,x)
        print(node, index)
        matrix[int(index[0])][int(index[1])] = 1

    #matrix[0][13] = 1
    #matrix[1][12] = 1
    #matrix[2][13] = 1

    printMatrix(matrix)

    start = (0, (h-1)//2)
    
    end = (w-2, (h-1)//2)

    path = astar(matrix, start, end)

    print(start, end)
    print(path)

    inst = getInstructions(path, start)
    print(inst)
    #control(inst)

if __name__ == '__main__':
    process()
