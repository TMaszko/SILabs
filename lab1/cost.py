import numpy as np


def calculate_population_cost(distances, flows, population, invert=False):
    return [1/calculate_individual_cost(individual, distances, flows) if invert
            else calculate_individual_cost(individual, distances, flows)
            for individual in population]



def calculate_partial_cost(facility, facility_localization, individual, distances, flows):
    localizations_to_process = range(facility_localization, len(individual))
    # for loc in localizations_to_process:
        # print('localizaation to process ' + str(loc))
    return sum([
            calculate_one_relation_cost(
                distance_between_two_localizations(facility_localization, localization, distances),
                flow_between_two_localizations(facility, individual[localization], flows))
            for localization in localizations_to_process
    ])

def calculate_one_relation_cost(calculated_distances, calculated_flows):
    return sum([dist * calculated_flows[i] for i, dist in enumerate(calculated_distances)])


def calculate_individual_cost(individual, distances, flows):
    # print('individual: ' + str(individual))
    return sum([
        calculate_partial_cost(facility, localization, individual, distances, flows) # nie bedzie bral samego siebie
        for localization, facility in enumerate(individual)
    ])





def value_of_relation_between_two_localization(value_index, value2_index, relations):

    return relations[value_index][value2_index], relations[value2_index][value_index]

def flow_between_two_localizations(facility_index, facility2_index, flows):
    result = value_of_relation_between_two_localization(facility_index, facility2_index,flows)
    # print('flow: (' + str(facility_index) + ', ' + str(facility2_index) + ') :' + str(result))
    return result


def distance_between_two_localizations(localization_index, localization2_index, distances):
    result = value_of_relation_between_two_localization(localization_index, localization2_index, distances)
    # print('distance: (' + str(localization_index) + ', ' + str(localization2_index) + ')' + str(result))
    return result
