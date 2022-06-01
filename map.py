from numpy import array_equal


class Map:

    def __init__(self, g: list, start_cell: list):
        self.g  = g
        self.cycle = [start_cell]

    def _is_valid_state(self):
        if len(self.cycle) >= 4 \
                and self.cycle[0][1] == self.cycle[-1][1]:
            return True
        return False

    def _get_candidates(self):
        if len(self.cycle) % 2 == 1:
            candidates = [coor for coor in self.g if coor[0] == self.cycle[-1][0]
                          and not array_equal(coor, self.cycle[-1])]
        else:
            candidates = [coor for coor in self.g if coor[1] == self.cycle[-1][1]
                          and not array_equal(coor, self.cycle[-1])]
        return candidates

    def _search(self):
        if self._is_valid_state():
            return True

        for candidate in self._get_candidates():
            self.cycle.append(candidate)
            founded = self._search()
            if founded:
                return True
            else:
                self.cycle.pop()
        return False

    def search_for_cycle(self):
        founded = self._search()
        if founded:
            return self.cycle
        return None


# TEST
"""
    0 0 0 * *
    0 * * 0 *
    * 0 * 0 0
"""
# the_map = Map(g=[[0, 3],
#                  [0, 4],
#                  [1, 1],
#                  [1, 2],
#                  [1, 4],
#                  [2, 0],
#                  [2, 2]], start_cell=[2, 4])
# cycle = the_map.search_for_cycle()
# print(cycle)
