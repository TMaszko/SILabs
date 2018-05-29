from random import randint, random
from cost import calculate_population_cost


def tournament(population, population_costs, size):
    participants_costs = [population_costs[randint(0, size-1)] for _ in range(size)]
    print(participants_costs)
    print(str(population_costs))
    best_cost = min(participants_costs)
    print('index' + str(participants_costs.index(best_cost)))
    print('best_cost: ' + str(best_cost))
    print('winner' + str(population[participants_costs.index(best_cost)]))
    return population[population_costs.index(best_cost)]

def roulette(population, population_costs):
    inverted_population_costs = [1/cost for cost in population_costs]
    total_population_cost = sum(inverted_population_costs)
    print(total_population_cost)
    intervals = []
    selected_individuals = []
    last_cost = 0
    for cost in inverted_population_costs:
        print('cost' + str(1/cost))
        ratio = (cost + last_cost)/total_population_cost
        last_cost = cost + last_cost
        intervals.append(ratio)
    print('intervals: ' + str(intervals))
    for _ in population:
        trail_ratio = random()
        i = 0
        while intervals[i] < trail_ratio:
            i += 1
        selected_individuals.append(population[i])
    return selected_individuals
