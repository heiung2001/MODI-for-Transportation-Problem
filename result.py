from problem import TransportationProblem


class TransportationResult:
    """
    This class is to help handle the output of the Transportation Problem!
    """
    def __init__(self, problem: TransportationProblem, best_solution):
        self.problem = problem
        self.best_solution = best_solution

    def __str__(self):
        pass
