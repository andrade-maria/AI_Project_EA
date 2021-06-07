from evo import Individual      # import other files in this folder
import numpy as np              # numpy to deal with arrays
import copy                     # to make copy of strings

class TSP(Individual):

    # CROSSOVER FUNCTION
    def crossover(self, other, crossover_params, init_params):

        # value is a list of cities, which is given by X and Y
        crossover_params['rate'] = np.random.uniform(low = 1, high = 9)/10.0                                                    # for each individual it will be randomly generated a number between 0.1 and 0.9 to act as crossover single point
        try: 
            parent1_head = copy.copy(self.value[:int(len(self.value) * crossover_params['rate'])])                              # parent1_head is the first part of the parent1 
            parent1_tail = copy.copy(self.value[int(len(self.value) * crossover_params['rate']):init_params['n_cities']])       # parent1_tail is the second part of the parent1
            parent2_tail = copy.copy(other.value[int(len(other.value) * crossover_params['rate']):])                            # parent2_tail is the second part of the parent2
            
            mapping = {parent2_tail[i]: parent1_tail[i] for i in range(len(parent1_tail))}                                      # dictionary comprehension

            for i in range(len(parent1_head)):                                                      
                while parent1_head[i] in parent2_tail:                                                                          # change all occurrencies which are repeated on the tail
                    parent1_head[i] = mapping[parent1_head[i]]                                                                  # keep changing the same position until is not repeated anymore
        except:
            print("parent1_head: ", parent1_head)
            print("parent1_tail: ", parent1_tail)
            print("parent2_tail: ", parent2_tail)
            print("Mapping: ", mapping)

        return TSP(np.hstack([parent1_head, parent2_tail]))                                                                     # put two arrays together parent1 + parent2, hstack stands to horizontally stack

    # MUTATION FUNTCION
    def mutation(self, mutate_params):
        for _ in range(mutate_params['rate']):                                                                                  # mutate only one time per chromosome
            i, j = np.random.choice(range(1, len(self.value)), 2, replace=False)                                                # can be the same position -> it won't mutate at all, range start at 1, because dist_center can't leave the first place
            self.value[i], self.value[j] = self.value[j], self.value[i]

    # Generates a random array changing places of cities
    def _random_init(self, cities_list, init_params):
        return np.random.choice(cities_list, size= init_params['n_cities']-1, replace=False)                                    # size is one smaller because dist_center is out                
        
        # np.random.choice returns the list in random order, replace must be false, so it does not choose same city twice