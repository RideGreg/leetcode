# Time:  O((|E| + |V|) * log|V|) = O(|E| * log|V|),
#        if we can further to use Fibonacci heap, it would be O(|E| + |V| * log|V|)
# Space: O(|E| + |V|) = O(|E|)

# 787
# There are n cities connected by m flights. Each fight starts from city u and arrives at v with a price w.
#
# Now given all the cities and fights, together with starting city src and the destination dst,
# your task is to find the cheapest price from src to dst with up to k stops.
# If there is no such route, output -1.
#
# Example 1:
# Input:
# n = 3, edges = [[0,1,100],[1,2,100],[0,2,500]]
# src = 0, dst = 2, k = 1
# Output: 200
# Explanation:
# The cheapest price from city 0 to city 2 with at most 1 stop costs 200, as marked red in the picture.
#
# Example 2:
# Input:
# n = 3, edges = [[0,1,100],[1,2,100],[0,2,500]]
# src = 0, dst = 2, k = 0
# Output: 500
#
# Explanation:
# The cheapest price from city 0 to city 2 with at most 0 stop costs 500, as marked blue in the picture.
# Note:
# - The number of nodes n will be in range [1, 100], with nodes labeled from 0 to n - 1.
# - The size of flights will be in range [0, n * (n - 1) / 2].
# - The format of each flight will be (src, dst, price).
# - The price of each flight will be in the range [1, 10000].
# - k is in the range of [0, n - 1].
# - There will not be any duplicated flights or self cycles.

import collections
import heapq


class Solution(object):
    # Dijkstra with dict
    def findCheapestPrice(self, n, flights, src, dst, K): # USE THIS
        graph = collections.defaultdict(dict)
        for u, v, w in flights:
            graph[u][v] = w

        best = {}
        heap = [[0, src, 0]]  # cost, node, step
        while heap:
            cost, node, step = heapq.heappop(heap)
            if node == dst:
                return cost
            if (node, step) in best or step > K:
                continue
            best[node, step] = cost

            for nei, w in graph[node].items():
                if (nei, step + 1) not in best:
                    heapq.heappush(heap, (cost + w, nei, step + 1))
        return -1

    # wrong: return 9 for 1st testcase. Each state must bre represented by (node, steps),
    # otherwise lower steps path is missing.
    def findCheapestPrice_wrong(self, n, flights, src, dst, K):
        graph = [{} for _ in range(n)]
        for u, v, w in flights:
            graph[u][v] = w

        best, pq = set(), [(0, src, 0)]
        while pq:
            p, node, stops = heapq.heappop(pq)
            if node == dst:
                return p

            if node not in best and stops <= K:
                best.add(node)

                for nei, w in graph[node].items():
                    if nei not in best:
                        heapq.heappush(pq, (p + w, nei, stops + 1))
        return -1

    # Dijkstra with list
    def findCheapestPrice2(self, n, flights, src, dst, K):
        graph = [{} for _ in range(n)]
        for u, v, p in flights:
            graph[u][v] = p

        # K stops means can move K+1 steps, store and update the best price for each step separately
        # no need to fill best[src][0] as 0 like stepless Dijkstra does, because we won't go back to overwrite step 0.
        best = [[float('inf')] * (K + 2) for _ in range(n)]
        minHeap = [(0, src, 0)]  # (price, node-to-reach, step-needed)
        while minHeap:
            price, node, step = heapq.heappop(minHeap)
            if node == dst:
                return price
            if step > K or price > best[node][step]: # prune
                continue
            for nei, p in graph[node].items():
                if price + p < best[nei][step + 1]:
                    heapq.heappush(minHeap, (price + p, nei, step + 1))
                    best[nei][step + 1] = price + p

        return -1


    def findCheapestPrice_kamyu(self, n, flights, src, dst, K):
        """
        :type n: int
        :type flights: List[List[int]]
        :type src: int
        :type dst: int
        :type K: int
        :rtype: int
        """
        adj = collections.defaultdict(list)
        for u, v, w in flights:
            adj[u].append((v, w))
        best = collections.defaultdict(lambda: collections.defaultdict(lambda: float("inf")))
        min_heap = [(0, src, K+1)]
        while min_heap:
            result, u, k = heapq.heappop(min_heap)
            if k < 0 or best[u][k] < result:
                continue
            if u == dst:
                return result
            for v, w in adj[u]:
                if result+w < best[v][k-1]:
                    best[v][k-1] = result+w                    
                    heapq.heappush(min_heap, (result+w, v, k-1))
        return -1

print(Solution().findCheapestPrice(5,
    [[0,1,5],[1,2,5],[0,3,2],[3,1,2],[1,4,1],[4,2,1]], 0, 2, 2)) # 7
print(Solution().findCheapestPrice(3, [[0,1,100],[1,2,100],[0,2,500],[1,0,600]], 0, 2, 1)) # 200
print(Solution().findCheapestPrice(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 0)) # 500