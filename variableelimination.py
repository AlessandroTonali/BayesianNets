from utilities import transpose
from structurelearning import MLEEstimator
from structurelearning import *
import csv
from copy import deepcopy

# THIS PART IS THE IMPLEMENTATION OF THE POINTWISE MULTIPLICATION

def matrix_access(indexes, matrix, path):
    access_path = []
    for i in indexes:
        for j in path:
            if i == j[0]:
                access_path.append(j[1])
                break
    j = 0
    result = matrix
    while j < len(access_path):




        result = result[access_path[j]]
        j = j + 1
    return result




def matrix_creator(indexes, Cpts):      # do the matrix of the product result
    i = len(indexes) - 1
    matrix = [0 for i in range(0, len(Cpts[indexes[i]][1]))]
    i = i - 1
    while i >= 0:
        matrix = [deepcopy(matrix) for i in range(0, len(Cpts[indexes[i]][1]))]
        i = i -1
    return matrix

def pointwise_mult(index1, matrix1, index2, matrix2, res_matrix, product_indices, path):
    if isinstance(res_matrix, list):
        j = 0
        actual_index = product_indices.pop(0)     #TODO this is slow
        while j < len(res_matrix):
            path.append([actual_index, j])
            res_matrix[j] = pointwise_mult(index1, matrix1, index2, matrix2, res_matrix[j], product_indices, path)
            path.pop()
            j = j + 1
        product_indices.insert(0, actual_index)
        return res_matrix

    else:
        left = matrix_access(index1, matrix1, path)
        right = matrix_access(index2, matrix2, path)
        return left * right








def single_mult(Operator1, Operator2, cpts):
    index1 = Operator1[0]
    matrix1 = Operator1[1]
    index2 = Operator2[0]
    matrix2 = Operator2[1]

    productIndices = deepcopy(index1)

    for i in index2:
        if i in productIndices:
            continue
        productIndices.append(i)

    productIndices.sort()
    result = matrix_creator(productIndices, cpts)
    result = pointwise_mult(index1, matrix1, index2, matrix2, result, productIndices, [])
    return [productIndices, result]

def FinalMultiply(dependentNodes, dependenciesList, cpts):
    to_be_removed = []
    for i in dependentNodes:
        if len(i[0]) == 0:
            to_be_removed.append(i)
    for i in to_be_removed:
        dependentNodes.remove(i)
        dependenciesList.remove(i)
    return multiply(dependentNodes, cpts)


def multiply(dependentNodes, cpts):
    while len(dependentNodes) > 1:
        op1 = dependentNodes.pop(0)
        op2 = dependentNodes.pop(0)
        dependentNodes.append(single_mult(op1, op2, cpts))
    return dependentNodes[0]


# IN THIS PART I WILL IMPLEMENT THE ADDOUT OF A VARIABLE

def reorder(indexes, matrix, index, result, path):
    if isinstance(result, list):
        j = 0
        actual_index = indexes.pop(0)
        while j < len(result):
            path.append([actual_index, j])
            result[j] = reorder(indexes, matrix, index, result[j], path)
            path.pop()
            j = j + 1
        indexes.insert(0, actual_index)
        return result
    else:
        result = matrix
        found = False
        #TODO METTI APPOSTO MFAI CICLO NON FOR
        i = 0
        newPath = deepcopy(path)

        while i < len(path):
            if path[i][0] != index or found:
                result = result[newPath[i][1]]
                i = i + 1
            else:

                popped = newPath.pop()
                newPath.insert(i, popped)
                found = True

        return result



def instantiateReorderedMatrix(indexes, matrix, index):
    lenghtmatrix = []
    scope = matrix
    for i in indexes:
        if i != index:
            lenghtmatrix.append(len(scope))
            scope = scope[0]
        else:
            lenghtofTarget = len(scope)
            scope = scope[0]
    lenghtmatrix.append(lenghtofTarget)
    j = len(lenghtmatrix) - 1
    result = [0 for i in range(0, lenghtmatrix[j])]
    j = j - 1
    while j >= 0:
        result = [deepcopy(result) for i in range(0,lenghtmatrix[j])]
        j = j - 1
    return result

