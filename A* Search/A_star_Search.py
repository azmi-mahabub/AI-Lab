h = {'AP': 5, 'KBR': 4, 'B': 4, 'M': 2, 'JG': 1, 'UAP': 0,
     'KB': 2, 'Pan': 1, 'AG': 4, 'K': 3, 'CMH': 2}
edges = {
    'AP': {'KBR': 5},
    'KBR': {'B': 6, 'CMH': 5},
    'B': {'M': 3},
    'M': {'JG': 2, 'KB': 4},
    'JG': {'UAP': 4},
    'KB': {'Pan': 2},
    'Pan': {'UAP': 2},
    'CMH': {'K': 5},
    'K': {'AG': 5},
    'AG': {'UAP': 6}
}

start = 'AP'
goal = 'UAP'

opened = [start]
closed = {}
g = {start: 0}

while opened:
    current = opened[0]
    for node in opened:
        if g[node] + h[node] < g[current] + h[current]:
            current = node

    if current == goal:
        path = [current]
        while current in closed:
            current = closed[current]
            path.insert(0, current)
        print("Optimal path:", " -> ".join(path))
        print("Total cost:", g[goal])
        break

    opened.remove(current)

    for neighbor, weight in edges.get(current, {}).items():
        G = g[current] + weight
        if neighbor not in g or G < g[neighbor]:
            g[neighbor] = G
            closed[neighbor] = current
            if neighbor not in opened:
                opened.append(neighbor)

