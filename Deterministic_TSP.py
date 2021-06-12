from Dictionaries import *          # import dictionary for graph
from Graph import find_edge_weight  # to find weight of each edge
from itertools import permutations  # to create permutations
import numpy                        # to use numpy arrays
import math                         # to represent infinite
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def fitness(states):
    res = 0
    for i in range(len(states)):
        state_a = states[i]                                                     # tsp.value is number of states
        state_b = states[i + 1]     if i+1 < len(states) else states[0]
        
        res += find_edge_weight(state_a, state_b)                               # Fitness of each individual is calculated based on the sum of all nodes connected in this specific path

    return res


###################### TRAVELING SALESMAN PROBLEM #######################
def solve_deterministic_tsp(states, dist_center, region):

    # permutation will be done for all cities except dist
    states.remove(dist_center)

    all_permutations = list(permutations(states))
    smallest_cost = math.inf

    hist = []
    for individual in all_permutations:
        new_list = numpy.insert(numpy.array(individual), 0, dist_center)
        actual_cost = fitness(new_list)
        smallest_cost = min(smallest_cost, actual_cost)
        hist.append(actual_cost)
   
    
    # PLOTTING
    title = "TSP for region "+ region + "\nSmallest cost: "+ str(smallest_cost)+ " minutes"
    plt.title(title)
    plt.xlabel("Number of Iterations")
    plt.ylabel("Fitness (cost) of each iteration (minutes)")
    plt.plot(hist)

    plt.show()


######## MAIN #########
legend = []
for region, states in dict_regions.items():

    dist_center = distribution_center[region]               # initial city
    solve_deterministic_tsp(states, dist_center, region)
    

