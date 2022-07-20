from astar import astar

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

nodes = getNodes('data-position.csv')
nodes = toInt(nodes)

gridSize = 40

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

w, h = (xMax - xMin)//gridSize + 1, (yMax - yMin)//gridSize + 1
matrix = [[0 for i in range(w)] for j in range(h)]

for node in nodes:
    matrix[int(node[1]//gridSize)][int(node[0]//gridSize)] = 1

matrix[yPositiveMin//gridSize][xPositiveMin//gridSize] = 0    
matrix[h//2][w-1] = 0  

printMatrix(matrix)

start = (yPositiveMin//gridSize, xPositiveMin//gridSize)
end = (h//2, w-1)

path = astar(matrix, start, end)

print(path)