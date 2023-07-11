import colorHelper

def text2Tuple(txt):
    return tuple(txt)


PRINTCHAR = {-1: "#", 0: " ", 1: "O", 2: "-", 3 : "+", 4: "*", 5: "±", 6:"@", 7:"$"}
def printMatrix(matrix, offset = "", showLineNum=True, printDict=None):
    if printDict is None:
        printDict = PRINTCHAR
    LEADING = 4
    if showLineNum:
        width = len(matrix[0])
        
        #Tientallen 
        if width > 10:            
            line = offset + LEADING * " "
            for x in range(width):
                if x % 10 == 0:
                    line += f"{(x // 10) % 10}"
                else:
                    line += " "
            print(line)
        #enkelen
        line = offset + LEADING * " "
        for x in range(width):
            line += f"{x % 10}"
        print(line)
        print(offset + (LEADING+width)*"-")
    line = 0
    for row in matrix:
        value = ""
        for d in row:
            if d in printDict:
                value += printDict[d]
            elif d == 0:
                value += " "
            else:
                value += "O"
                    
        if showLineNum:
            value = offset + f"{line:3} " + value
            line += 1
        else:
            value = offset + value
        print(value)

def tuple2Matrix(tpl):
    m = []
    for row in tpl:
        m.append(list(row))
    return m

def areLinesSame(line1, line2):
    if len(line1) != len(line2):
        return False
    for x in range(len(line1)):
        if line1[x] != line2[x]:
            return False
    return True

def areMatrixSame(matrix1, matrix2):
    if len(matrix1) != len(matrix2):
        return False
    for y in range(len(matrix1)):
        if not areLinesSame(matrix1[y], matrix2[y]):
            return False
    return True 
    
# create a new matrix width x height of color
def createMatrix(color=2, width=32, height=32):
    m = []
    row = width * [color]
    while height > 0:
        m.append(row.copy())
        height -= 1
    return m

def copyMatrix(matrix):
    newMatrix = []
    for row in matrix:
        newMatrix.append(row.copy())
    return newMatrix

def changeMatrix(matrix, fromColor, toColor):
    newMatrix = []
    for row in matrix:
        newRow = []
        for x in row:
            if x == fromColor:
                x = toColor
            newRow.append(x)
        newMatrix.append(newRow)
    return newMatrix

def getDimensions(matrix):
    return blockWidth(matrix), blockHeight(matrix)

def blocksOnRow(line):
    count = 0
    for x in line:
        if x != 0:
           count += 1
    return count

def blocksOnColumn(matrix, x):
    count = 0
    for line in matrix:
        if line[x] != 0:
           count += 1
    return count

def blockWidth(matrix):
    maxCount = 0
    for line in matrix:
       maxCount = max(maxCount, blocksOnRow(line))
    return maxCount

def blockHeight(matrix):
    maxCount = 0
    for x in range(len(matrix[0])):
        maxCount = max( maxCount, blocksOnColumn(matrix, x))
    return maxCount
    
def hLine(matrix, x, y, xEnd, color):
    for i in range(x, xEnd):
        matrix[y][i] = color

def vLine(matrix, x, y, yEnd, color):
    for i in range(y, yEnd):
        matrix[i][x] = color
    
# change the colors of the origional matrix
def changeColor(m, fromColor, toColor):
    for row in m:
        for x in range(len(row)):
            if row[x] == fromColor:
                row[x] = toColor
    return m

def lowerColorIntensity(m, factor):
    for row in m:
        for x in range(len(row)):
            r,g,b = colorHelper.getRGBfromInt(row[x])
            newValue = (int(r* factor), int(g* factor), int(b* factor))            
            row[x] = newValue
    return m


def getMatrixWidthHeight(m):
    return len(m[0]), len(m)


