"""
Kyiv Metro 2025 Graph (simplified version)
Schematic layout similar to Kyiv metro map
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import networkx as nx


# ---------- 1. SIMPLIFIED LINES ----------

line_M1 = [
    "Академмістечко",
    "Житомирська",
    # "Святошин",
    # "Нивки",
    # "Берестейська",
    "Шулявська",
    "Політехнічний інститут",
    "Вокзальна",
    "Університет",
    "Театральна",
    "Хрещатик",
    "Арсенальна",
    "Дніпро",
    # "Гідропарк",
    "Лівобережна",
    # "Дарниця",
    # "Чернігівська",
    "Лісова",
]

line_M2 = [
    "Героїв Дніпра",
    # "Варшавська",
    "Оболонь",
    "Почайна",
    # "Тараса Шевченка",
    # "Контрактова площа",
    "Поштова площа",
    "Майдан Незалежності",
    "Площа Українських Героїв",
    "Олімпійська",
    'Палац "Україна"',
    # "Либідська",
    # "Деміївська",
    "Голосіївська",
    # "Васильківська",
    "Виставковий центр",
    # "Іподром",
    "Теремки",
]

line_M3 = [
    "Сирець",
    # "Дорогожичі",
    "Лук'янівська",
    "Золоті ворота",
    "Палац спорту",
    # "Кловська",
    "Печерська",
    "Звіринецька",
    # "Видубичі",
    # "Славутич",
    "Осокорки",
    "Позняки",
    # "Харківська",
    # "Вирлиця",
    "Бориспільська",
    "Червоний хутір",
]

lines = {"M1": line_M1, "M2": line_M2, "M3": line_M3}

TRANSFER_STATIONS = {
    "Хрещатик",
    "Майдан Незалежності",
    "Театральна",
    "Золоті ворота",
    "Площа Українських Героїв",
    "Палац спорту",
}

LINE_COLORS = {"M1": "#e74c3c", "M2": "#3498db", "M3": "#2ecc71"}

# Ребра, де при спрощенні були видалені проміжні станції → time = 5
LONG_EDGES = {
    "M1": [
        ("Житомирська", "Шулявська"),   # Святошин, Нивки, Берестейська
        ("Дніпро", "Лівобережна"),      # Гідропарк
        ("Лівобережна", "Лісова"),      # Дарниця, Чернігівська
    ],
    "M2": [
        ("Героїв Дніпра", "Оболонь"),           # Варшавська
        ("Почайна", "Поштова площа"),   # Тараса Шевченка, Контрактова площа
        ('Палац "Україна"', "Голосіївська"),   # Либідська, Деміївська
        ("Голосіївська", "Виставковий центр"),  # Васильківська
        ("Виставковий центр", "Теремки"),      # Іподром
    ],
    "M3": [
        ("Сирець", "Лук'янівська"),        # Дорогожичі
        ("Палац спорту", "Печерська"),     # Кловська
        ("Звіринецька", "Осокорки"),       # Видубичі, Славутич
        ("Позняки", "Бориспільська"),      # Харківська, Вирлиця
    ],
}


# ---------- 2. BUILD GRAPH ----------


def add_line_edges(G, stations):
    # базово всюди ставимо time=3 (сусідні станції)
    for u, v in zip(stations[:-1], stations[1:]):
        G.add_edge(u, v, time=3)


def build_graph():
    G = nx.Graph()

    for code, st_list in lines.items():
        # додаємо вершини
        for st in st_list:
            if st not in G:
                G.add_node(st, lines={code})
            else:
                G.nodes[st]["lines"].add(code)

        # додаємо стандартні ребра між сусідніми станціями (time=3)
        add_line_edges(G, st_list)

        # оновлюємо вагу до 5 там, де при спрощенні були вилучені станції
        for u, v in LONG_EDGES.get(code, []):
            if G.has_edge(u, v):
                G[u][v]["time"] = 5

    # Interchanges (пересадки) → time = 4
    transfers = [
        ("Театральна", "Золоті ворота"),
        ("Хрещатик", "Майдан Незалежності"),
        ("Площа Українських Героїв", "Палац спорту"),
    ]
    for u, v in transfers:
        G.add_edge(u, v, time=4)

    return G


# ---------- 3. ANALYSIS ----------


def analyze_graph(G: nx.Graph) -> None:
    print("Analysis of the simplified Kyiv Metro 2025 Graph\n")

    print("Basic characteristics:")
    print(f"   Number of stations (nodes): {G.number_of_nodes()}")
    print(f"   Number of connections (edges): {G.number_of_edges()}")

    degrees = dict(G.degree())
    print("\nTop stations by degree (number of connections):")
    for station, degree in sorted(
        degrees.items(), key=lambda x: x[1], reverse=True
    )[:10]:
        print(f"   {station}: {degree}")

    avg_degree = sum(degrees.values()) / G.number_of_nodes()
    print(f"\nAverage degree: {avg_degree:.2f}")

    density = nx.density(G)
    print(f"Graph density: {density:.4f}")

    if nx.is_connected(G):
        diameter = nx.diameter(G)
        radius = nx.radius(G)
        print(f"Diameter: {diameter}")
        print(f"Radius: {radius}")
    else:
        print("Graph is not connected.")

    betweenness = nx.betweenness_centrality(G, weight="time")
    print("\nTop 5 stations by betweenness centrality:")
    for station, value in sorted(
        betweenness.items(), key=lambda x: x[1], reverse=True
    )[:5]:
        print(f"   {station}: {value:.4f}")

    clustering = nx.average_clustering(G)
    print(f"\nAverage clustering coefficient: {clustering:.4f}")


# ---------- 4. SCHEMATIC COORDINATES + VISUALISATION ----------


def node_color(G, n):
    if n in TRANSFER_STATIONS:
        return "#f1c40f"
    return LINE_COLORS[list(G.nodes[n]["lines"])[0]]


def visualize(G):
    print("Drawing simplified Kyiv Metro 2025 layout...")

    # ---- Coordinates updated (lower M2 shifted left, Olympiiska lower) ----
    pos = {
        # M1 (red)
        "Академмістечко": (-10, -1),
        "Житомирська": (-9, -1),
        "Шулявська": (-7, -0.6),
        "Політехнічний інститут": (-5.5, -0.4),
        "Вокзальна": (-4, -0.2),
        "Університет": (-2.8, -0.1),
        "Театральна": (-1.5, 0),
        "Хрещатик": (0, 0),
        "Арсенальна": (1.2, 0.2),
        "Дніпро": (2.3, 0.4),
        "Лівобережна": (3.5, 0.6),
        "Лісова": (5, 0.8),

        # M2 (blue)
        "Героїв Дніпра": (1, 6),
        "Оболонь": (1, 4.2),
        "Почайна": (1, 3.2),
        "Поштова площа": (0.8, 1.7),
        "Майдан Незалежності": (0, 1.0),
        "Площа Українських Героїв": (0, -1.0),
        "Олімпійська": (-0.5, -2.4),
        'Палац "Україна"': (-1.0, -3.1),
        "Голосіївська": (-1.8, -3.9),
        "Виставковий центр": (-2.3, -5.2),
        "Теремки": (-2.8, -6.6),

        # M3 (green)
        "Сирець": (-3.5, 3),
        "Лук'янівська": (-2.4, 2),
        "Золоті ворота": (-1.5, 1),
        "Палац спорту": (-0.7, -1.4),
        "Печерська": (1.0, -3.0),
        "Звіринецька": (2, -3.9),
        "Осокорки": (3.3, -4.8),
        "Позняки": (4.5, -5.4),
        "Бориспільська": (5.5, -6),
        "Червоний хутір": (6.3, -6.6),
    }

    node_sizes = [900 if n in TRANSFER_STATIONS else 450 for n in G.nodes()]
    node_colors = [node_color(G, n) for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(16, 10))

    # ребра
    nx.draw_networkx_edges(
        G, pos, width=2.5, alpha=0.6, edge_color="gray", ax=ax
    )

    # 🔢 підписи до ребер: час у хвилинах (атрибут time)
    edge_labels = nx.get_edge_attributes(G, "time")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=7,
        ax=ax,
    )

    # вузли
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="black",
        linewidths=1.3,
        ax=ax,
    )
    nx.draw_networkx_labels(
        G, pos, font_size=8, font_weight="bold", ax=ax
    )

    ax.set_title(
        "Kyiv Metro 2025 (Simplified schematic layout)",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.axis("off")

    legend_elements = [
        Patch(facecolor=LINE_COLORS["M1"], edgecolor="black", label="M1"),
        Patch(facecolor=LINE_COLORS["M2"], edgecolor="black", label="M2"),
        Patch(facecolor=LINE_COLORS["M3"], edgecolor="black", label="M3"),
        Patch(facecolor="#f1c40f", edgecolor="black", label="Пересадка"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=10)

    plt.tight_layout()
    plt.savefig("kyiv_metro_2025_schematic_simplified.png", dpi=300)
    plt.show()


# ---------- 5. MAIN ----------


def main():
    G = build_graph()
    analyze_graph(G)
    visualize(G)


if __name__ == "__main__":
    main()
