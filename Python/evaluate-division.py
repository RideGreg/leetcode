# Time:  O((e + q) * α(n)) ~= O(e + q), using either one of "path compression" and "union by rank" results in amortized O(logn)
#                                     , using  both results in α(n) ~= O(1)
# Space: O(n)

# 399
# Equations are given in the format A / B = k,
# where A and B are variables represented as strings,
# and k is a real number (floating point number).
# Given some queries, return the answers.
# If the answer does not exist, return -1.0.
#
# Example:
# Given a / b = 2.0, b / c = 3.0.
# queries are: a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ? .
# return [6.0, 0.5, -1.0, 1.0, -1.0 ].
#
# The input is:
# vector<pair<string, string>> euqations, vector<double>& values, vector<pair<string, string>> query .
#
# where equations.size() == values.size(),the values are positive.
# this represents the equations.return vector<double>. .
# The example above: equations = [ ["a", "b"], ["b", "c"] ].
# values = [2.0, 3.0]. queries = [ ["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"] ].
#
# The input is always valid. You may assume that
# evaluating the queries will result in no division by zero and there is no contradiction.

import collections


class Solution(object):
    # DFS: build Weighted Directed Graph, find Path Weight
    def calcEquation(self, equations, values, queries):
        """
        :type equations: List[List[str]]
        :type values: List[float]
        :type query: List[List[str]]
        :rtype: List[float]
        """
        def dfs(x, y):
            if y in graph[x]: # graph is defaultdict, so ok to access graph[x]
                return graph[x][y]

            for nei in graph[x]:
                if nei not in visited:
                    visited.add(nei) # IMPORTANT to avoid circle
                    ret = dfs(nei, y)
                    if ret is not None: # 不同的路径到达目标path value是一样的，找到一个路径即可返回
                        return graph[x][nei] * ret
            return None

        # construct Weighted Directed Graph
        graph = collections.defaultdict(dict)
        for i, (a, b) in enumerate(equations):
            graph[a][a] = 1; graph[b][b] = 1 # 自环路不是必须，是为了快速直接返回
            graph[a][b] = values[i]
            if values[i]: # 因为这是带权重的有向图，要顺便添加反向的edge
                graph[b][a] = 1 / values[i]

        ans = []
        for x, y in queries:
            if x not in graph or y not in graph:
                ans.append(-1.0)
            else:
                visited = set()
                v = dfs(x, y)
                ans.append(v if v is not None else -1.0)
        return ans

    # Weighted UnionFind
    # 构建带权值边的并查集，对于输入方程，初始化除数和被除数的根为自身，权值为1。再合并除数
    # 和被除数使其连通，有相同的根，更新权值 = 数/根。

    # 对于每个查询：若不联通，则答案为-1.0；若联通，则使用它们与共同根相除的结果计算商。
    def calcEquation2(self, equations, values, queries):
        def find(x):
            if x not in root: return None, -1
            w = 1
            while root[x] != x: # we skipped path compression for simplicity
                w *= weight[x]
                x = root[x]
            return x, w

        def union(x, y, w):
            xroot, xweight = find(x) # xweight = x / xroot
            yroot, yweight = find(y) # yweight = y / yroot
            if not xroot or not yroot or xroot == yroot:
                return

            root[xroot] = yroot
            weight[xroot] = 1 / xweight * w * yweight # = xroot / yroot
            self.count -= 1

        root, weight, self.count = {}, {}, 0 # count is for reference, not used in this problem
        for i, (x, y) in enumerate(equations):
            for node in [x, y]:
                if node not in root: # initialize
                    root[node] = node
                    weight[node] = 1
                    self.count += 1
            union(x, y, values[i])

        ans = []
        for x, y in queries:
            xroot, xweight = find(x) # xweight = x / xroot
            yroot, yweight = find(y) # yweight = y / yroot
            if not xroot or not yroot or xroot != yroot:
                ans.append(-1)
            else:
                ans.append(xweight / yweight)
        return ans


import collections
import itertools


