#
#Matrix = [[1, 0, 1, 1],
#          [1, 0, 1, 1],
#          [1, 1, 1, 0],
#          [1, 0, 1, 0]]
#Start =  (2, 0)
#Finish = (0, 2)


def findPath(Matrix, WallMatrix, Start, Finish):
    resPath = {0:[Start], }
    res = []
    check = True
    currentPosition = Start
    i = 0
    counter = 0
    if Finish != -1:
        if Matrix[Start[1]][Start[0]] and Matrix[Finish[1]][Finish[0]]:
            while currentPosition != Finish:
                if len(Matrix[0])*len(Matrix) <= counter:
                    return -1
                for currentPosition in resPath[i]:
                    if currentPosition == Finish:
                        break
                    newPoints = checkAround(currentPosition, Matrix, WallMatrix)
                    for newPoint in newPoints:
                        for j in list(resPath.values()):
                            if newPoint in j:
                                check = False
                        if not newPoint in res and check:
                            res += [newPoint]
                        check = True

                if Finish in res:
                    res = [Finish]
                i += 1
                resPath[i] = res
                res = []
                counter += 1
            resPath = output(resPath, i, Matrix, WallMatrix, Start)
            return resPath
        else:
            return False


def output(resPath, endOfDictionary, Matrix, WallMatrix, Start):
    try:
        res = [resPath[len(resPath.keys())-2][0], ]
    except KeyError:
        return -1
    endOfDictionary-=1
    while not Start in res:
        for i in range(0, endOfDictionary):
            pointsAround = checkAround(res[len(res)-1], Matrix, WallMatrix)
            for j in pointsAround:
                if j in resPath[i] and not j in res:
                    res.append(j)
                    endOfDictionary -= 1
                    break
    res.reverse()
    return res


def checkAround(currentPosition, Matrix, WallMatrix):
    res = []
    currentPositionX, currentPositionY = currentPosition
    MatrixSize = (len(Matrix), len(Matrix[0]))
    if(currentPositionX + 1 < MatrixSize[1] and Matrix[currentPositionY][currentPositionX+1]): # Проверка справа
        if not WallMatrix[currentPositionY][currentPositionX][3] and not WallMatrix[currentPositionY][currentPositionX+1][1]:
            res.append((currentPositionX+1, currentPositionY))

    if(currentPositionX - 1 >= 0 and Matrix[currentPositionY][currentPositionX-1]): # Проверка слева
        if not WallMatrix[currentPositionY][currentPositionX][1] and not WallMatrix[currentPositionY][currentPositionX-1][3]:
            res.append((currentPositionX-1, currentPositionY))

    if(currentPositionY + 1 < MatrixSize[0] and Matrix[currentPositionY+1][currentPositionX]): # Проверка снизу
        if not WallMatrix[currentPositionY][currentPositionX][0] and not WallMatrix[currentPositionY+1][currentPositionX][2]:
            res.append((currentPositionX, currentPositionY+1))

    if(currentPositionY - 1 >= 0 and Matrix[currentPositionY-1][currentPositionX]): # Проверка сверху
        if not WallMatrix[currentPositionY][currentPositionX][2] and not WallMatrix[currentPositionY-1][currentPositionX][0]:
            res.append((currentPositionX, currentPositionY-1))

    return res  # 1 Проверка справа, 2 Проверка слева, 3 Проверка снизу, 4 Проверка сверху

#print(findPath(Matrix, Start, Finish))