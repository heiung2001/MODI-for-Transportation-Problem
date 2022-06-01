import numpy as np
from map import Map


class TransportationOptimizer:

    def __init__(self, supply, demand, costs: np.array, x0: np.array):
        self.supply = supply
        self.demand = demand
        self.costs = costs
        self.x0 = x0
        self.result = None

        self.g = np.argwhere(x0 > 0)
        self.not_g = np.argwhere(x0 == 0)

        # maybe don't need these
        self.uv_costs = None
        self.uv_coefs = None
        self.delta = None

    def _get_uv(self):
        m = len(self.supply)
        n = len(self.demand)

        coors = []
        for i, tup in enumerate(self.g):
            coors.extend([[i, tup[0]], [i, tup[1] + m]])
        equation_matrix = np.zeros((m + n - 1, m + n))
        equation_matrix[tuple(np.array(coors).T)] = 1  # don't know why it works :D
        equation_matrix = np.delete(equation_matrix, 0, axis=1)

        uv_flat_idxs = [self.g[i, 0] * n + self.g[i, 1] for i in range(len(self.g))]
        uv_costs = np.take(self.costs.flatten(), uv_flat_idxs)

        uv_coefs = np.insert(np.array(np.linalg.inv(equation_matrix).dot(uv_costs), dtype=np.int64), 0, 0)
        return uv_coefs

    def _get_delta(self):
        m = len(self.supply)
        n = len(self.demand)

        uv_flat_idxs = [self.not_g[i, 0] * n + self.not_g[i, 1] for i in range(len(self.not_g))]
        uv_costs = np.take(self.costs.flatten(), uv_flat_idxs)

        delta = np.zeros_like(self.costs)
        delta[tuple(self.not_g.T)] = [
            self.uv_coefs[self.not_g[i, 0]] + self.uv_coefs[self.not_g[i, 1] + m] - uv_costs[i]
            for i in range(len(self.not_g))]
        return delta

    def optimize(self):     # only one best solution can be found!
        self.uv_coefs = self._get_uv()
        self.delta = self._get_delta()

        positive_delta = np.argwhere(self.delta > 0)
        if len(positive_delta) == 0:
            self.result = self.x0
            return True

        adjust_cell = np.argwhere(self.delta == np.max(self.delta))[0]     # maybe have more than one that reach max
        adjust_cycle = Map(self.g.tolist(), adjust_cell.tolist()).search_for_cycle()

        sub_set = [cell for idx, cell in enumerate(adjust_cycle) if idx % 2 != 0]
        add_set = [cell for idx, cell in enumerate(adjust_cycle) if idx % 2 == 0]
        discard_cell, theta = self.__improve_solution(sub_set, add_set)

        for idx in range(len(self.g)):
            if np.array_equal(self.g[idx], discard_cell):
                self.g[idx] = adjust_cell

        return False

    def __improve_solution(self, sub_set, add_set):
        candidates = self.x0[tuple(np.array(sub_set).T)]

        minimal = np.min(candidates)
        minimal_idx = np.argmin(candidates)

        self.x0[tuple(np.array(sub_set).T)] -= minimal
        self.x0[tuple(np.array(add_set).T)] += minimal

        return sub_set[minimal_idx], minimal

    def get_best_solution(self):
        is_best = self.optimize()
        while not is_best:
            is_best = self.optimize()
        return self.result


# TEST CASES
# opt = TransportationOptimizer([50, 70, 80], [60, 30, 40, 70],
#                               np.array([[2, 4, 5, 1], [3, 6, 4, 8], [1, 2, 5, 3]]),
#                               np.array([[50, 0, 0, 0], [10, 30, 30, 0], [0, 0, 10, 70]]))
# opt = TransportationOptimizer([80, 110, 90, 440], [85, 75, 280, 280],
#                               np.array([[8, 2, 5, 4], [7, 5, 6, 8], [1, 3, 7, 5], [0, 0, 0, 0]]),
#                               np.array([[0, 75, 5, 0], [0, 0, 110, 0], [85, 0, 5, 0], [0, 0, 160, 280]]))
# opt = TransportationOptimizer([100, 160, 140], [80, 70, 100, 90, 60],
#                               np.array([[6, 5, 3, 1, 0], [9, 7, 5, 8, 0], [2, 9, 4, 6, 0]]),
#                               np.array([[0, 0, 0, 90, 10], [0, 70, 40, 0, 50], [80, 0, 60, 0, 0]]))
# result = opt.get_best_solution()
# print(result)
