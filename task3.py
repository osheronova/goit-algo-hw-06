"""
Task 3.
Dijkstra's algorithm on the simplified Kyiv Metro 2025 graph.

Graph is built in task1.py (build_graph):
- edge weight 'time' is used as travel time in minutes
  (3 = normal, 4 = transfer, 5 = long jump after simplification).
"""

import heapq
import csv
import matplotlib.pyplot as plt

from task1 import build_graph  # reuse graph from Task 1


# ---------- Dijkstra ----------


def dijkstra(G, start):
    """Run Dijkstra from one start node. Returns (dist, prev)."""
    dist = {node: float("inf") for node in G.nodes()}
    prev = {node: None for node in G.nodes()}
    dist[start] = 0

    heap = [(0, start)]  # (distance, node)

    while heap:
        cur_dist, u = heapq.heappop(heap)
        if cur_dist > dist[u]:
            continue  # outdated value

        for v in G.neighbors(u):
            w = G[u][v].get("time", 1)
            new_dist = cur_dist + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return dist, prev


def restore_path(prev, start, end):
    """Rebuild path from start to end using 'prev' dict."""
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        if cur == start:
            break
        cur = prev[cur]
    path.reverse()
    if not path or path[0] != start:
        return []  # no path
    return path


# ---------- All-pairs shortest paths ----------


def compute_all_pairs(G):
    """Run Dijkstra from each node. Returns (nodes, dist, paths)."""
    nodes = list(G.nodes())
    all_dist = {}
    all_paths = {}

    for start in nodes:
        dist, prev = dijkstra(G, start)
        all_dist[start] = dist
        all_paths[start] = {
            end: restore_path(prev, start, end) for end in nodes
        }

    return nodes, all_dist, all_paths


def save_distance_matrix_csv(nodes, all_dist, filename="task3_distance_matrix.csv"):
    """Save shortest-path distance matrix to CSV (for Excel / analysis)."""
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Station"] + nodes)
        for i in nodes:
            row = [
                i,
                *[
                    int(all_dist[i][j])
                    if all_dist[i][j] != float("inf")
                    else ""
                    for j in nodes
                ],
            ]
            writer.writerow(row)


# ---------- Heatmap plotting ----------


def plot_distance_heatmap(nodes, all_dist, filename="task3_distance_heatmap.png"):
    """Draw heatmap of shortest travel times between all station pairs."""
    n = len(nodes)
    # build numeric matrix in fixed order of nodes
    matrix = [
        [
            all_dist[i][j] if all_dist[i][j] != float("inf") else 0
            for j in nodes
        ]
        for i in nodes
    ]

    fig, ax = plt.subplots(figsize=(0.4 * n + 4, 0.4 * n + 4))

    im = ax.imshow(matrix, cmap="OrRd")

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(nodes, rotation=90, fontsize=6)
    ax.set_yticklabels(nodes, fontsize=6)

    ax.set_title("Distance matrix of shortest paths\n(time in minutes)")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Time (minutes)")

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.show()


# ---------- Demo / main ----------


def main():
    G = build_graph()

    print("Dijkstra's algorithm on simplified Kyiv Metro 2025 graph\n")

    nodes, all_dist, all_paths = compute_all_pairs(G)

    # few example routes
    examples = [
        ("Академмістечко", "Лісова"),
        ("Героїв Дніпра", "Червоний хутір"),
        ("Сирець", "Теремки"),
        ("Позняки", "Майдан Незалежності"),
    ]

    print("Examples of shortest paths by travel time:\n")
    for start, end in examples:
        path = all_paths[start][end]
        time = all_dist[start][end]
        print(f"{start} -> {end}")
        print("   Path: " + " -> ".join(path))
        print(f"   Total time: {int(time)} min\n")

    # save matrix for report / Excel
    save_distance_matrix_csv(nodes, all_dist)
    print("Distance matrix saved to 'task3_distance_matrix.csv'")

    # draw heatmap like in example
    plot_distance_heatmap(nodes, all_dist)
    print("Heatmap saved to 'task3_distance_heatmap.png'")


if __name__ == "__main__":
    main()
