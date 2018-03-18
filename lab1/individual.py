import numpy as np
from random import randint


def generate_random_individual(size):
    a = np.arange(size)
    np.random.shuffle(a)
    return a


def mutate_individual(individual):
    all_localizations_to_draw = range(0, len(individual))
    localization1_to_swap = randint(0,len(all_localizations_to_draw) - 1)
    localizations_after_first_draw = [pos for idx, pos in enumerate(all_localizations_to_draw)
                                      if idx != localization1_to_swap ]
    localization2_to_swap = randint(0,len(localizations_after_first_draw) - 1)
    swap_gens(localization1_to_swap, localization2_to_swap, individual)
    return individual


def swap_gens(index1,index2, arr):
    temp = arr[index1]
    arr[index1] = arr[index2]
    arr[index2] = temp


def crossover(parent_1, parent_2):
    parent_1_part = randint(1, len(parent_1)-2)
    child_part_1 = parent_1[:parent_1_part]
    child_part_2 = [gen for gen in np.concatenate((parent_2[parent_1_part:], parent_2[:parent_1_part])) if gen not in child_part_1]
    child = np.concatenate((child_part_1, child_part_2))
    return child