class UnionFind(object):
    def __init__(self):
        self.set = {}
        self.rank = collections.Counter()

    def find_set(self, x):
        xp, xr = self.set.setdefault(x, (x, 1.0))
        if x != xp:
            pp, pr = self.find_set(xp)  # path compression.
            self.set[x] = (pp, xr*pr)  # x/pp = xr*pr
        return self.set[x]

    def union_set(self, x, y, r):
        (xp, xr), (yp, yr) =  map(self.find_set, (x, y))
        if xp == yp:
            return False
        if self.rank[xp] < self.rank[yp]:  # union by rank
            # to make x/yp = r*yr and merge xp into yp
            # => since x/xp = xr, we can merge with xp/yp = r*yr/xr 
            self.set[xp] = (yp, r*yr/xr)
        elif self.rank[xp] > self.rank[yp]:
            # to make y/xp = 1/r*xr and merge xp into yp
            # => since y/yp = yr, we can merge with yp/xp = 1/r*xr/yr 
            self.set[yp] = (xp, 1.0/r*xr/yr)
        else:
            # to make y/xp = 1/r*xr and merge xp into yp
            # => since y/yp = yr, we can merge with yp/xp = 1/r*xr/yr 
            self.set[yp] = (xp, 1.0/r*xr/yr)
            self.rank[xp] += 1 
        return True

    def query_set(self, x, y):
        if x not in self.set or y not in self.set:
            return -1.0
        (xp, xr), (yp, yr) = map(self.find_set, (x, y))
        return xr/yr if xp == yp else -1.0


class UnionFindPathCompressionOnly(object):
    def __init__(self):
        self.set = {}

    def find_set(self, x):
        xp, xr = self.set.setdefault(x, (x, 1.0))
        if x != xp:
            pp, pr = self.find_set(xp)  # path compression.
            self.set[x] = (pp, xr*pr)  # x/pp = xr*pr
        return self.set[x]

    def union_set(self, x, y, r):
        (xp, xr), (yp, yr) =  map(self.find_set, (x, y))
        if xp == yp:
            return False
        # to make x/yp = r*yr and merge xp into yp
        # => since x/xp = xr, we can merge with xp/yp = r*yr/xr 
        self.set[xp] = (yp, r*yr/xr)
        return True

    def query_set(self, x, y):
        if x not in self.set or y not in self.set:
            return -1.0
        (xp, xr), (yp, yr) = map(self.find_set, (x, y))
        return xr/yr if xp == yp else -1.0


class Solution_kamyu(object):
    def calcEquation(self, equations, values, queries):
        """
        :type equations: List[List[str]]
        :type values: List[float]
        :type queries: List[List[str]]
        :rtype: List[float]
        """
        union_find = UnionFind()
        for (a, b), k in zip(equations, values):
            union_find.union_set(a, b, k)
        return [union_find.query_set(a, b) for a, b in queries]


# Time:  O(e + q * n), at most O(n^3 + q)
# Space: O(n^2)
# bfs solution
import collections
import itertools


class Solution2(object):
    def calcEquation(self, equations, values, queries):
        """
        :type equations: List[List[str]]
        :type values: List[float]
        :type queries: List[List[str]]
        :rtype: List[float]
        """
        adj = collections.defaultdict(dict)
        for (a, b), k in zip(equations, values):
            adj[a][b] = k
            adj[b][a] = 1.0/k

        def bfs(adj, a, b, lookup):
            if a not in adj or b not in adj:
                return -1.0
            if (a, b) in lookup:
                return lookup[a, b]
            visited = {a}
            q = collections.deque([(a, 1.0)])
            while q:
                u, val = q.popleft()
                if u == b:
                    lookup[a, b] = val
                    return val
                for v, k in adj[u].items():
                    if v not in visited:
                        visited.add(v)
                        q.append((v, val*k))
            lookup[a, b] = -1.0
            return -1.0

        lookup = {}
        return [bfs(adj, a, b, lookup) for a, b in queries]


# Time:  O(n^3 + q)
# Space: O(n^2)
import collections
import itertools


# variant of floyd–warshall algorithm solution: populate many edges
class Solution3(object):
    def calcEquation(self, equations, values, queries):
        """
        :type equations: List[List[str]]
        :type values: List[float]
        :type queries: List[List[str]]
        :rtype: List[float]
        """
        adj = collections.defaultdict(dict)
        for (a, b), k in itertools.izip(equations, values):
            adj[a][a] = adj[b][b] = 1.0
            adj[a][b] = k
            adj[b][a] = 1.0/k
        for k in adj:
            for i in adj[k]:
                for j in adj[k]:
                    adj[i][j] = adj[i][k]*adj[k][j]
        return [adj[a].get(b, -1.0) for a, b in queries]



print(Solution().calcEquation(
    [["x1","x2"],["x2","x3"],["x3","x4"],["x4","x5"]],
    [3.0,4.0,5.0,6.0],
    [["x1","x5"],["x5","x2"],["x2","x4"],["x2","x2"],["x2","x9"],["x9","x9"]]
)) # [360.00000,0.00833,20.00000,1.00000,-1.00000,-1.00000]
print(Solution().calcEquation(
    [["a", "b"], ["b", "c"]],
    [2.0, 3.0],
    [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
)) # [6.0, 0.5, -1.0, 1.0, -1.0]
