from collections import deque

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

def bfs(graph, start, goal):

    if start not in graph:
        print(f"Error: '{start}' no existe en el grafo.")
        return None, None, None
    
    if goal not in graph:
        print(f"Error: '{goal}' no existe en el grafo.")
        return None, None, None
    
    if start == goal:
        return [start], 0, 0
    
    # cola FIFO cada elemento es (ciudad_actual, camino recorrido, costo_acumulado)
    queue = deque()
    queue.append((start, [start], 0))

    #ciudades visitadas
    visited = set()
    visited.add(start)

    while queue:
        current_city, path, cost = queue.popleft() #FIFO, saca el primer elemento

        #explora vecinos
        for neighbor, weight in graph.get(current_city, []):

            if neighbor in visited:
                continue
                
            new_path = path + [neighbor]
            new_cost = cost + weight
            
            #si el vecino es el objetivo, retorna el camino, costo y número de nodos visitados
            if neighbor == goal:
                hops = len(new_path) - 1
                return new_path, new_cost, hops
            
            #marca el vecino como visitado y lo agrega a la cola
            visited.add(neighbor)
            queue.append((neighbor, new_path, new_cost))

    #si se vacía la cola sin encontrar el objetivo, retorna None
    return None, None, None


def bfs_steps(start, goal):
    if start not in graph:
        return None, None, None, []

    if goal not in graph:
        return None, None, None, []

    if start == goal:
        steps = [{"current": start, "open_set": [start], "visited": []}]
        return [start], 0, 0, steps

    queue = deque()
    queue.append((start, [start], 0))

    visited = set()
    visited.add(start)
    steps = []

    while queue:
        current_city, path, cost = queue.popleft()

        steps.append(
            {
                "current": current_city,
                "open_set": [current_city] + [node for node, _, _ in queue],
                "visited": sorted(visited - {current_city}),
            }
        )

        for neighbor, weight in graph.get(current_city, []):
            if neighbor in visited:
                continue

            new_path = path + [neighbor]
            new_cost = cost + weight

            if neighbor == goal:
                hops = len(new_path) - 1
                steps.append(
                    {
                        "current": neighbor,
                        "open_set": [neighbor] + [node for node, _, _ in queue],
                        "visited": sorted(visited),
                    }
                )
                return new_path, new_cost, hops, steps

            visited.add(neighbor)
            queue.append((neighbor, new_path, new_cost))

    return None, None, None, steps

# Ejemplo de uso

if __name__ == "__main__":

    casos = [
        ("Pasto", "Barranquilla"),
        ("Cali", "Bogota"),
        ("Cucuta", "Riohacha"),
        ("Bogota", "Bogota"),
        ("Pasto", "Riohacha"),

    ]

    for start, goal in casos:
        print(f"\n{'='*50}")
        print(f" Origen = {start}")
        print(f" Destino = {goal}")
        print(f"{'='*50}\n")

        path, cost, hops = bfs(graph, start, goal)

        if path is None:
            print(" Resultado: No existe un camino entre las ciudades.")
        else:
            print(f" Camino: {' -> '.join(path)}")
            print(f" Saltos: {hops} ciudades intermedias")
            print(f" Costo km: {cost:.4f} km (bfs no considera costos, solo el número de saltos)")