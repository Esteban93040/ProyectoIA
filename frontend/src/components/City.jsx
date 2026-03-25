import { Text } from "@react-three/drei";

const CITY_COLORS = {
  current: "#f4d35e",
  open: "#4d9de0",
  visited: "#e63946",
  path: "#56c271",
  default: "#c7c9d1",
};

function City({ name, position, state }) {
  const color = CITY_COLORS[state] || CITY_COLORS.default;

  return (
    <group position={position}>
      <mesh castShadow>
        <sphereGeometry args={[0.35, 24, 24]} />
        <meshStandardMaterial color={color} roughness={0.35} metalness={0.15} />
      </mesh>
      <Text
        position={[0, 0.58, 0]}
        fontSize={0.22}
        color="#f4f5f8"
        anchorX="center"
        anchorY="middle"
      >
        {name}
      </Text>
    </group>
  );
}

export default City;
