import { Canvas } from "@react-three/fiber";
import { OrbitControls, Stars } from "@react-three/drei";
import City from "./City";
import Road from "./Road";

const toWorldPosition = (city) => {
  const x = city.longitud * 1.35;
  const y = city.latitud * 1.35;
  return [x, y, 0];
};

const buildCenteredPositions = (cities) => {
  const names = Object.keys(cities);
  if (names.length === 0) return {};

  const rawPositions = names.reduce((acc, name) => {
    acc[name] = toWorldPosition(cities[name]);
    return acc;
  }, {});

  const xs = names.map((name) => rawPositions[name][0]);
  const ys = names.map((name) => rawPositions[name][1]);
  const centerX = (Math.min(...xs) + Math.max(...xs)) / 2;
  const centerY = (Math.min(...ys) + Math.max(...ys)) / 2;

  return names.reduce((acc, name) => {
    const [x, y, z] = rawPositions[name];
    acc[name] = [x - centerX, y - centerY, z];
    return acc;
  }, {});
};

const buildPathEdgeSet = (path) => {
  const edges = new Set();
  if (!Array.isArray(path)) return edges;

  for (let i = 0; i < path.length - 1; i += 1) {
    const key = [path[i], path[i + 1]].sort().join("::");
    edges.add(key);
  }
  return edges;
};

function Scene({ cities, roads, current, openSet, visitedSet, finalPath }) {
  const cityNames = Object.keys(cities);
  const cityPositions = buildCenteredPositions(cities);

  const pathNodeSet = new Set(finalPath || []);
  const pathEdgeSet = buildPathEdgeSet(finalPath);

  const getCityState = (cityName) => {
    if (cityName === current) return "current";
    if (pathNodeSet.has(cityName)) return "path";
    if (openSet.has(cityName)) return "open";
    if (visitedSet.has(cityName)) return "visited";
    return "default";
  };

  return (
    <Canvas orthographic camera={{ position: [0, 20, 100], zoom: 48 }}>
      <color attach="background" args={["#0f1420"]} />
      <fog attach="fog" args={["#0f1420", 80, 200]} />

      <ambientLight intensity={0.65} />
      <directionalLight
        intensity={0.75}
        position={[0, 0, 50]}
      />
      <pointLight intensity={0.35} position={[-20, -8, 30]} color="#9fd4ff" />

      <Stars radius={180} depth={45} count={2600} factor={4} fade speed={0.4} />

      {roads.map((road) => {
        const from = cityPositions[road.from];
        const to = cityPositions[road.to];
        if (!from || !to) return null;

        const key = [road.from, road.to].sort().join("::");
        return <Road key={`${road.from}-${road.to}`} start={from} end={to} isPath={pathEdgeSet.has(key)} />;
      })}

      {cityNames.map((cityName) => (
        <City
          key={cityName}
          name={cityName}
          position={cityPositions[cityName]}
          state={getCityState(cityName)}
        />
      ))}

      <mesh position={[0, 0, -1.6]}>
        <circleGeometry args={[160, 64]} />
        <meshStandardMaterial color="#161f33" transparent opacity={0.85} />
      </mesh>

      <OrbitControls
        enablePan={false}
        enableZoom={false}
        enableRotate={false}
      />
    </Canvas>
  );
}

export default Scene;
