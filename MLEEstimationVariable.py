from collections import deque
from copy import deepcopy


def nestedListCreator(iValues, parentsVal):
    if len(parentsVal) == 0:
        return [0 for i in range(0, len(iValues))]

    j = len(parentsVal) - 1
    cpt = [0 for i in range(0, len(parentsVal[j]))]
    j = j - 1
    while j >= 0:
        proposedList = [deepcopy(cpt) for i in range(0, len(parentsVal[j]))]
        cpt = proposedList
        j = j - 1
    return [deepcopy(cpt) for i in range(0, len(iValues))]


def possibleValues(index, data):
    values = set()
    for i in data:
        if i[index] in values:
            continue
        values.add(i[index])
    return values


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
        encoded = tuple(actualItem)

        if encoded in nijk:
            nijk[encoded][1] += 1
        else:
            nijk[encoded] = [actualItem, 1]

        actualItem.pop()
        encoded = tuple(actualItem)

        if len(actualItem) == 0:
            continue

        if encoded in nij:
            nij[encoded] += 1
        else:
            nij[encoded] = 1

    return [nijk, nij]


def ListAcces(nestedList, parentsval, path, nijk, nij, r):
    if isinstance(nestedList, list):
        j = 0
        thisParents = parentsval.popleft()
        for i in thisParents:
            path.append(i)
            nestedList[j] = ListAcces(nestedList[j], parentsval, path, nijk, nij, r)
            j = j + 1
            path.pop()
        parentsval.appendleft(thisParents)
    else:
        x = path
        j = x.pop(0)
        x.append(j)
        if tuple(x) in nijk:

            nijkindex = nijk[tuple(x)]
            nijindex = nij[tuple(nijkindex[0])]

        else:
            x = deepcopy(path)

            nijkindex = ["padding", 0]
            x.pop()
            if tuple(x) in nij:
                nijindex = nij[tuple(x)]
            else:
                nijindex = 0

        if nijindex == 0:
            nestedList = 1 / r
        else:
            nestedList = (nijkindex[1] + 0.01) / (nijindex + 0.01 * r)

        j = path.pop()
        path.insert(0,j)

    return nestedList


def MLEEstimationvar(variable, parents, data ):
    rMatrix = data[1]
    data = data[0]
    nijks = findNijk(variable, parents, data)
    nijk = nijks[0]
    nij = nijks[1]
    ivalues = rMatrix[variable]
    ivalues.sort()
    r = len(rMatrix[variable])
    if len(parents) == 0:
        q = 0
        cpt = [0 for i in range(0, r)]
        j = 0
        for i in ivalues:
            z = [i]
            z = tuple(z)
            if z in nijk:
                nijk_val = nijk[z][1]
            else:
                nijk_val = 0
            cpt[j] = (nijk_val + 0.01) / (len(data) + r * 0.01)
            j = j + 1
        return cpt

    else:
        q = 1
        parentsval = deque()

        for i in parents:
            actualVal = rMatrix[i]
            actualVal.sort()
            q = q * len(actualVal)
            parentsval.append(actualVal)
    cpt = nestedListCreator(ivalues, parentsval)
    parentsval.insert(0, ivalues)

    return ListAcces(cpt, parentsval, [], nijk, nij, r)





