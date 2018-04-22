import numpy as np

import math
from datetime import datetime as date
from CSPBacktrack import CSPBacktrack
from Constraint import Constraint
from Variable import Variable
from Vertex import Vertex


def create_graph_from_square_matrix(size):
    num_vertex = size * size
    vertex_matrix = np.arange(num_vertex).reshape(size, size)
    return [
        Vertex(
            vertex_no,
            [
                neighbour for neighbour in
                np.concatenate((
                    vertex_matrix[math.floor(vertex_no / size)],
                    vertex_matrix[:, vertex_no % size]))
                if neighbour != vertex_no
            ],
            Variable(np.arange(size))
        ) for vertex_no in range(num_vertex)
    ]


def create_graph_for_queens(size):
    domain = np.arange(size)
    return [Vertex(x, [vertex_no for vertex_no in domain if vertex_no != x], Variable(domain)) for x in domain]


def get_all_diagonal_neighbours(vertex_matrix):
    first_diag = get_all_diagonals_from_matrix(vertex_matrix)
    sec_diag = get_all_diagonals_from_matrix(np.fliplr(vertex_matrix))
    return np.concatenate((first_diag, sec_diag))


def find_neighbour_of_vertex(vertex_no, lists_neighbours):
    return np.array(flatten([neighbours for neighbours in lists_neighbours if vertex_no in neighbours]), dtype=np.int32)


def flatten(list_neigh):
    if len(list_neigh) == 0:
        return []
    else:
        return np.concatenate((list_neigh[0], flatten(list_neigh[1:])))


def filter_vertex_from_neighbours(vertex_no, neighbours):
    return [neigh for neigh in neighbours if neigh != vertex_no]


def get_all_diagonals_from_matrix(matrix):
    size = len(matrix)
    return [np.diag(matrix, offset) for offset in range(-(size - 1), size)]


def create_constraints_edges_squares():
    return Constraint(lambda v, neigh_list , graph: v.variable.value not in neigh_list)

def create_constraint_queens():
    return Constraint(constraint_queens)

def add_constraints_to_graph(graph, create_constraints_edges_fn):
    for node in graph:
        node.constraints = create_constraints_edges_fn()


def constraint_queens(vertex, neighbours, graph):
    neighbour_vertices = [graph[neigh] for neigh in vertex.neighbours]
    # print(neighbour_vertices)
    return len([neighbour_vertex for neighbour_vertex in neighbour_vertices if
                neighbour_vertex.variable.value is not None and (neighbour_vertex.variable.value == vertex.variable.value or
                int(math.fabs(neighbour_vertex.no - vertex.no)) == int(
                    math.fabs(vertex.variable.value - neighbour_vertex.variable.value)))
                ]) == 0


graph = create_graph_for_queens(10)
# graph = create_graph_from_square_matrix(4)

for i in graph:
    print(i)

# add_constraints_to_graph(graph, create_constraints_edges_squares)
# #
csp = CSPBacktrack(graph)
# #

add_constraints_to_graph(graph, create_constraint_queens)
start_time = date.now()
csp.solve(0, start_time)
print(csp.counter)
print(csp.backtrack_count)
print((date.now() - start_time).microseconds)
