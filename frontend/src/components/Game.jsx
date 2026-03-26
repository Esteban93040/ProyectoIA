import { useEffect, useMemo, useState } from "react";
import Scene from "./Scene";
import { useAStar } from "../hooks/useAStar";

const ALGORITHM_LABELS = {
  astar: "A*",
  bfs: "BFS",
  bcu: "BCU",
  dfs: "DFS",
};

function Game() {
  const { graph, result, runSearch, loading, error } = useAStar();

  const cityList = useMemo(() => Object.keys(graph.cities || {}), [graph.cities]);

  const [start, setStart] = useState("");
  const [goal, setGoal] = useState("");
  const [algorithm, setAlgorithm] = useState("astar");
  const [stepIndex, setStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speedMs, setSpeedMs] = useState(700);

  useEffect(() => {
    if (cityList.length > 1 && !start && !goal) {
      setStart(cityList[0]);
      setGoal(cityList[1]);
    }
  }, [cityList, start, goal]);

  const steps = result?.steps || [];
  const currentStep = steps[stepIndex] || null;
  const animationFinished = steps.length > 0 && stepIndex >= steps.length - 1;
  const finalPath = animationFinished ? result?.path || [] : [];

  useEffect(() => {
    if (!isPlaying || steps.length === 0) return undefined;

    const timer = setTimeout(() => {
      setStepIndex((prev) => {
        if (prev >= steps.length - 1) {
          setIsPlaying(false);
          return prev;
        }
        return prev + 1;
      });
    }, speedMs);

    return () => clearTimeout(timer);
  }, [isPlaying, stepIndex, speedMs, steps.length]);

  const handleRun = async () => {
    if (!start || !goal) return;
    const data = await runSearch(algorithm, start, goal);
    if (data) {
      setStepIndex(0);
      setIsPlaying(true);
    }
  };

  const handleReset = () => {
    setStepIndex(0);
    setIsPlaying(false);
  };

  const openSet = new Set(currentStep?.open_set || []);
  const visitedSet = new Set(currentStep?.visited || []);

  return (
    <section className="game-layout">
      <aside className="hud-panel">
        <h2>Control de simulacion</h2>

        <div className="field-row">
          <label htmlFor="algorithm-select">Algoritmo</label>
          <select
            id="algorithm-select"
            value={algorithm}
            onChange={(event) => setAlgorithm(event.target.value)}
          >
            <option value="astar">A*</option>
            <option value="bfs">BFS</option>
            <option value="bcu">BCU</option>
            <option value="dfs">DFS</option>
          </select>
        </div>

        <div className="field-row">
          <label htmlFor="start-city">Inicio</label>
          <select
            id="start-city"
            value={start}
            onChange={(event) => setStart(event.target.value)}
          >
            {cityList.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
        </div>

        <div className="field-row">
          <label htmlFor="goal-city">Meta</label>
          <select
            id="goal-city"
            value={goal}
            onChange={(event) => setGoal(event.target.value)}
          >
            {cityList.map((city) => (
              <option key={city} value={city}>
                {city}
              </option>
            ))}
          </select>
        </div>

        <div className="field-row">
          <label htmlFor="speed-range">Velocidad ({speedMs} ms/paso)</label>
          <input
            id="speed-range"
            type="range"
            min="120"
            max="1800"
            step="20"
            value={speedMs}
            onChange={(event) => setSpeedMs(Number(event.target.value))}
          />
        </div>

        <div className="button-row">
          <button type="button" onClick={handleRun} disabled={loading || !start || !goal}>
            {loading ? "Calculando..." : `Iniciar ${ALGORITHM_LABELS[algorithm] || "Busqueda"}`}
          </button>
          <button
            type="button"
            onClick={() => setIsPlaying((prev) => !prev)}
            disabled={steps.length === 0}
          >
            {isPlaying ? "Pausar" : "Reanudar"}
          </button>
          <button type="button" onClick={handleReset} disabled={steps.length === 0}>
            Reiniciar
          </button>
        </div>

        <div className="status-card">
          <p>Algoritmo: {ALGORITHM_LABELS[algorithm] || "-"}</p>
          <p>Paso: {steps.length === 0 ? "-" : `${stepIndex + 1} / ${steps.length}`}</p>
          <p>Actual: {currentStep?.current || "-"}</p>
          <p>Costo final: {result?.cost ? result.cost.toFixed(2) : "-"}</p>
          <p>Saltos (BFS): {result?.hops ?? "-"}</p>
          <p>Camino: {result?.path ? result.path.join(" -> ") : "-"}</p>
          {error ? <p className="error-text">{error}</p> : null}
        </div>

        <div className="legend">
          <h3>Leyenda</h3>
          <p><span className="dot current" /> Nodo actual (amarillo)</p>
          <p><span className="dot open" /> Open set (azul)</p>
          <p><span className="dot visited" /> Visitados (rojo)</p>
          <p><span className="dot path" /> Camino final (verde)</p>
        </div>
      </aside>

      <div className="scene-wrap">
        <Scene
          cities={graph.cities || {}}
          roads={graph.roads || []}
          current={currentStep?.current || ""}
          openSet={openSet}
          visitedSet={visitedSet}
          finalPath={finalPath}
        />
      </div>
    </section>
  );
}

export default Game;
