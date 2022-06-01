import numpy as np
from copy import deepcopy


class TransportationInitiator:

    def __init__(self, supply, demand, costs):
        self.supply = deepcopy(supply)
        self.demand = deepcopy(demand)
        self.costs  = deepcopy(costs)

        self.initial_result = np.zeros_like(costs)
        self._init_result()

    def _init_result(self):
        return self.initial_result


class LeastCostInitiator(TransportationInitiator):
    
    def __init__(self, supply, demand, costs):
        super(LeastCostInitiator, self).__init__(supply, demand, costs)

    def _max_coordinates(self):
        min_indices = np.argwhere(self.costs == np.amin(self.costs))
        candidates  = {
            str(tup): np.min([self.supply[tup[0]], self.demand[tup[1]]]) for tup in min_indices
        }
        selection = max(candidates, key=candidates.get)
        return int(selection[1]), int(selection[3]), int(candidates.get(selection))

    def _init_result(self):
        m = len(self.supply)
        n = len(self.demand)
        threshold = 99999999

        i = 0
        while i < m+n-1:
            x, y, val = self._max_coordinates()

            if self.supply[x] - val == 0:
                self.costs[x, :] = threshold
                self.supply[x]  = threshold
                self.demand[y] -= val
            else:
                self.costs[:, y]   = threshold
                self.demand[y]  = threshold
                self.supply[x] -= val

            self.initial_result[x, y] = val
            i += 1
        return self.initial_result

#
# init_tp = LeastCostInitiator([80,110,90,440],[85,75,280,280],
#                                   [[8,2,5,4],[7,5,6,8],[1,3,7,5],[0,0,0,0]])
# res = init_tp.init_result()
# print(res)
