class Variable:
    def __init__(self, domain):
        self.domain = domain
        self.value = None

    def __str__(self):
        return "Value: " + str(self.value) + " Domain: " + str(self.domain)

    def __repr__(self):
        return "Value: " + str(self.value) + " Domain: " + str(self.domain)


