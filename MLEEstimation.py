from utilities import transpose
from MLEEstimationVariable import MLEEstimationvar


def MLEEstimator(graph, data):

    graph = transpose(graph)
    if len(graph) == 0:
        print("uncorrect graph")
        exit(-1)
    capableIndexes = [i for i in range (0, len(graph[0]))]
    cpt = []
    index = 0
    for i in graph:
        parents = []
        for j in capableIndexes:
            if i[j] == 1:
                parents.append(j)
        cpt.append(MLEEstimationvar(index, parents, data))
        index = index + 1
    return cpt
