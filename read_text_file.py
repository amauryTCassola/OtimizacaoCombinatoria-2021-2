def InstanceFromTextFile(filepath):
    
    f = open(filepath, "r")
    n = int(f.readline())

    distancesMatrix = [[0 for x in range(n)] for y in range(n)]

    for i in range(n):
        currentLine = f.readline()
        distancesRow = currentLine.split(" ")
        for j in range(n):
            distancesMatrix[i][j] = int(distancesRow[j])

    demandsLine = f.readline()
    demandsStringArray = demandsLine.split(" ")
    demandsArray = [int(demandsStringArray[i]) for i in range(n)]

    limitsLine = f.readline()
    limitsStringArray = limitsLine.split(" ")
    limitsArray = [int(limitsStringArray[i]) for i in range(n)]

    return distancesMatrix, demandsArray, limitsArray
        