def sumout_lastindex(matrix):
    if isinstance(matrix[0], list):
        j = 0
        while j < len(matrix):
            matrix[j] = sumout_lastindex(matrix[j])
            j = j + 1
        return matrix
    else:
        sum = 0
        for i in matrix:
            sum = sum + i
        return sum


def add_out(list_matrix, index):
    indexes = list_matrix[0]
    matrix = list_matrix[1]

    reorderedInstantiation = instantiateReorderedMatrix(indexes, matrix, index)

    reorderedMatrix = reorder(indexes, matrix, index, reorderedInstantiation, [])
    indexes.remove(index)
    return [indexes, sumout_lastindex(reorderedMatrix)]







def dynamic_matrix_selector(depth, selector, matrix):
    if depth == 0:
        return matrix[selector]
    j = 0
    while j < len(matrix):
        matrix[j] = dynamic_matrix_selector(depth - 1, selector, matrix[j])
        j = j + 1
    return matrix

def observationRemover(obs, probability):
    probMatrix = probability[1]
    indexes = probability[0]
    observedIndex = 0

    j = 0
    for i in indexes:
        if i == obs[0]:
            observedIndex = j
            break
        j = j + 1
    return dynamic_matrix_selector(observedIndex, obs[1], probMatrix)







def variableElimination(index, observations, model):
    '''

    :param index:
    :param observations:
    devo prima capire come scgliere solo le variabili che contano

    prendo il graph ne faccio la trasposta

    prendo solo le variabili che contano (ancestors)


    :param model:
    :return:
    '''


    graph = transpose(model[0])

    xSet = index

    zSet = [i[0] for i in observations]

    ySet = []

    i = 0

    while i < len(model[0]):
        if i != xSet and not(i in zSet):
            ySet.append(i)
        i = i + 1

    #Now let's make a list of tuples where we state the parameters in which every matrix depends

    i = 0

    dependenciesList = []
    while i < len(model[0]):

        parents = graph[i]
        cpt = model[1][i]
        dependecies = []

        j = 0
        dependecies.append(i)
        for z in parents:
            if z == 1:
                dependecies.append(j)
            j = j + 1

        dependenciesList.append([dependecies, cpt])
        i = i + 1

    #now we want to take into account only the values taken from the observations

    for obs in observations:

        for cpts in dependenciesList:

            if obs[0] in cpts[0]:
                cpts[1] = observationRemover(obs, cpts)
                cpts[0].remove(obs[0])

    #now start with multiplications and with sums

    tmp = deepcopy(dependenciesList)

    for i in ySet:

        dependentNodes = []
        for j in dependenciesList:
            if i in j[0]:
                dependentNodes.append(j)

        for j in dependentNodes:
            dependenciesList.remove(j)

        multiplication = multiply(dependentNodes, tmp)
        addition = add_out(multiplication, i)

        dependenciesList.append(addition)

    dependentNodes = []
    for i in dependenciesList:
        dependentNodes.append(i)
    result =  FinalMultiply(dependentNodes, dependenciesList, tmp)[1]

    sum = 0

    for additor in result:
        sum = sum + additor

    j = 0
    while j < len(result):
        result[j] = result[j] / sum
        j = j + 1
    return result












with open('wine.csv', 'r', encoding="utf-8") as csvfile:
    wine = csv.reader(csvfile)
    wine = list(wine)
    wine.pop(0)

a = [[0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
     [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

data = [[1,0,0],
        [1,1,1],
        [0,0,1],
        [1,1,1],
        [0,0,0],
        [0,1,1],
        [1,1,1],
        [0,0,0],
        [1,1,1],
        [0,0,0]]

b = [[0.98,0.03],[0.02,0.97]]

c = [[[1, 1], [0.92, 0.01]], [[0, 0], [0.08, 0.99]]]

result = [[[[0,0],[0,0]],[[0,0],[0,0]]],[[[0,0],[0,0]],[[0,0],[0,0]]]]

#graph = K2Algorithm(5, wine, BICScoreFunction)[0]
#
#cpt = MLEEstimator(graph, wine)


#print(variableElimination(7, [[1, 0], [4, 3], [8, 2], [11, 4], [10,0]], (graph,cpt)))

