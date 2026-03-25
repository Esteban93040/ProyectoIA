import math

# Grafo con ciudades
ciudades = {
    'Bogota': {'latitud': 4.7110, 'longitud': -74.0721},
    'Medellin': {'latitud': 6.2442, 'longitud': -75.5812},
    'Cali': {'latitud': 3.4516, 'longitud': -76.5320},
    'Barranquilla': {'latitud': 10.9685, 'longitud': -74.7813},
    'Cartagena': {'latitud': 10.3910, 'longitud': -75.4794},
    'Bucaramanga': {'latitud': 7.1193, 'longitud': -73.1227},
    'Pereira': {'latitud': 4.8143, 'longitud': -75.6946},
    'Santa Marta': {'latitud': 11.2408, 'longitud': -74.1990},
    'Ibague': {'latitud': 4.4389, 'longitud': -75.2322},
    'Manizales': {'latitud': 5.0703, 'longitud': -75.5138},
    'Pasto': {'latitud': 1.2136, 'longitud': -77.2811},
    'Villavicencio': {'latitud': 4.1420, 'longitud': -73.6266},
    'Neiva': {'latitud': 2.9273, 'longitud': -75.2819},
    'Armenia': {'latitud': 4.5339, 'longitud': -75.6811},
    'Cucuta': {'latitud': 7.8891, 'longitud': -72.4967},
    'Popayan': {'latitud': 2.4448, 'longitud': -76.6147},
    'Monteria': {'latitud': 8.7479, 'longitud': -75.8814},
    'Sincelejo': {'latitud': 9.3047, 'longitud': -75.3978},
    'Tunja': {'latitud': 5.5353, 'longitud': -73.3678},
    'Riohacha': {'latitud': 11.5444, 'longitud': -72.9072}
}

#grafo con rutas
conexiones = {
    'Armenia': {'Cali': 152.9434, 'Ibague': 50.8713, 'Pereira': 31.2149},
    'Barranquilla': {'Cartagena': 99.7108, 'Santa Marta': 70.3822, 'Sincelejo': 196.9281},
    'Bogota': {'Bucaramanga': 287.6396, 'Ibague': 132.0978, 'Tunja': 120.3551, 'Villavicencio': 80.2645},
    'Bucaramanga': {'Bogota': 287.6396, 'Cucuta': 109.9525, 'Tunja': 178.2034},
    'Cali': {'Armenia': 152.9434, 'Popayan': 112.3271},
    'Cartagena': {'Barranquilla': 99.7108, 'Monteria': 187.9459, 'Sincelejo': 121.1214},
    'Cucuta': {'Bucaramanga': 109.9525},
    'Ibague': {'Armenia': 50.8713, 'Bogota': 132.0978, 'Neiva': 168.1727},
    'Manizales': {'Medellin': 130.7446, 'Pereira': 34.8063},
    'Medellin': {'Manizales': 130.7446, 'Monteria': 280.3587},
    'Monteria': {'Cartagena': 187.9459, 'Medellin': 280.3587, 'Sincelejo': 81.5702},
    'Neiva': {'Ibague': 168.1727},
    'Pasto': {'Popayan': 155.652},
    'Pereira': {'Armenia': 31.2149, 'Manizales': 34.8063},
    'Popayan': {'Cali': 112.3271, 'Pasto': 155.652},
    'Riohacha': {'Santa Marta': 144.8013},
    'Santa Marta': {'Barranquilla': 70.3822, 'Riohacha': 144.8013},
    'Sincelejo': {'Barranquilla': 196.9281, 'Cartagena': 121.1214, 'Monteria': 81.5702},
    'Tunja': {'Bogota': 120.3551, 'Bucaramanga': 178.2034},
    'Villavicencio': {'Bogota': 80.2645}}

def distancebystart (latStart, lonStart, latDest,lonDest):
    r = 6371.0

    latStart = math.radians(latStart) 
    lonStart = math.radians(lonStart) 
    latDest = math.radians(latDest) 
    lonDest = math.radians(lonDest) 

    dlat= latDest-latStart
    dlon= lonDest-lonStart

    a=math.sin(dlat/2)**2 + math.cos(latStart)*math.cos(latDest)*math.sin(dlon/2)**2
    c= 2* math.asin(math.sqrt(a))

    distance= r*c

    return distance

#Codigo utilizado para hallar la distancia entre conexiones
# grafo = {}
# for ciudad, vecinos in conexiones.items():
#     grafo[ciudad] = {}
#     for vecino in vecinos:
#         dist = distancebystart(
#             ciudades[ciudad]["latitud"], ciudades[ciudad]["longitud"],
#             ciudades[vecino]["latitud"], ciudades[vecino]["longitud"],
#         )
#         grafo[ciudad][vecino] = round(dist, 4)

# print("grafo = ")
# pprint.pprint(grafo, sort_dicts=True)


# Heurística h(n): distancia en línea desde un punto hasta el destino+
def crear_heuristica(ciudades_dict, ciudad_destino):
    """Calcula la distancia de cada ciudad al destino"""
    h = {}
    lat_dest = ciudades_dict[ciudad_destino]['latitud']
    lon_dest = ciudades_dict[ciudad_destino]['longitud']
    
    for ciudad, coords in ciudades_dict.items():
        h[ciudad] = distancebystart(
            coords['latitud'], 
            coords['longitud'], 
            lat_dest, 
            lon_dest
        )
    
    return h



def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(start)
    return path[::-1]


def a_star(start, goal):
    h = crear_heuristica(ciudades, goal)
    open_set = {start}
    came_from = {}
    g = {city: float('inf') for city in conexiones}
    g[start] = 0
    f = {city: float('inf') for city in conexiones}
    f[start] = h[start]

    while open_set:
        # nodo con menor f
        current = min(open_set, key=lambda x: f[x])
        if current == goal:
            return reconstruct_path(came_from, start, goal), g[goal]

        open_set.remove(current)
        for neighbor, cost in conexiones[current].items():
            tentative_g = g[current] + cost
            if tentative_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = tentative_g
                f[neighbor] = tentative_g + h[neighbor]
                open_set.add(neighbor)

    return None, float('inf')

def a_star_steps(start, goal):
    h = crear_heuristica(ciudades, goal)
    open_set = {start}
    visited = set()
    came_from = {}
    g = {city: float('inf') for city in conexiones}
    g[start] = 0
    f = {city: float('inf') for city in conexiones}
    f[start] = h[start]

    steps = []  # 👈 NUEVO

    while open_set:
        current = min(open_set, key=lambda x: f[x])

        # guardar estado
        steps.append({
            "current": current,
            "open_set": sorted(open_set),
            "visited": sorted(visited),
            "g": {city: cost for city, cost in g.items() if cost != float('inf')},
            "f": {city: score for city, score in f.items() if score != float('inf')}
        })

        if current == goal:
            return reconstruct_path(came_from, start, goal), g[goal], steps

        open_set.remove(current)
        visited.add(current)

        for neighbor, cost in conexiones[current].items():
            tentative_g = g[current] + cost
            if tentative_g < g[neighbor]:
                came_from[neighbor] = current
                g[neighbor] = tentative_g
                f[neighbor] = tentative_g + h[neighbor]
                open_set.add(neighbor)

    return None, float('inf'), steps


def get_graph_data():
    roads = []
    seen = set()
    for source, neighbors in conexiones.items():
        for target, cost in neighbors.items():
            road_id = tuple(sorted((source, target)))
            if road_id in seen:
                continue
            seen.add(road_id)
            roads.append({"from": source, "to": target, "cost": cost})

    return {"cities": ciudades, "roads": roads}


