import Game from "./components/Game";

function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <h1>Search Pathfinder: Colombia Ops</h1>
        <p>Visualiza A*, BFS y BCU paso a paso como una simulacion estilo videojuego.</p>
      </header>
      <Game />
    </div>
  );
}

export default App;
