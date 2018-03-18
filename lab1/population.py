from individual import generate_random_individual


def generate_init_population(amount, size):
    result = [generate_random_individual(size) for _ in range(amount)]
    return result
