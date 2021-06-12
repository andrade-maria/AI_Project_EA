from EA import Individual       # import other files in this folder
import numpy as np              # numpy to deal with arrays
import copy                     # to make copy of strings

class TSP(Individual):

    # CROSSOVER FUNCTION
    def crossover(parent1, parent2, crossover_params, init_params):
        
        # generate random crossover single point
        crossover_params['single_point'] = np.random.uniform(low = 1, high = 9)/10.0                                                    # for each individual a number will be randomly generated between 0.1 and 0.9 to act as crossover single point
        
        try: 
            parent1_head = copy.copy(parent1.value[:int(len(parent1.value) * crossover_params['single_point'])])                        # parent1_head is the first part of the parent1 
            parent1_tail = copy.copy(parent1.value[int(len(parent1.value) * crossover_params['single_point']):init_params['n_cities']]) # parent1_tail is the second part of the parent1
            parent2_tail = copy.copy(parent2.value[int(len(parent2.value) * crossover_params['single_point']):])                        # parent2_tail is the second part of the parent2
            
            mapping = {parent2_tail[i]: parent1_tail[i] for i in range(len(parent1_tail))}                                              # dictionary comprehension

            for i in range(len(parent1_head)):                                                      
                while parent1_head[i] in parent2_tail:                                                                                  # change all occurrencies which are repeated on the tail
                    parent1_head[i] = mapping[parent1_head[i]]                                                                          # keep changing the same position until is not repeated anymore
        except:
            print("parent1_head: ", parent1_head)
            print("parent1_tail: ", parent1_tail)
            print("parent2_tail: ", parent2_tail)
            print("Mapping: ", mapping)

        return TSP(np.hstack([parent1_head, parent2_tail]))                                                                     # put two arrays together parent1 + parent2, hstack stands to horizontally stack

    # MUTATION FUNTCION
    def mutation(self, mutate_params):
        for _ in range(mutate_params['rate']):                                                                                  # mutate only one time per chromosome
            i, j = np.random.choice(range(1, len(self.value)), 2, replace=False)                                                # can be the same position -> it won't mutate at all, range starts at 1, because dist_center can't leave the first place
            self.value[i], self.value[j] = self.value[j], self.value[i]

    # Generates a random array by changing places of cities
    def _random_init(self, cities_list, init_params):
        return np.random.choice(cities_list, size= init_params['n_cities']-1, replace=False)                                    # size is one smaller because dist_center is out                
        
        # np.random.choice returns the list at random order, replace must be false, so it does not choose same city twice