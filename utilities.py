from copy import deepcopy

def listEncoder(array):
    if len(array) == 0:
        return ""
    encode = str(array[0])
    i = 1
    while i < len(array):
        encode = encode + "#"
        encode = encode + str(array[i])
        i = i + 1
    return encode

def transpose(matrix):
    result = deepcopy(matrix)
    i = 0
    j = 0
    while i < len(matrix):
        while j < len(matrix[0]):
            result[j][i] = matrix[i][j]
            j = j + 1
        j = 0
        i = i + 1
    return result