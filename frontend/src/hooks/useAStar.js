import { useCallback, useEffect, useMemo, useState } from "react";

const DEFAULT_API_URL = "http://127.0.0.1:8000";
const SUPPORTED_ALGORITHMS = new Set(["astar", "bfs", "bcu", "dfs"]);

export function useAStar() {
  const apiUrl = useMemo(
    () => import.meta.env.VITE_API_URL || DEFAULT_API_URL,
    []
  );

  const [graph, setGraph] = useState({ cities: {}, roads: [] });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchGraph = useCallback(async () => {
    setError("");
    try {
      const response = await fetch(`${apiUrl}/graph`);
      if (!response.ok) {
        throw new Error("No se pudo obtener el grafo");
      }
      const data = await response.json();
      setGraph(data);
      return data;
    } catch (requestError) {
      setError(requestError.message);
      return null;
    }
  }, [apiUrl]);

  const runSearch = useCallback(
    async (algorithm, start, goal) => {
      setLoading(true);
      setError("");
      try {
        const normalizedAlgorithm = String(algorithm || "astar").toLowerCase();
        const endpoint = SUPPORTED_ALGORITHMS.has(normalizedAlgorithm)
          ? normalizedAlgorithm
          : "astar";

        const response = await fetch(`${apiUrl}/${endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ start, goal }),
        });

        if (!response.ok) {
          const details = await response.json().catch(() => ({}));
          throw new Error(details.detail || "Error ejecutando busqueda");
        }

        const data = await response.json();
        setResult(data);
        return data;
      } catch (requestError) {
        setError(requestError.message);
        setResult(null);
        return null;
      } finally {
        setLoading(false);
      }
    },
    [apiUrl]
  );

  useEffect(() => {
    fetchGraph();
  }, [fetchGraph]);

  return {
    apiUrl,
    graph,
    result,
    loading,
    error,
    fetchGraph,
    runSearch,
  };
}
