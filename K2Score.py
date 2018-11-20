from numpy import log
from collections import deque
from utilities import listEncoder





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
            nijk[encoded] += 1
        else:
            nijk[encoded] = 1

        actualItem.pop()
        encoded = listEncoder(actualItem)

        if len(actualItem) == 0:
            continue

        if encoded in nij:
            nij[encoded] += 1
        else:
            nij[encoded] = 1

    return [nijk, nij]

# finds r

def possibleValues(index, data):
    values = set()
    for i in data:
        if i[index] in values:
            continue
        values.add(i[index])
    return len(values)


def logFactorial(n):
    result = 0
    if n == 0:
        return 0
    while n > 0:
        result = result + log(n)
        n = n - 1
    return result


def K2Secondterm(nijk):
    result = 0
    for i in nijk.values():
        result = result + logFactorial(i)
    return result


def K2Firstterm(nij, r, q):
    result = 0
    missing = q - len(nij)
    for i in nij.values():
        result = result - logFactorial(i + r - 1)
    result = result - missing*logFactorial(r - 1)
    return result


def K2ScoreFunction(index, parents, data):
    rMatrix = data[1]
    data = data[0]
    r = rMatrix[index]

    if len(parents) == 0:  # check if we are in the particulare case where q = 0
        q = 0
    else:
        q = 1
        for i in parents:
            q = q * rMatrix[i]

    nijk = findNijk(index, parents, data)
    secondTerm = K2Secondterm(nijk[0])
    if q == 0:
        firstUpperTerm = logFactorial(r - 1)
    else:
        firstUpperTerm = q * logFactorial(r - 1)
    if q == 0:
        firstLowerTerm = - logFactorial(len(data) + r - 1)
    else:
        firstLowerTerm = K2Firstterm(nijk[1], r, q)
    return secondTerm + firstLowerTerm + firstUpperTerm
