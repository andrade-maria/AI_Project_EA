from dictionaries import *                          # import dictionary for graph
from collections import defaultdict                 # import dictionary for graph
import matplotlib.pyplot as plt                     # to plot the graphs
from evo import Evolution                           # import other files in this folder
from tsp import TSP                                 # import other files in this folder
from itertools import permutations                  # to create permutations

# VARIABLE TO SAVE OUR WHOLE GRAPH
graph = defaultdict(list)

# ADD EDGE ON GRAPH
def addEdge(graph,u,v,weight):
    graph[u].append((v,weight))
  
# FIND WEIGHT OF EACH EDGE
def __find_weight(state1, state2):
    for pair, time in dict_travel_time.items():
        if pair[0] == state1 and pair[1] == state2 or pair[0] == state2 and pair[1] == state1:
            #print("State1 : ", state1, "    - State2: ", state2, "  - Distance: ", time)
            return time
    return -1;

# GET NUMBER OF VACCINES THAT EACH STATE SHOULD RECEIVE
def __get_number_vaccines_by_state(total_vaccines):
    lst = list()
    for key, values in dict_states.items():                                         #first element of value is state, second is %pop
        amount = int((values[1]*total_vaccines)/100.0)
        lst.append((values[0], amount))

    return lst

# FIND THE FITNESS FOR EACH INDIVIUAL (FEASIBLE SOLUTION)
def tsp_fitness_creator():

    def fitness(tsp):
        res = 0
        for i in range(len(tsp.value)):                                             # tsp.value is number of states
            if i+1 != len(tsp.value):
                res += __find_weight(tsp.value[i], tsp.value[i + 1])                # Fitness of each individual is calculates based on the sum of all nodes connected in this specific path
            else:
                res += __find_weight(tsp.value[i], tsp.value[0])
        return -res
        
    return fitness                                                                  # return the memory address in which the fitness function can be reached


################################## MAIN #############################

# CREATING THE EDGES
for region, values in dict_regions.items():   # each region has a list as value
    for state1 in values:
        for state2 in values:
            if state1 != state2:
                weight = __find_weight(state1, state2)                  #find the weight of the two states using the dictionary
                addEdge(graph,state1,state2, weight)

# calculate the number of vaccines needed for each state
total_vaccines = 50000000
number_vaccines_per_state = __get_number_vaccines_by_state(total_vaccines)



#SHOWING THE GRAPH
for node in graph:
    print("Processing node: ", node)
    for neighbour in graph[node]:
        print(neighbour[0], " - ", neighbour[1], end = ", ")
    print("\n")

print("\n\n\n")


# SHOWING AMOUNT OF VACCINES PER STATE
soma = 0
stt = list()
v = list()
for i in number_vaccines_per_state:
    stt.append(i[0])
    v.append(i[1])



# CALCULATE BEST PATH FOR EACH REGION
fitness_of_regions = {}

for region in dict_regions:
        
    region_graph = {}
    count_states = 0
    print("Processing Region",region)
    for state in dict_regions[region]:
        count_states += 1
        region_graph[state] = graph[state]
    
    # variables for Evolution object
    fitness = tsp_fitness_creator()
    n_cities = count_states
    cities_list = dict_regions[region]
    dist_center = distribution_center[region]
    cities_list.remove(dist_center)                                             # remove the distribution center from the list of cities that will be generated
                                                                                # so the dist_center be always in the first position

    # evo is a object of type Evolution (class)
    evo = Evolution(
        pool_size=100, fitness=fitness, individual_class=TSP, n_offsprings=30,
        crossover_params={'rate': 0},                                           # this will be randomly generated for each generation                            
        mutate_params={'rate': 1},
        init_params={'n_cities': n_cities, 'dist_center': dist_center},
        cities_list = cities_list
    )
    n_epochs = 100                                                              # number of generations

    hist = []
    
    # Each generation is calculated here
    for i in range(n_epochs):
        pool = evo.pool                                                         # variable with pool of individuals
        hist.append(pool.fitness(pool.individuals[-1]))                         # call the fitness function, to calculate the best value for the best path, and append on hist
        evo.step()
    
    best_fitness = evo.pool.fitness(evo.pool.individuals[-1])
    fitness_of_regions[dist_center]= (best_fitness * (-1))                       # fitness_of_regions save best answer for each region

    print("Order: ", evo.pool.individuals[-1].value)
    print("Fitness: ", best_fitness)
    
    
    # PLOTING
    title = region + ": " + str(best_fitness*-1) + " minutes"
    plt.title(title)
    plt.xlabel("Number of Generations")
    plt.ylabel("Fitness Value (minutes)")
    plt.plot(hist)
    plt.show()
    
    
print("Best fitness of each region: ", fitness_of_regions)

# CALCULATE BEST ORDER FOR SÃO PAULO TO DISTRIBUTE FOR EACH REGION
# Distribution of each region is made parallel, so it must find which region should send the doses first

# create graph from SP to each distribution center
# we must have 4 equations, we must have t1 t2 t3 t4 -> time to travel to each region

region_time_to_travel = []
for region, dist in distribution_center.items():
    if dist != "SP":
        region_time_to_travel.append((dist, dict_travel_time[("SP", dist)]))

best_answer = 10e10
constants = [(1,0,0,0), 
             (2,1,0,0), 
             (2,2,1,0), 
             (2,2,2,1)]

equations = []

all_possibilities = permutations(region_time_to_travel)

for center in list(all_possibilities):
    equations.clear()
    for i in range(4):
        eq = fitness_of_regions[center[i][0]] + constants[i][0]* center[0][1] + constants[i][1]* center[1][1] + constants[i][2]* center[2][1] + constants[i][3]* center[3][1]
        equations.append(eq)                                            # each permutation get 4 equations, one for each region
    
    longest_trip = max(equations)                                       # answer is the value for the region with longest time because it's a parallel distribution
    best_answer = min(best_answer, longest_trip)                        # from each permutation, check if a better answer was found
    

print("\n\n\nBest answer: ", best_answer)


