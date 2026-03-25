from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from AstarCopy import a_star_steps, get_graph_data
from bcu import uniform_cost_search_steps
from bfs import bfs_steps


class AStarRequest(BaseModel):
    start: str
    goal: str


app = FastAPI(title="A* Visualizer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/graph")
def get_graph():
    return get_graph_data()


@app.post("/astar")
def run_astar(payload: AStarRequest):
    graph = get_graph_data()
    cities = graph["cities"]

    if payload.start not in cities:
        raise HTTPException(status_code=400, detail=f"Ciudad inicio invalida: {payload.start}")
    if payload.goal not in cities:
        raise HTTPException(status_code=400, detail=f"Ciudad destino invalida: {payload.goal}")

    path, cost, steps = a_star_steps(payload.start, payload.goal)
    if path is None:
        raise HTTPException(status_code=404, detail="No se encontro camino entre las ciudades")

    return {
        "path": path,
        "cost": cost,
        "steps": steps,
    }


@app.get("/astar")
def run_astar_get(start: str, goal: str):
    return run_astar(AStarRequest(start=start, goal=goal))


@app.post("/bcu")
def run_bcu(payload: AStarRequest):
    graph = get_graph_data()
    cities = graph["cities"]

    if payload.start not in cities:
        raise HTTPException(status_code=400, detail=f"Ciudad inicio invalida: {payload.start}")
    if payload.goal not in cities:
        raise HTTPException(status_code=400, detail=f"Ciudad destino invalida: {payload.goal}")

    path, cost, steps = uniform_cost_search_steps(payload.start, payload.goal)
    if path is None:
        raise HTTPException(status_code=404, detail="No se encontro camino entre las ciudades")

    return {
        "path": path,
        "cost": cost,
        "steps": steps,
    }


@app.get("/bcu")
def run_bcu_get(start: str, goal: str):
    return run_bcu(AStarRequest(start=start, goal=goal))


@app.post("/bfs")
def run_bfs(payload: AStarRequest):
    graph = get_graph_data()
    cities = graph["cities"]

    if payload.start not in cities:
        raise HTTPException(status_code=400, detail=f"Ciudad inicio invalida: {payload.start}")
    if payload.goal not in cities:
        raise HTTPException(status_code=400, detail=f"Ciudad destino invalida: {payload.goal}")

    path, cost, hops, steps = bfs_steps(payload.start, payload.goal)
    if path is None:
        raise HTTPException(status_code=404, detail="No se encontro camino entre las ciudades")

    return {
        "path": path,
        "cost": cost,
        "hops": hops,
        "steps": steps,
    }


@app.get("/bfs")
def run_bfs_get(start: str, goal: str):
    return run_bfs(AStarRequest(start=start, goal=goal))