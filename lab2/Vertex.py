class Vertex:
    def __init__(self, no, neighbours, variable):
        self.no = no
        self.neighbours = neighbours
        self.variable = variable
        self.constraints = None

    def __str__(self):
        return "Vertex number: " + str(self.no) + " Neighbours: " + str(self.neighbours) + ' Variable: ' + str(
            self.variable)

    def __repr__(self):
        return "Vertex number: " + str(self.no) + " Neighbours: " + str(self.neighbours) + ' Variable: ' + str(
            self.variable)

    def check_constraints(self, graph):
            return self.constraints.check(self,
                                          [graph[neighbour_no].variable.value for neighbour_no in self.neighbours],
                                          graph)
