import Game from "./components/Game";

function App() {
  return (
    <div className="app-root">
      <header className="app-header">
        <h1>A* Pathfinder: Colombia Ops</h1>
        <p>Visualiza A* paso a paso como una simulacion estilo videojuego.</p>
      </header>
      <Game />
    </div>
  );
}

export default App;
