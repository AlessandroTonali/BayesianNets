
from variableelimination import variableElimination

from copy import deepcopy


def accuracy(data, index, model):
    rMatrix = data[1]
    data = data[0]
    sum = 0
    best_index = 0
    for r in data:

        path = []
        j = 0
        while j < len(r):
            if j == index:
                j = j + 1
                continue
            if r[j] not in rMatrix[j]:
                print("ciao")
            k = rMatrix[j].index(r[j])
            path.append([j, k])
            j = j + 1

        cpt = variableElimination(index, path, deepcopy(model))
        max_el = max(cpt)
        i = 0
        while i < len(cpt):
            if cpt[i] == max_el:
                best_index = i
            i = i + 1
        if int(r[index]) == int(rMatrix[index][best_index]):

            sum = sum + 1
    return sum/len(data)









