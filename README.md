# A* Visualizer Web App

Proyecto completo para visualizar el algoritmo A* como videojuego:

- Backend en FastAPI.
- Frontend en React + Vite.
- Visualizacion 3D con Three.js via React Three Fiber.

## Estructura

```text
backend/
  Astar.py
  AstarCopy.py
  bfs.py
  bcu.py
  dfs.py
  main.py
  proyecto.py
  requirements.txt
frontend/
  index.html
  package.json
  vite.config.js
  .env.example
  src/
    App.jsx
    main.jsx
    styles.css
    hooks/
      useAStar.js
    components/
      City.jsx
      Road.jsx
      Scene.jsx
      Game.jsx
```

## Backend

### 1) Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 2) Ejecutar API

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Endpoints

- `GET /health`: estado del servicio.
- `GET /graph`: grafo (ciudades y carreteras).
- `POST /astar`: ejecuta A*.

Ejemplo de body para `/astar`:

```json
{
  "start": "Pasto",
  "goal": "Barranquilla"
}
```

Respuesta:

```json
{
  "path": ["Pasto", "Popayan", "Cali"],
  "cost": 267.9791,
  "steps": [
    {
      "current": "Pasto",
      "open_set": ["Pasto"],
      "visited": [],
      "g": {"Pasto": 0},
      "f": {"Pasto": 1112.35}
    }
  ]
}
```

## Frontend

### 1) Instalar dependencias

```bash
cd frontend
npm install
```

### 2) Configurar URL del backend (opcional)

```bash
cp .env.example .env
```

### 3) Ejecutar app

```bash
npm run dev
```

Abrir `http://localhost:5173`.

## Flujo de visualizacion

- Nodo actual: amarillo.
- Open set: azul.
- Visitados: rojo.
- Camino final: verde.
- Slider para velocidad de animacion por pasos.

## Arquitectura modular

- `useAStar`: hook para consumir backend.
- `Game`: HUD, controles y estado de simulacion.
- `Scene`: escena 3D y orquestacion de nodos/carreteras.
- `City`: render de ciudad (esfera + etiqueta).
- `Road`: render de conexion (linea).
