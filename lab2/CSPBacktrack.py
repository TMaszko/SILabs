import numpy as np
import math

from datetime import datetime


class CSPBacktrack:
    def __init__(self, graph):
        self.graph = graph
        self.counter = 0
        self.backtrack_count = 0

    def solve(self, starting_vertex_no,first_time):
        if starting_vertex_no is None:
            self.counter += 1
            if self.counter == 1:
                print((datetime.now() - first_time).microseconds)
            # self.print_csp()
            # print('===============================================')
            return
        else:
            vertex = self.graph[starting_vertex_no]
            domain = vertex.variable.domain
            # np.random.shuffle(domain)
            for possible_value in  domain:
                vertex.variable.value = possible_value
                is_assignment_possible = vertex.check_constraints(self.graph)
                if is_assignment_possible:
                    # entangled_variables = [self.graph[vertex_no].variable for vertex_no in vertex.neighbours]
                    # saved_domains = [variable.domain for variable in entangled_variables]
                    # self.cut_domain(entangled_variables, [possible_value])
                    # self.cut_domain_queens(vertex)
                    # print('current state ')
                    # self.print_csp()
                    # print('----------------------------------------------')
                    # self.solve(self.mrv_heuristic(self.graph, starting_vertex_no),first_time)
                    self.solve(starting_vertex_no + 1 if starting_vertex_no + 1 < len(self.graph) else None,first_time)
                    # self.return_domain(entangled_variables, saved_domains)
                self.backtrack_count += 1
            vertex.variable.value = None

    # def solve_queens(self,starting_vertex_no, remaining_queens):
    #     # print(starting_vertex_no)
    #     if starting_vertex_no is None:
    #         if remaining_queens == 0:
    #             self.counter += 1
    #         return
    #     else:
    #         if remaining_queens == 0:
    #             self.counter += 1
    #             # self.print_csp()
    #             return
    #
    #         for vertex_no in range(starting_vertex_no, len(self.graph)):
    #             # print(vertex_no)
    #             vertex = self.graph[vertex_no]
    #             vertex.variable.value = 1
    #             is_assignment_possible = vertex.check_constraints(self.graph)
    #             if is_assignment_possible:
    #                 # print(vertex_no)
    #                 self.solve_queens(vertex_no + 1 if vertex_no + 1 < len(self.graph) else None, remaining_queens - 1)
    #             vertex.variable.value = None

    def mrv_heuristic(self, graph, current_vertex):
        available_vertices = [vertex for vertex in graph if
                              vertex.no != current_vertex and vertex.variable.value is None]
        if len(available_vertices) > 0:
            min_domain_index_in_available_vertices = np.argmin(
                [len(vertex.variable.domain) for vertex in available_vertices])
            # print(min_domain_index_in_available_vertices)
            return available_vertices[min_domain_index_in_available_vertices].no
        else:
            return None

    def print_csp(self):
        size = math.floor(math.sqrt(len(self.graph)))
        print(np.array([vertex.variable.value for vertex in self.graph]).reshape([size, size]))

        print(self.counter)
        print(self.backtrack_count)

    def cut_domain(self, entangled_variables, values_to_cut):
        for variable in entangled_variables:
            variable.domain = [value_domain for value_domain in variable.domain if value_domain not in values_to_cut]

    def return_domain(self, entangled_variables, domains_to_return):
        for (i, variable) in enumerate(entangled_variables):
            variable.domain = domains_to_return[i]

    def cut_domain_queens(self, vertex):
        neighbours = vertex.neighbours
        neighbours_vertices = [self.graph[neigh] for neigh in neighbours]
        for neigh_vertex in neighbours_vertices:
            if neigh_vertex.variable.value is None:
                neigh_vertex.variable.domain = [value for value in neigh_vertex.variable.domain if
                                                (value != vertex.variable.value
                                                 and int(math.fabs(neigh_vertex.no - vertex.no)) != int(
                                                            math.fabs(
                                                                vertex.variable.value - value)))]