# mergeMatrix is smaller than mainMatrix
def mergeMatrix(mainMatrix, mergeMatrix, tranparentColor=-1):
    width1, height1 = getMatrixWidthHeight(mainMatrix)
    width2, height2 = getMatrixWidthHeight(mergeMatrix)
    offsetMergeX = max(0, (width1 - width2) // 2)
    offsetMergeY = max(0, (height1 - height2) // 2)
    print(width1, height1, width2, height2, offsetMergeX, offsetMergeY)

    newMatrix = []
    for y, row in enumerate(mainMatrix):
        mergePosY = y - offsetMergeY
        if mergePosY >= 0 and mergePosY < height2:
            mergeRow = mergeMatrix[mergePosY]
        else:
            mergeRow = None
        newRow = []
        for x, element in enumerate(row):
            mergePosX = x - offsetMergeX
            if mergeRow != None and mergePosX >= 0 and mergePosX < width2:
                mergeElement = mergeRow[mergePosX]
                if mergeElement == tranparentColor:
                    mergeElement = element
                newRow.append(mergeElement)
            else:
                newRow.append(element)
        newMatrix.append(newRow)
    return newMatrix


# get the character from the matrix`dict
# empty space shoud always be present
def getMatrix(key, characterMatrixDict):
    if key in characterMatrixDict:
        return characterMatrixDict[key]
    return characterMatrixDict[" "]


# ls is a list of elements
# matrixDict is a dictionary with matrix characters as result
# returns list of matrix Characters
def elementsToMatrix(ls, matrixDict):
    m = []
    for element in ls:
        m.append(getMatrix(element, matrixDict))
    return m


def printDict(matrixDict):
    for c in matrixDict.keys():
        printMatrix(getMatrix(c, matrixDict))
        print()


# listOfChars is a list of dot_matrix chars
# all characters must be of the same height
# returns a matrix with all the characters
def appendMatrixHorizontal(listOfChars, sep=1, emptyValue=0):
    allCharacters = []
    if len(listOfChars) == 0:
        return allCharacters
    seperator = sep * [emptyValue]
    y = 0
    _, maxY = getMatrixWidthHeight(listOfChars[0])
    while y < maxY:
        line = []
        maxIndex = len(listOfChars) - 1
        for index, c in enumerate(listOfChars):
            line += c[y]
            if index != maxIndex:
                line += seperator
        allCharacters.append(line)
        y = y + 1
    return allCharacters


# listOfChars is a list of dot_matrix chars
# all characters must be of the same Width
# returns a matrix with all the characters
def appendMatrixVertical(listOfMatrix, sep=1, emptyValue=0):
    allCharacters = []
    if len(listOfMatrix) == 0:
        return allCharacters

    width = len(listOfMatrix[0][0])
    seperator = width * [emptyValue]
    for m in listOfMatrix:
        for c in m:
            allCharacters.append(c)
        for _ in range(sep):
            allCharacters.append(seperator)
    return allCharacters


def _alignCenter(matrix, width, emptyValue=0):
    newMatrix = []
    spaces = max(0, (width - len(matrix[0])))
    leadingCount = spaces // 2
    leading = leadingCount * [emptyValue]
    ending = (spaces - leadingCount) * [emptyValue]
    for row in matrix:
        newMatrix.append(leading + row + ending)
    return newMatrix


def _alignMiddle(matrix, height, emptyValue=0):
    newMatrix = []
    rowSpaces = len(matrix[0]) * [emptyValue]

    count = 0
    leading = max(0, (height - len(matrix))) // 2
    while count < leading:
        newMatrix.append(rowSpaces)
        count += 1

    for row in matrix:
        count += 1
        newMatrix.append(row)
        if count > height:
            return newMatrix

    while count < height:
        newMatrix.append(rowSpaces)
        count += 1

    return newMatrix


def _alignLeft(matrix, width, emptyValue=0):
    newMatrix = []
    endingCount = max(0, (width - len(matrix[0])))
    ending = endingCount * [emptyValue]
    for row in matrix:
        newMatrix.append(row + ending)
    return newMatrix


def _alignRight(matrix, width, emptyValue=0):
    newMatrix = []
    leadingCount = max(0, width - len(matrix[0]))
    leading = leadingCount * [emptyValue]
    for row in matrix:
        newMatrix.append(leading + row)
    return newMatrix


# alignPos = 0 Left, 1=center, 2=right
def alignHorizontal(matrix, width, alignPos=0, emptyValue=0):
    if alignPos == 0:
        return _alignLeft(matrix, width, emptyValue)
    if alignPos == 2:
        return _alignRight(matrix, width, emptyValue)
    return _alignCenter(matrix, width, emptyValue)


def alignVertical(matrix, height, alignPos=0, emptyValue=0):
    if alignPos == 0:  # top
        return matrix
    if alignPos == 2:  # bottom
        return matrix
    return _alignMiddle(matrix, height, emptyValue)

def moveMatrix(matrix, dX=0, dY=0):
    newMatrix = []
    #move in x
    width = len(matrix[0])
    if dX > width:
        dX = width
    if dX < -width:
        dX = -width
        
    for row in matrix:
        if dX == 0:
           data = row 
        elif dX > 0:
            data = [0] * dX
            data += row[0: width - dX]        
        elif dX < 0:
            data = row[-dX:width + dX]    
            data += [0] * (-1 * dX)
        newMatrix.append(data)
    if dY == 0:
        return newMatrix
    
    #move in Y
    height = len(matrix)
    if dY > height:
        dY = height
    if dY < -height:
        dY = -height
    row = width * [0]
    if dY < 0: #add row on top
        newMatrix = newMatrix[-dY:height]
        while dY < 0:
            newMatrix.append(row)
            dY += 1
    else:
        newMatrix = newMatrix[0:height-dY]
        while dY > 0:
            newMatrix.insert(0, row)
            dY -= 1
    return newMatrix
    
    
if __name__ == "__main__":
    matrix = {"6": ((0,1,1,0),
                    (1,1,1,1),
                    (1,1,1,1),
                    (0,1,1,0))}
    
    listMatrix = elementsToMatrix("6", matrix)
    completeMatrix1 = appendMatrixHorizontal(listMatrix, 2)
    completeMatrix1 = alignHorizontal(completeMatrix1, 32, 1)
    completeMatrix1 = alignVertical(completeMatrix1, 32, 1)
    printMatrix(completeMatrix1)
    completeMatrix1 = moveMatrix(completeMatrix1, 10, 10)
    printMatrix(completeMatrix1)
    
    if False:
        listMatrix = elementsToMatrix("0123456789ABC", matrix.MATRIX)
        completeMatrix1 = appendMatrixHorizontal(listMatrix, 2)
        completeMatrix1 = alignHorizontal(completeMatrix1, 32, 1)
        completeMatrix1 = alignVertical(completeMatrix1, 32, 1)
        printMatrix(completeMatrix1)
        completeMatrix2 = changeColor(completeMatrix1, 1, 2)
        printMatrix(completeMatrix2)

    if False:
        import matrixArt

        mainMatrix = tuple2Matrix(matrixArt.matrixArt32x32)
        # mainMatrix = createMatrix(0, 32, 32)
        printMatrix(mainMatrix)

        changeColor(mainMatrix, 0, 2)
        printMatrix(mainMatrix)

        import matrix_16x16 as matrix

        # print(text2Tuple("Hoi 1234"))
        listMatrix = elementsToMatrix("1", matrix.MATRIX)
        completeMatrix1 = appendMatrixHorizontal(listMatrix, 1)
        completeMatrix1 = alignHorizontal(completeMatrix1, 32, 1)
        printMatrix(completeMatrix1)

        merged = mergeMatrix(mainMatrix, completeMatrix1, 0)
        printMatrix(merged)

    #     
    #     
    #     
    #     listMatrix = elementsToMatrix("3", matrix.MATRIX)
    #     completeMatrix = appendMatrixHorizontal(listMatrix, 1)
    #     completeMatrix2 = alignHorizontal(completeMatrix, 32, 0)
    #     #printMatrix(completeMatrix2)
    #     
    #     completeMatrix2 = alignHorizontal(completeMatrix, 32, 2)
    #     #printMatrix(completeMatrix2)
    #     
    #     completeMatrix2 = alignHorizontal(completeMatrix, 32, 1)
    #     #printMatrix(completeMatrix2)
    #     
    #     completeMatrix2 = appendMatrixVertical((completeMatrix1, completeMatrix2), 1)
    #     #printMatrix(completeMatrix2)
    #     
    #     completeMatrix2 = changeColor(completeMatrix2, 0, 2)
    #     
    #     completeMatrix2 = alignVertical(completeMatrix2, 32, 1)
    #     completeMatrix2 = changeColor(completeMatrix2, 0, 2)
    #     printMatrix(completeMatrix2)







