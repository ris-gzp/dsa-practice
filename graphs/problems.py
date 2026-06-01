# Graphs — common patterns: DFS, BFS, topological sort, union-find
from collections import deque


def bfs(graph: dict[int, list[int]], start: int) -> list[int]:
    visited, queue, order = {start}, deque([start]), []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order


def dfs(graph: dict[int, list[int]], start: int, visited: set | None = None) -> list[int]:
    if visited is None:
        visited = set()
    visited.add(start)
    order = [start]
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            order.extend(dfs(graph, neighbor, visited))
    return order
