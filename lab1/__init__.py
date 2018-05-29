import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import random, choice
from population import generate_init_population
from cost import calculate_individual_cost, calculate_population_cost
from selection import tournament, roulette
from individual import crossover, mutate_individual
from random_search import random_search


def read_file(path):
    with open(path) as f:
        data = pd.DataFrame([row.rstrip().split() for row in f]).get_values()
        # rozmiar data[0][0] , 1sza macierz [2:rozmiar+2], 2macierz [rozmiar+3:] (do konca)
        size = int(data[0][0])
        distances = np.asarray(data[2:(size + 2)], dtype=int)
        flows = np.asarray(data[(size + 3):], dtype=int)

        return {
            'size': size,
            'flows': flows,
            'distances': distances
        }


# print(read_file('data/test.dat'))


def test():
    config = read_file("data/test.dat")
    print(config)
    # print(calculate_individual_cost([2, 3, 0, 1], config['distances'], config['flows']))
    init_pop = generate_init_population(10, 4)
    # after = []
    # print('init: ' + str(init_pop))
    # for _ in range(10) :
    #     after.append(tournament(init_pop,
    #                             calculate_population_cost(config['distances'], config['flows'], init_pop), 3))
    # print('after' + str(after))
    print(roulette(generate_init_population(10, 4), config['distances'], config['flows']))
    # print(crossover([1,2,3,4], [4,3,2,1]))


# test()



def run():
    p_cross = 0.7
    p_mutation = 0.01
    config = read_file('data/had12.dat')
    distances = config['distances']
    flows = config['flows']
    individual_size = config['size']
    new_population = []
    population_size = 100
    tour_size = 5
    num_of_gen = 100
    result_matrix = np.zeros((4, num_of_gen, 5))
    print(result_matrix)
    for e in range(5):
        current_population = generate_init_population(population_size, individual_size)
        current_population_costs = calculate_population_cost(distances, flows, current_population)
        result_matrix[:,0,e] = ([0, min(current_population_costs), np.average(current_population_costs),
                             max(current_population_costs)])
        print('poczatek fora')
        for gen in range(1, num_of_gen):
            print('current' + str(current_population))
            for _ in range(population_size):
                new_population.append(tournament(current_population, current_population_costs, tour_size))
            print('after tournamtent' + str(new_population))
            # new_population = roulette(current_population, current_population_costs)
            new_population = [
                crossover(individual_parent, choice(new_population)) if random() <= p_cross else individual_parent
                for individual_parent in new_population
            ]
            print('after crossover: ' + str(new_population))
            new_population = [mutate_individual(indiv) if random() <= p_mutation else indiv for indiv in new_population]
            current_population = new_population
            new_population = []
            current_population_costs = calculate_population_cost(distances, flows, current_population)
            print('gen' + str(gen))
            result_matrix[:, gen, e] = ([gen, min(current_population_costs),
                                   np.average(current_population_costs), max(current_population_costs)
                                   ])
            print('generation ' + str(gen))

    plt.xlabel('Generations')
    plt.ylabel('Costs')
    plt.errorbar(np.arange(num_of_gen),  np.average(result_matrix[1, :, :], axis=1),  np.std(result_matrix[1, :, :], axis=1), fmt='-o', label="Best")
    plt.errorbar(np.arange(num_of_gen), np.average(result_matrix[2, :, :], axis=1), np.std(result_matrix[2, :, :], axis=1), fmt='-o', label="Avg")
    plt.errorbar(np.arange(num_of_gen), np.average(result_matrix[3, :, :], axis=1), np.std(result_matrix[3, :, :], axis=1), fmt='-o', label="Worst")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=4, borderaxespad=0.)
    plt.show()
    random_search(num_of_gen, individual_size, distances, flows)


run()