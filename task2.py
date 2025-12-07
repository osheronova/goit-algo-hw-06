"""
Task 2.
DFS та BFS на графі спрощеного Київського метро 2025.
"""

from collections import deque
from task1 import build_graph


def bfs_path(G, start: str, goal: str) -> list[str] | None:
    """Пошук найкоротшого шляху (за кількістю ребер) за допомогою BFS."""
    if start == goal:
        return [start]

    visited = {start}
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        for neighbour in G.neighbors(node):
            if neighbour in visited:
                continue
            new_path = path + [neighbour]
            if neighbour == goal:
                return new_path
            visited.add(neighbour)
            queue.append((neighbour, new_path))

    return None


def dfs_path(G, start: str, goal: str) -> list[str] | None:
    """Пошук шляху за допомогою DFS (може бути довшим за найкоротший)."""
    if start == goal:
        return [start]

    visited: set[str] = set()
    stack: list[tuple[str, list[str]]] = [(start, [start])]

    while stack:
        node, path = stack.pop()

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            return path

        for neighbour in G.neighbors(node):
            if neighbour not in visited:
                stack.append((neighbour, path + [neighbour]))

    return None


def print_comparison(G, start: str, goal: str) -> None:
    bfs = bfs_path(G, start, goal)
    dfs = dfs_path(G, start, goal)

    print(f"\nМаршрут: {start} → {goal}")

    if bfs:
        print("BFS path: " + " → ".join(bfs))
        print(f"BFS length (edges): {len(bfs) - 1}")
    else:
        print("BFS path: not found")

    if dfs:
        print("DFS path: " + " → ".join(dfs))
        print(f"DFS length (edges): {len(dfs) - 1}")
    else:
        print("DFS path: not found")


def main() -> None:
    G = build_graph()

    # Декілька показових маршрутів для порівняння
    routes = [
        ("Академмістечко", "Лісова"),
        ("Героїв Дніпра", "Червоний хутір"),
        ("Сирець", "Теремки"),

    ]

    print("DFS vs BFS on simplified Kyiv Metro 2025 graph")
    for start, goal in routes:
        print_comparison(G, start, goal)


if __name__ == "__main__":
    main()
