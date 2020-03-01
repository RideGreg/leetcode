# Time:  O(m * n)
# Space: O(m * n)

import collections


# A* Search Algorithm without heap
class Solution(object):
    def minCost(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        def a_star(grid, b, t):
            R, C = len(grid), len(grid[0])
            f, dh = 0, 1
            closer, detour = [b], []
            lookup = set()
            while closer or detour:
                if not closer:
                    f += dh
                    closer, detour = detour, closer
                b = closer.pop()
                if b == t:
                    return f
                if b in lookup:
                    continue
                lookup.add(b)
                for nd, (dr, dc) in enumerate(directions, 1):
                    nb = (b[0]+dr, b[1]+dc)
                    if not (0 <= nb[0] < R and 0 <= nb[1] < C and nb not in lookup):
                        continue
                    (closer if nd == grid[b[0]][b[1]] else detour).append(nb)
            return -1

        return a_star(grid, (0, 0), (len(grid)-1, len(grid[0])-1))

    
# Time:  O(m * n)
# Space: O(m * n)
class Solution2(object):
    def minCost(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: int
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        R, C = len(grid), len(grid[0])
        dq = collections.deque([((0, 0), 0)])
        lookup = {(0, 0): 0}
        while dq:
            b, d = dq.popleft()
            if b == (R-1, C-1):
                return d
            for nd, (dr, dc) in enumerate(directions, 1):
                nb = (b[0]+dr, b[1]+dc)
                cost = 1-(nd == grid[b[0]][b[1]])
                if not (0 <= nb[0] < R and 0 <= nb[1] < C and
                        (nb not in lookup or lookup[nb] > d+cost)):
                    continue
                lookup[nb] = d+cost
                if cost:
                    dq.append((nb, d+cost))
                else:
                    dq.appendleft((nb, d))
        return -1  # never reach here
