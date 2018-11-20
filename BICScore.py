from numpy import log
from collections import deque
from utilities import listEncoder





def possibleValues(index, data):
    values = set()
    for i in data:
        if i[index] in values:
            continue
        if i[index] == 4:
            j = 1
        values.add(i[index])
    return len(values)


# finds nijk and nij

def findNijk(index, parents, data):
    nijk = {}
    nij = {}
    importantindex = parents + [index]
    preprocessed = deque()
    supportList = deque()

    for i in data:
        for j in importantindex:
            supportList.append(i[j])
        preprocessed.append(supportList)
        z = 0
        supportList = deque()

    # now for every line you put it in the dictionary
    # the list should be encoded because the lists can't be the key of a dictionary

    while len(preprocessed) > 0:

        actualItem = preprocessed.popleft()
        encoded = listEncoder(actualItem)

        if encoded in nijk:
            nijk[encoded][1] += 1
        else:
            nijk[encoded] = [actualItem, 1]

        actualItem.pop()
        encoded = listEncoder(actualItem)


        if encoded in nij:
            nij[encoded] += 1
        else:
            nij[encoded] =  1

    return [nijk, nij]


def BICScoreFunction(index, parents, data):
    rMatrix = data[1]
    data = data[0]

    r = rMatrix[index]
    if len(parents) == 0:
        q = 0
    else:
        q = 1
        for i in parents:
            q = q * rMatrix[i]

    secondterm = - q * (r - 1) * log(len(data))

    parameters = findNijk(index, parents, data)
    nijk = parameters[0]
    nij = parameters[1]
    firstTerm = 0
    for i in nijk.values():
        actualij = nij[listEncoder(i[0])]
        firstTerm = firstTerm + i[1]*(log(i[1]) - log(actualij))

    return 2 * firstTerm + secondterm

