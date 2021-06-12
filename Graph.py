from Dictionaries import *                          # import dictionary for graph
from collections import defaultdict                 # import dictionary for graph

# ADD EDGE ON GRAPH
def __addEdge(graph,u,v,weight):
    graph[u].append((v,weight))
  

# FIND WEIGHT OF EACH EDGE
def find_edge_weight(state1, state2):
    for pair, time in dict_travel_time.items():
        if pair[0] == state1 and pair[1] == state2 or pair[0] == state2 and pair[1] == state1:
            #print("State1 : ", state1, "    - State2: ", state2, "  - Distance: ", time)
            return time
    return -1;


#SHOWING THE GRAPH
def show_graph(graph):
    for node in graph:
        print("Processing node: ", node)
        for neighbour in graph[node]:
            print(neighbour[0], " - ", neighbour[1], end = ", ")
        print("\n")

    print("\n\n\n")

# BUILD THE GRAPH ACCORDING TO DICTIONARY
def build_graph():    
    graph = defaultdict(list)

    # CREATING THE EDGES
    for region, values in dict_regions.items():   # each region has a list as value
        for state1 in values:
            for state2 in values:
                if state1 != state2:
                    weight = find_edge_weight(state1, state2)                  #find the weight of the two states using the dictionary
                    __addEdge(graph,state1,state2, weight)
    
    return graph

