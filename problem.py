import numpy as np
from initiator import TransportationInitiator, LeastCostInitiator
from optimizer import TransportationOptimizer
from result import TransportationResult


class TransportationProblem:

    def __init__(self, supply, demand, costs):
        self.supply = supply
        self.demand = demand
        self.costs  = np.array(costs)
        # self.result = np.zeros_like(costs)

        self.__pre_processing()

    def __pre_processing(self):
        supp_total = np.sum(self.supply)

        try:
            new_wh_nums = len(tuple(filter(lambda x: x is None, self.demand)))

            i = 1
            while i <= new_wh_nums:
                self.demand[-i] = supp_total
                i += 1

            self.supply.append(np.sum(self.demand) - supp_total)
            self.costs = np.vstack((self.costs, np.zeros_like(self.demand)))
        except Exception as e:
            raise e

    def solve(self, initiator_class=LeastCostInitiator, optimizer_class=TransportationOptimizer):
        assert issubclass(initiator_class, TransportationInitiator)

        try:
            initiator = initiator_class(self.supply, self.demand, self.costs)
            opt = optimizer_class(self.supply, self.demand, self.costs, x0=initiator.initial_result)

            is_best = opt.optimize()
            while not is_best:
                is_best = opt.optimize()

            return opt.result
        except Exception as e:
            raise e


# TEST CASES

tp = TransportationProblem([80, 110, 90], [85, 75, None, None, None],     # "None" means new warehouse need to build
                           [[8, 2, 5, 4, 3], [7, 5, 6, 8, 9], [1, 3, 7, 5, 2]])
result = tp.solve(LeastCostInitiator)
print(result)
