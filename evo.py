import numpy as np                      # numpy to deal with arrays
from abc import ABC, abstractmethod     #


class Individual(ABC):
    def __init__(self, value=None, init_params=None, cities_list=None):
        if value is not None:
            self.value = value
        else:
            self.value = self._random_init(cities_list, init_params)
            self.value = np.insert(self.value, 0, init_params['dist_center'])

    @abstractmethod
    def crossover(self, other, crossover_params, init_params):
        pass

    @abstractmethod
    def mutation(self, mutate_params):
        pass

    @abstractmethod
    def _random_init(self, cities_list, init_params):
        pass


class Optimization(Individual):
    def pair(self, other, crossover_params):
        return Optimization(crossover_params['rate'] * self.value + (1 - crossover_params['rate']) * other.value)

    def mutate(self, mutate_params):
        self.value += np.random.normal(0, mutate_params['rate'], mutate_params['dim'])
        for i in range(len(self.value)):
            if self.value[i] < mutate_params['lower_bound']:
                self.value[i] = mutate_params['lower_bound']
            elif self.value[i] > mutate_params['upper_bound']:
                self.value[i] = mutate_params['upper_bound']

    def _random_init(self, init_params):
        return np.random.uniform(init_params['lower_bound'], init_params['upper_bound'], init_params['dim'])


class Population:
    # Constructor method, called when initialized
    def __init__(self, size, fitness, individual_class, init_params, cities_list):
        #define each characteristic of the self (kind of struct)
        self.fitness = fitness                                                      # fitness function is called several times
        self.individuals = [individual_class(cities_list = cities_list, init_params = init_params) for _ in range(size)]
        self.individuals.sort(key=lambda x: self.fitness(x))

    def replace(self, new_individuals):
        size = len(self.individuals)
        self.individuals.extend(new_individuals)
        self.individuals.sort(key=lambda x: self.fitness(x))
        self.individuals = self.individuals[-size:]                                 # throwing out 30 individuals, and including the best offsprings

    def get_parents(self, n_offsprings):
        mothers = self.individuals[-2 * n_offsprings::2]                            # mothers are even
        fathers = self.individuals[-2 * n_offsprings + 1::2]                        # fathers are odds

        return mothers, fathers


class Evolution:
    # Constructor method, called when initialized
    def __init__(self, pool_size, fitness, individual_class, n_offsprings, crossover_params, mutate_params, init_params, cities_list):
        
        #define each characteristic of the self (kind of struct)
        self.crossover_params = crossover_params
        self.mutate_params = mutate_params

        # pool is a gene pool -> population of feasible solutions
        self.pool = Population(pool_size, fitness, individual_class, init_params, cities_list)
        self.n_offsprings = n_offsprings
        self.cities_list = cities_list
        self.init_params = init_params

    def step(self):
        mothers, fathers = self.pool.get_parents(self.n_offsprings)
        offsprings = []

        for mother, father in zip(mothers, fathers):
            offspring = mother.crossover(father, self.crossover_params, self.init_params)
            offspring.mutation(self.mutate_params)
            offsprings.append(offspring)

        self.pool.replace(offsprings)