from Dictionaries import *                                      # import dictionary for graph
from Graph import build_graph, show_graph, find_edge_weight     # import functions to create and show graph            
from EA import Evolution                                        # to run evolutionary algorithm
from TSP import TSP                                             # to create specific evolutionary parameters for TSP
from Plotting import plot_hist, plot_graph, plot_show           # to plot with mathplotlib
from itertools import permutations                              # to create permutations
from math import inf                                            # use  INF 'number'

# FIND THE FITNESS FOR EACH INDIVIUAL (FEASIBLE SOLUTION)
def fitness(tsp):
    res = 0
    for i in range(len(tsp.value)):
        state_a = tsp.value[i]                                                   # tsp.value is number of states
        state_b = tsp.value[i + 1]     if i+1 < len(tsp.value) else tsp.value[0]
        
        res += find_edge_weight(state_a, state_b)                                 # Fitness of each individual is calculates based on the sum of all nodes connected in this specific path

    return res


################################## MAIN #############################
'''
    # MAIN is divided into two parts
    #   > Run evolutionary algorithm and find best path for each region
    #   > Calculate and find the best distribution order from SP to each region
    # Finally present the final answer: minimum time to make the distribution in whole Brazil
'''

        # PART 1

# CREATE GRAPH FOR BRAZIL
graph = build_graph()                                                           # to change the graph, one must change info in Dictionaries.py


# CALCULATE BEST PATH FOR EACH REGION
fitness_of_regions = {}
legend = []
for region in dict_regions:
    print("Processing Region",region)

    # CREATE PARTIAL GRAPH AND COUNT STATES
    region_graph = {}                                                           # partial graph
    count_states = 0                                                            # count how many states there are inside that region
    
    for state in dict_regions[region]:
        region_graph[state] = graph[state]                                      # save only the edges from states inside that region
        count_states += 1


    # SET VARIABLES FOR EVOLUTION CLASS
    fitness_func_address = fitness                                              # get the memory address in which the fitness function can be reached
    n_cities = count_states
    cities_list = dict_regions[region]
    dist_center = distribution_center[region]
    

    # REMOVE THE DISTRIBUTION CENTER FROM LIST THAT WILL BE RANDOMLY GENERATED
    cities_list.remove(dist_center)                                             
                                                                            

    # CREATE EVO OBJECT, CLASS EVOLUTION AND SET PARAMETERS
    evo = Evolution(
        pool_size=100, fitness=fitness, individual_class=TSP, n_offsprings=30,
        crossover_params={'single_point': 0},                                   # this will be randomly generated for each individual                           
        mutate_params={'rate': 1},
        init_params={'n_cities': n_cities, 'dist_center': dist_center},
        cities_list = cities_list
    )
    n_epochs = 100                                                              # number of generations

    # RUN EA FOR EACH GENERATION
    hist = []                                                                   # save values of the fittest invidual of each generation

    for i in range(n_epochs):
        pool = evo.pool                                                         # variable with pool of individuals
        
        hist.append(pool.fitness(pool.individuals[0]))                          # call the fitness function, to calculate the best value for the best individual, and append on hist
        evo.step()                                                              # step method call for reproduction, crossover, mutation and selection
    
    best_fitness = evo.pool.fitness(evo.pool.individuals[0])
    fitness_of_regions[dist_center]= best_fitness                               # fitness_of_regions save best answer for each region

    print("Order: ", evo.pool.individuals[0].value)
    
    # PLOTTING
    plt = plot_hist(region=region, best_fitness=best_fitness, hist=hist)
    legend.append(region + " " + str(best_fitness) +" minutes")

plt.legend(legend)
plot_show(plt)
    
    
print("Best fitness of each region: ", fitness_of_regions)


        # PART 2


# CALCULATE BEST ORDER FOR SÃO PAULO TO DISTRIBUTE FOR EACH REGION AND FIND FINAL ANSWER
'''
        # Distribution of each region is made parallel, 
        # so it must find to which region, the plane should send the doses first
        # 1. create graph from SP to each distribution center
        # 2. we must have 4 equations, we must have t1 t2 t3 t4 -> time to travel to each region
'''


# CREATE A TUPLE (DISTRIBUTION_CENTER, TIME_FROM_SP_TO_DIST_CENTER)
region_time_to_travel = []
for _, dist in distribution_center.items():
    if dist != "SP":
        region_time_to_travel.append((dist, dict_travel_time[("SP", dist)]))

# CREATE FOUR EQUATIONS THAT REPRESENT THE TIME FOR THE VACCINE LEAVE FROM SP AND BE DISTRIBUTED TO EVERY STATE INSIDE EACH REGION
equations = []
best_answer = inf                                                                   # inf from math library
constants = [(1,0,0,0),                                                             # constants for each equation
             (2,1,0,0), 
             (2,2,1,0), 
             (2,2,2,1)]

all_orders_possibilities = permutations(region_time_to_travel)                      # try all 4! possibilities of order for SP to distribution to each region


# FOR EACH ORDER OF DISTRIBUTION, FIND THE EQUATIONS FOR THAT ORDER AND GET THE BEST ANSWER FROM ALL POSSIBILITIES
for region_order in list(all_orders_possibilities):                                 #  each region_order is an array of TUPLE (DISTRIBUTION_CENTER, TIME_FROM_SP_TO_DIST_CENTER)
    equations.clear()
    for i in range(4):
        eq = fitness_of_regions[region_order[i][0]] + constants[i][0]* region_order[0][1] + \
                                                      constants[i][1]* region_order[1][1] + \
                                                      constants[i][2]* region_order[2][1] + \
                                                      constants[i][3]* region_order[3][1]

        equations.append(eq)                                                        # each permutation get 4 equations, one for each region
    
    equations.append(fitness_of_regions["SP"])                                      # append the time to distribute inside SP's region, since this is done with another airplane and it is already in SP
    longest_trip = max(equations)                                                   # answer is one of the 5 equations, the value for the region with longest time because it's a parallel distribution                      
    
    # save order that SP will make the distribution
    if longest_trip < best_answer:
        best_answer = longest_trip                                                  # from each permutation, check if a better answer was found
        order_of_distribution = region_order

# FINAL ANSWER
print("\n\n\nPath from SP to centers: ", order_of_distribution)
print("\n\n\nBest answer: ", best_answer)


