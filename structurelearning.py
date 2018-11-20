import csv

from BICScore import BICScoreFunction

from K2Score import K2ScoreFunction

from utilities import transpose

from MLEEstimation import MLEEstimator

from MLEEstimationVariable import MLEEstimationvar

'''
In this file i will implement k2 algo
pseudocode
input max k, data, scorefunction

pseudocode

while i in columns
    pi = score function(i, emptyset)
    while k < maxK
        find the best father i.e. the one which maximizes the father function
        if bestfather > pi
            pi = bestfather[i, pi+ bestfather]
        else break
    add father set to fathers
return graph
'''



def K2Score(index, parents, data):
    return K2ScoreFunction(index, parents, data)

def BICScore(index, parents, data):
    return BICScoreFunction(index, parents, data)










def maxScore(index, parents, data, scorefunction, rMatrix):

    i = 0

    while i < index:
        if i in parents:
            i = i + 1
            continue
        bestScore = scorefunction(index, parents + [i], [data, rMatrix])
        bestIndex = i
        i = i + 1
        break
    while i < index:
        if i in parents:
            i = i + 1
            continue
        proposedScore = scorefunction(index, parents + [i], [data, rMatrix])
        if proposedScore > bestScore:
            bestScore = proposedScore
            bestIndex = i
        i = i + 1
    return [bestIndex, bestScore]


def K2Algorithm(k, data, scoreFunction):
    rMatrix = [len(i) for i in data[1]]
    data = data[0]

    if len(data) == 0:
        print("no data available")
        exit(-1)
    parents = []
    numberOfColumns = len(data[0])
    for i in range(0, numberOfColumns):
        parents.append([0 for i in range (0,numberOfColumns)])
    totalScore = 0
    i = 0
    while i < numberOfColumns:
        parentsIndexes = []
        actualScore = scoreFunction(i, parentsIndexes, [data, rMatrix])
        for j in range(0, k):
            if j >= i:
                break
            scoreMaxer = maxScore(i, parentsIndexes, data, scoreFunction, rMatrix)
            bestFather = scoreMaxer[0]
            bestScore = scoreMaxer[1]
            if bestScore > actualScore:
                actualScore = bestScore
                parents[i][bestFather] = 1
                parentsIndexes.append(bestFather)
            else:
                break
        totalScore = totalScore + actualScore
        i = i+1

    return [transpose(parents), totalScore]



































