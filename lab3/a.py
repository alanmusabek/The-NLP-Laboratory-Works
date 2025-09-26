def getMinEditDistance(source, target):
    cols = len(target) + 1
    rows = len(source) + 1
    matrix_zeros = [[0 for i in range(cols)] for j in range(rows)] # generate two dimentional array
    for i in range(len(source) + 1):
        # your code
        matrix_zeros[i][0] = i

    for j in range(len(target) + 1):
        # your code
        matrix_zeros[0][j] = j
    
    print(matrix_zeros)

getMinEditDistance("Start", "Finish")