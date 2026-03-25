def uniform_cost_search(graph, start, goal):
    dist = {start: 0}
    parent = {start: None}
    frontier = [(0, start)]  # (coste acumulado, nodo)
    while frontier:
        # seleccionar el nodo con menor costo acumulado
        frontier.sort(key=lambda x: x[0])  # ordena por costo
        cost, node = frontier.pop(0)       # saca el primero (menor costo)
        # ignorar entradas viejas
        if cost > dist.get(node, float('inf')):
            continue
        # Si llegamos al objetivo
        if node == goal:
            # reconstruir camino
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, cost
        # expandir vecinos
        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                parent[neighbor] = node
                frontier.append((new_cost, neighbor))
    return None, None


def uniform_cost_search_steps(start, goal):
    if start not in graph or goal not in graph:
        return None, None, []

    dist = {start: 0}
    parent = {start: None}
    frontier = [(0, start)]
    steps = []
    visited = set()

    while frontier:
        frontier.sort(key=lambda x: x[0])
        cost, node = frontier.pop(0)

        if cost > dist.get(node, float('inf')):
            continue

        steps.append(
            {
                "current": node,
                "open_set": [node] + [n for _, n in frontier],
                "visited": sorted(visited),
                "g": {city: value for city, value in dist.items()},
            }
        )

        if node == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            path.reverse()
            return path, cost, steps

        visited.add(node)

        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if new_cost < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_cost
                parent[neighbor] = node
                frontier.append((new_cost, neighbor))

    return None, None, steps

#grafo con rutas
graph = {
    'Armenia': [('Cali', 152.9434), ('Ibague', 50.8713), ('Pereira', 31.2149)],
    'Barranquilla': [('Cartagena', 99.7108), ('Santa Marta', 70.3822), ('Sincelejo', 196.9281)],
    'Bogota': [('Bucaramanga', 287.6396), ('Ibague', 132.0978), ('Tunja', 120.3551), ('Villavicencio', 80.2645)],
    'Bucaramanga': [('Bogota', 287.6396), ('Cucuta', 109.9525), ('Tunja', 178.2034)],
    'Cali': [('Armenia', 152.9434), ('Popayan', 112.3271)],
    'Cartagena': [('Barranquilla', 99.7108), ('Monteria', 187.9459), ('Sincelejo', 121.1214)],
    'Cucuta': [('Bucaramanga', 109.9525)],
    'Ibague': [('Armenia', 50.8713), ('Bogota', 132.0978), ('Neiva', 168.1727)],
    'Manizales': [('Medellin', 130.7446), ('Pereira', 34.8063)],
    'Medellin': [('Manizales', 130.7446), ('Monteria', 280.3587)],
    'Monteria': [('Cartagena', 187.9459), ('Medellin', 280.3587), ('Sincelejo', 81.5702)],
    'Neiva': [('Ibague', 168.1727)],
    'Pasto': [('Popayan', 155.652)],
    'Pereira': [('Armenia', 31.2149), ('Manizales', 34.8063)],
    'Popayan': [('Cali', 112.3271), ('Pasto', 155.652)],
    'Riohacha': [('Santa Marta', 144.8013)],
    'Santa Marta': [('Barranquilla', 70.3822), ('Riohacha', 144.8013)],
    'Sincelejo': [('Barranquilla', 196.9281), ('Cartagena', 121.1214), ('Monteria', 81.5702)],
    'Tunja': [('Bogota', 120.3551), ('Bucaramanga', 178.2034)],
    'Villavicencio': [('Bogota', 80.2645)]
    }

# Ejemplo: buscar de S a X
if __name__ == "__main__":
    path, cost = uniform_cost_search(graph, 'Cali', 'Bogota')
    print("Camino óptimo:", path)
    print("Costo total:", cost)