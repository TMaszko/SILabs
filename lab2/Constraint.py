class Constraint:
    def __init__(self, check_fn):
        self.check_fn = check_fn

    def check(self, *args):
        return self.check_fn(*args)