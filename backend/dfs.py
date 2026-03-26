
def dfs(graph, start, goal):

    if start not in graph or goal not in graph:
        print("Error: ciudad no encontrada")
        return None, None


    stack = []
    stack.append((start, [start], 0))

    visitados = set()

    while stack:

        nodo, camino, costo = stack.pop()

      
        if nodo in visitados:
            continue

        visitados.add(nodo)

       
        if nodo == goal:
            return camino, costo

        vecinos = graph.get(nodo, [])

        
        for vecino, peso in reversed(vecinos):

            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                nuevo_costo = costo + peso

                stack.append((vecino, nuevo_camino, nuevo_costo))

    return None, None


def dfs_steps(start, goal):

    if start not in graph or goal not in graph:
        return None, None, []

    stack = []
    stack.append((start, [start], 0))

    visitados = set()
    steps = []

    while stack:

        nodo, camino, costo = stack.pop()

        if nodo in visitados:
            continue


        steps.append({
            "current": nodo,
            "open_set": [n for n, _, _ in stack],
            "visited": list(visitados)
        })

        visitados.add(nodo)

        if nodo == goal:
            return camino, costo, steps

        vecinos = graph.get(nodo, [])

        for vecino, peso in reversed(vecinos):

            if vecino not in visitados:
                nuevo_camino = camino + [vecino]
                nuevo_costo = costo + peso

                stack.append((vecino, nuevo_camino, nuevo_costo))

    return None, None, steps


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


# prueba rápida
if __name__ == "__main__":
    camino, costo = dfs(graph, 'Cali', 'Bogota')

    print("Camino encontrado:", camino)
    print("Costo total:", costo)