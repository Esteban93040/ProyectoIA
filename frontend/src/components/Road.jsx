import { Line } from "@react-three/drei";

function Road({ start, end, isPath }) {
  return (
    <Line
      points={[start, end]}
      color={isPath ? "#56c271" : "#7b859f"}
      lineWidth={isPath ? 3.2 : 1.2}
      transparent
      opacity={isPath ? 0.95 : 0.45}
    />
  );
}

export default Road;
