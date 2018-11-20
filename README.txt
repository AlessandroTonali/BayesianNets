In this repository you can find some tools for bayesian newtowrks
For structure learning there is the code of K2Algorithm, the signature of the function is:

AdjacencyGraph = K2Algorithm(k, data, scorefunction)

Where adjacency graph is the graph in which for every line there is 1 on the index of child nodes
k is the max number of children a node can have
data is the tuple  (input dataset, listvalues)
where listvalues is a list containing the list of all the values each column can take 
for example if we have two columnns and the first can take values 1,2 while the second 0,1,2  
listvalues = [[1,2],[0,1,2]] # this is useful for the estimation
scorefunction is the scorefunction we want to use for the algorithm ( BICScore and logK2Score are provided)
For parameter estimation i provide the MaximumLikelyHood estimation whose signature is the following:
cpt = MLEEstimation(graph,data)
where cpt list is a list containing n = #nodes elements and each element is 
the probability a nested list, for accessing you should access cpt[ni][f1][..][fn]
where ni is the i-th value the node takes, f1 is the value tha the father 1 takes until the n-th father and you will get the probability f this combination
 
Inference

for inference i coded the varible elimination algorithm whose signature is:
probability =  variableElimination(index, observations, model)

index is the index we are interested in finding the probability
obesrvation is a list of tuples (index, observed value)
model is the tuple (graph, cpt) 

