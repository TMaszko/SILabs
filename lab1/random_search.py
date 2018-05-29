import numpy as np
import  matplotlib.pyplot as plt
from individual import generate_random_individual
from cost import calculate_individual_cost


def random_search(gen, size, distances, flows):
    bests = []
    best = generate_random_individual(size)
    best_cost = calculate_individual_cost(best, distances, flows)
    bests.append(best_cost)
    for _ in range(1, gen):
        current = generate_random_individual(size)
        current_cost = calculate_individual_cost(current, distances, flows)
        if current_cost < best_cost:
            best = current
            best_cost = current_cost
        bests.append(best_cost)
    #
    plt.plot(np.arange(gen), bests, label="Best")
    plt.show()

