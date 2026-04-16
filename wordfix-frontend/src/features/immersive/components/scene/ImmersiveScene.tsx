/**
 * 3D Scene component using React Three Fiber.
 * Sprint 15 — Shadows, new scenes (hospital, school, hotel, shop, bank, park, gym), improved NPC visuals.
 */

import { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Environment, Text, Box, Plane, Sphere, Cylinder } from '@react-three/drei';
import { PCFShadowMap } from 'three';
import type { SceneConfig } from '../../types/immersive';
import type { Group } from 'three';

interface Props {
  environment: string;
  sceneConfig?: SceneConfig;
  npcName: string;
}

/** Reusable NPC character with idle animation */
function NPCCharacter({ name, position, bodyColor = '#4a69bd', labelColor = '#333' }: {
  name: string;
  position: [number, number, number];
  bodyColor?: string;
  labelColor?: string;
}) {
  const groupRef = useRef<Group>(null);
  const elapsed = useRef(0);

  // Gentle idle sway
  useFrame((_, delta) => {
    elapsed.current += delta;
    if (groupRef.current) {
      groupRef.current.rotation.y = Math.sin(elapsed.current * 0.5) * 0.05;
      groupRef.current.position.y = position[1] + Math.sin(elapsed.current * 1.2) * 0.015;
    }
  });

  return (
    <group ref={groupRef} position={position}>
      {/* Head */}
      <Sphere args={[0.22, 24, 24]} position={[0, 0.55, 0]} castShadow>
        <meshStandardMaterial color="#FDBCB4" roughness={0.6} />
      </Sphere>
      {/* Neck */}
      <Cylinder args={[0.06, 0.06, 0.12, 8]} position={[0, 0.3, 0]}>
        <meshStandardMaterial color="#FDBCB4" roughness={0.6} />
      </Cylinder>
      {/* Body */}
      <Box args={[0.45, 0.55, 0.28]} position={[0, 0, 0]} castShadow>
        <meshStandardMaterial color={bodyColor} roughness={0.5} metalness={0.1} />
      </Box>
      {/* Arms */}
      <Box args={[0.12, 0.45, 0.12]} position={[-0.3, -0.02, 0]} castShadow>
        <meshStandardMaterial color={bodyColor} roughness={0.5} />
      </Box>
      <Box args={[0.12, 0.45, 0.12]} position={[0.3, -0.02, 0]} castShadow>
        <meshStandardMaterial color={bodyColor} roughness={0.5} />
      </Box>
      {/* Name label */}
      <Text
        position={[0, 0.92, 0]}
        fontSize={0.13}
        color={labelColor}
        anchorX="center"
        anchorY="bottom"
        outlineWidth={0.01}
        outlineColor="#ffffff"
      >
        {name}
      </Text>
    </group>
  );
}

function OfficeScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[10, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#e8e0d4" roughness={0.8} />
      </Plane>
      <Plane args={[10, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#f5f0e8" roughness={0.9} />
      </Plane>
      {/* Desk */}
      <Box args={[2.5, 0.1, 1.2]} position={[0, 0.85, -2]} castShadow receiveShadow>
        <meshStandardMaterial color="#8B4513" roughness={0.7} metalness={0.05} />
      </Box>
      {[[-1.1, 0.4, -2.5], [1.1, 0.4, -2.5], [-1.1, 0.4, -1.5], [1.1, 0.4, -1.5]].map((pos, i) => (
        <Box key={i} args={[0.08, 0.8, 0.08]} position={pos as [number, number, number]} castShadow>
          <meshStandardMaterial color="#6B3410" roughness={0.8} />
        </Box>
      ))}
      {/* Monitor */}
      <Box args={[0.8, 0.5, 0.05]} position={[-0.5, 1.35, -2.3]} castShadow>
        <meshStandardMaterial color="#222" roughness={0.3} metalness={0.6} />
      </Box>
      {/* Chair */}
      <Box args={[0.6, 0.08, 0.6]} position={[0, 0.55, -0.5]} castShadow>
        <meshStandardMaterial color="#2c3e50" roughness={0.6} />
      </Box>
      <Box args={[0.6, 0.6, 0.05]} position={[0, 0.9, -0.8]} castShadow>
        <meshStandardMaterial color="#2c3e50" roughness={0.6} />
      </Box>
      <NPCCharacter name={npcName} position={[0, 1.5, -2.5]} bodyColor="#4a69bd" />
      {/* Window */}
      <Plane args={[1.5, 1.5]} position={[4.99, 2, -2]}>
        <meshStandardMaterial color="#87CEEB" emissive="#87CEEB" emissiveIntensity={0.3} transparent opacity={0.7} />
      </Plane>
      {/* Bookshelf */}
      <Box args={[1, 2, 0.3]} position={[-4, 1, -4.5]} castShadow>
        <meshStandardMaterial color="#A0522D" roughness={0.7} />
      </Box>
    </group>
  );
}

function RestaurantScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[10, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#2c1810" roughness={0.9} />
      </Plane>
      <Plane args={[10, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#6B2020" roughness={0.8} />
      </Plane>
      {/* Table */}
      <Cylinder args={[0.6, 0.6, 0.05, 32]} position={[0, 0.75, -1.5]} castShadow>
        <meshStandardMaterial color="#f5f5dc" roughness={0.4} metalness={0.1} />
      </Cylinder>
      <Cylinder args={[0.05, 0.05, 0.7, 8]} position={[0, 0.38, -1.5]} castShadow>
        <meshStandardMaterial color="#333" metalness={0.5} />
      </Cylinder>
      {/* Candle */}
      <Cylinder args={[0.02, 0.02, 0.15, 8]} position={[0, 0.85, -1.5]}>
        <meshStandardMaterial color="#f5f5dc" />
      </Cylinder>
      <pointLight position={[0, 1, -1.5]} intensity={0.6} color="#ff9900" distance={3} />
      <NPCCharacter name={npcName} position={[1, 1.2, -2]} bodyColor="#1a1a2e" labelColor="#fff" />
    </group>
  );
}

function AirportScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[15, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#c0c0c0" roughness={0.6} metalness={0.1} />
      </Plane>
      <Plane args={[15, 5]} position={[0, 2.5, -5]} receiveShadow>
        <meshStandardMaterial color="#e8e8e8" roughness={0.9} />
      </Plane>
      {/* Counter */}
      <Box args={[4, 1, 0.5]} position={[0, 0.5, -3]} castShadow receiveShadow>
        <meshStandardMaterial color="#2c3e50" roughness={0.5} metalness={0.3} />
      </Box>
      {/* Screen */}
      <Box args={[2, 0.8, 0.05]} position={[0, 1.3, -3.2]} castShadow>
        <meshStandardMaterial color="#111" roughness={0.2} metalness={0.7} />
      </Box>
      <NPCCharacter name={npcName} position={[0, 1.5, -3.5]} bodyColor="#003366" />
    </group>
  );
}

function HospitalScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[10, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#eef2f5" roughness={0.8} />
      </Plane>
      <Plane args={[10, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#f8f8f8" roughness={0.9} />
      </Plane>
      {/* Examination table */}
      <Box args={[2, 0.15, 0.8]} position={[-1.5, 0.65, -2]} castShadow receiveShadow>
        <meshStandardMaterial color="#dce6f0" roughness={0.5} />
      </Box>
      <Box args={[0.08, 0.6, 0.08]} position={[-2.4, 0.3, -2.3]} castShadow>
        <meshStandardMaterial color="#bbb" metalness={0.6} />
      </Box>
      <Box args={[0.08, 0.6, 0.08]} position={[-0.6, 0.3, -2.3]} castShadow>
        <meshStandardMaterial color="#bbb" metalness={0.6} />
      </Box>
      {/* Desk */}
      <Box args={[1.5, 0.1, 0.8]} position={[2, 0.85, -3]} castShadow>
        <meshStandardMaterial color="#f0ebe3" roughness={0.7} />
      </Box>
      {/* Medical cabinet */}
      <Box args={[0.6, 1.2, 0.3]} position={[-4, 0.8, -4.5]} castShadow>
        <meshStandardMaterial color="#e0e8f0" roughness={0.5} metalness={0.2} />
      </Box>
      <NPCCharacter name={npcName} position={[2, 1.5, -3.5]} bodyColor="#f0f0f0" labelColor="#333" />
    </group>
  );
}

function SchoolScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[10, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#e8dcc0" roughness={0.9} />
      </Plane>
      <Plane args={[10, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#f5efe6" roughness={0.9} />
      </Plane>
      {/* Whiteboard */}
      <Box args={[3, 1.5, 0.05]} position={[0, 2, -4.9]} castShadow>
        <meshStandardMaterial color="#f8f8f8" roughness={0.3} />
      </Box>
      <Box args={[3.2, 1.6, 0.03]} position={[0, 2, -4.92]}>
        <meshStandardMaterial color="#666" roughness={0.6} metalness={0.3} />
      </Box>
      {/* Student desk */}
      <Box args={[1.2, 0.08, 0.6]} position={[0, 0.7, -1]} castShadow receiveShadow>
        <meshStandardMaterial color="#d4a76a" roughness={0.7} />
      </Box>
      <Box args={[0.05, 0.65, 0.05]} position={[-0.55, 0.35, -1.25]} castShadow>
        <meshStandardMaterial color="#777" metalness={0.5} />
      </Box>
      <Box args={[0.05, 0.65, 0.05]} position={[0.55, 0.35, -1.25]} castShadow>
        <meshStandardMaterial color="#777" metalness={0.5} />
      </Box>
      {/* Books on desk */}
      <Box args={[0.25, 0.08, 0.18]} position={[-0.3, 0.78, -0.9]} castShadow>
        <meshStandardMaterial color="#4169E1" roughness={0.7} />
      </Box>
      <NPCCharacter name={npcName} position={[0, 1.5, -3.5]} bodyColor="#8B4513" labelColor="#333" />
    </group>
  );
}

function HotelScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[12, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#d4c5a9" roughness={0.6} />
      </Plane>
      <Plane args={[12, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#f0e6d2" roughness={0.8} />
      </Plane>
      {/* Reception desk */}
      <Box args={[4, 1.1, 0.6]} position={[0, 0.55, -3]} castShadow receiveShadow>
        <meshStandardMaterial color="#5c3a21" roughness={0.6} metalness={0.1} />
      </Box>
      {/* Desk top marble */}
      <Box args={[4.1, 0.05, 0.65]} position={[0, 1.12, -3]} castShadow>
        <meshStandardMaterial color="#e8e0d0" roughness={0.3} metalness={0.2} />
      </Box>
      {/* Bell */}
      <Sphere args={[0.06, 16, 16]} position={[1, 1.2, -2.8]}>
        <meshStandardMaterial color="#ffd700" roughness={0.2} metalness={0.8} />
      </Sphere>
      {/* Plant */}
      <Cylinder args={[0.15, 0.18, 0.35, 8]} position={[3.5, 0.18, -2]}>
        <meshStandardMaterial color="#8B4513" roughness={0.8} />
      </Cylinder>
      <Sphere args={[0.3, 12, 12]} position={[3.5, 0.55, -2]} castShadow>
        <meshStandardMaterial color="#2d8544" roughness={0.8} />
      </Sphere>
      <NPCCharacter name={npcName} position={[0, 1.5, -3.5]} bodyColor="#2c3e50" labelColor="#333" />
    </group>
  );
}

function ShopScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[10, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#f0ebe3" roughness={0.7} />
      </Plane>
      <Plane args={[10, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#faf5ee" roughness={0.9} />
      </Plane>
      {/* Clothing rack */}
      <Cylinder args={[0.03, 0.03, 2, 8]} position={[-2, 1.2, -3]} rotation={[0, 0, Math.PI / 2]} castShadow>
        <meshStandardMaterial color="#888" metalness={0.7} />
      </Cylinder>
      <Cylinder args={[0.03, 0.03, 1.5, 8]} position={[-3, 0.6, -3]} castShadow>
        <meshStandardMaterial color="#888" metalness={0.7} />
      </Cylinder>
      <Cylinder args={[0.03, 0.03, 1.5, 8]} position={[-1, 0.6, -3]} castShadow>
        <meshStandardMaterial color="#888" metalness={0.7} />
      </Cylinder>
      {/* Mannequin */}
      <Cylinder args={[0.12, 0.15, 0.8, 8]} position={[2, 0.6, -3]} castShadow>
        <meshStandardMaterial color="#e8e0d8" roughness={0.5} />
      </Cylinder>
      <Sphere args={[0.12, 16, 16]} position={[2, 1.1, -3]} castShadow>
        <meshStandardMaterial color="#e8e0d8" roughness={0.5} />
      </Sphere>
      {/* Counter */}
      <Box args={[2, 1, 0.5]} position={[0, 0.5, -1]} castShadow receiveShadow>
        <meshStandardMaterial color="#f5f0e8" roughness={0.5} />
      </Box>
      {/* Mirror */}
      <Plane args={[1, 1.8]} position={[4.5, 1.3, -3]}>
        <meshStandardMaterial color="#d0dce6" roughness={0.1} metalness={0.5} />
      </Plane>
      <NPCCharacter name={npcName} position={[0, 1.5, -1.5]} bodyColor="#e67e22" labelColor="#333" />
    </group>
  );
}

function BankScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[12, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#e0d8c8" roughness={0.5} metalness={0.1} />
      </Plane>
      <Plane args={[12, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#f0ebe0" roughness={0.9} />
      </Plane>
      {/* Desk with partition */}
      <Box args={[2, 0.1, 1]} position={[0, 0.85, -2.5]} castShadow receiveShadow>
        <meshStandardMaterial color="#5c3a21" roughness={0.6} />
      </Box>
      <Box args={[0.05, 0.6, 1]} position={[0, 1.45, -2.5]} castShadow>
        <meshStandardMaterial color="#c0cfe0" roughness={0.3} metalness={0.2} transparent opacity={0.6} />
      </Box>
      {/* Computer */}
      <Box args={[0.5, 0.35, 0.03]} position={[0.3, 1.2, -2.8]} castShadow>
        <meshStandardMaterial color="#222" roughness={0.3} metalness={0.5} />
      </Box>
      {/* Documents */}
      <Box args={[0.3, 0.02, 0.2]} position={[-0.5, 0.92, -2.3]} castShadow>
        <meshStandardMaterial color="#fff" roughness={0.9} />
      </Box>
      {/* Nameplate */}
      <Box args={[0.4, 0.1, 0.08]} position={[-0.5, 0.95, -2.0]}>
        <meshStandardMaterial color="#c8a45a" roughness={0.3} metalness={0.6} />
      </Box>
      <NPCCharacter name={npcName} position={[0, 1.5, -3.2]} bodyColor="#1a3a5c" labelColor="#333" />
    </group>
  );
}

function ParkScene({ npcName }: { npcName: string }) {
  return (
    <group>
      {/* Grass */}
      <Plane args={[15, 15]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#5a8f3c" roughness={0.9} />
      </Plane>
      {/* Path */}
      <Plane args={[2, 10]} rotation={[-Math.PI / 2, 0, 0]} position={[0, 0.01, 0]}>
        <meshStandardMaterial color="#c8b898" roughness={0.8} />
      </Plane>
      {/* Bench */}
      <Box args={[1.2, 0.08, 0.4]} position={[2, 0.5, -1.5]} castShadow receiveShadow>
        <meshStandardMaterial color="#8B4513" roughness={0.7} />
      </Box>
      <Box args={[1.2, 0.4, 0.05]} position={[2, 0.75, -1.7]} castShadow>
        <meshStandardMaterial color="#8B4513" roughness={0.7} />
      </Box>
      {/* Tree trunk */}
      <Cylinder args={[0.12, 0.15, 1.5, 8]} position={[-3, 0.75, -3]} castShadow>
        <meshStandardMaterial color="#5c3a21" roughness={0.9} />
      </Cylinder>
      {/* Tree crown */}
      <Sphere args={[0.8, 12, 12]} position={[-3, 1.9, -3]} castShadow>
        <meshStandardMaterial color="#2d6b1e" roughness={0.9} />
      </Sphere>
      {/* Fountain base */}
      <Cylinder args={[0.5, 0.6, 0.4, 16]} position={[0, 0.2, -4]} castShadow receiveShadow>
        <meshStandardMaterial color="#8899aa" roughness={0.5} metalness={0.2} />
      </Cylinder>
      <Cylinder args={[0.08, 0.08, 0.6, 8]} position={[0, 0.6, -4]}>
        <meshStandardMaterial color="#8899aa" roughness={0.4} metalness={0.3} />
      </Cylinder>
      <NPCCharacter name={npcName} position={[1, 1.2, -2]} bodyColor="#3498db" labelColor="#333" />
    </group>
  );
}

function GymScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[12, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#3a3a3a" roughness={0.8} />
      </Plane>
      <Plane args={[12, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#444" roughness={0.7} />
      </Plane>
      {/* Mirror wall */}
      <Plane args={[8, 3]} position={[0, 1.8, -4.9]}>
        <meshStandardMaterial color="#b8c8d8" roughness={0.1} metalness={0.4} />
      </Plane>
      {/* Treadmill base */}
      <Box args={[0.8, 0.15, 1.8]} position={[-3, 0.2, -2]} castShadow receiveShadow>
        <meshStandardMaterial color="#222" roughness={0.5} metalness={0.3} />
      </Box>
      <Box args={[0.06, 1.2, 0.06]} position={[-3, 0.85, -2.85]} castShadow>
        <meshStandardMaterial color="#555" metalness={0.6} />
      </Box>
      {/* Dumbbell rack */}
      <Box args={[1.5, 0.8, 0.3]} position={[3, 0.5, -4]} castShadow>
        <meshStandardMaterial color="#333" roughness={0.6} metalness={0.4} />
      </Box>
      {/* Yoga mat */}
      <Box args={[0.8, 0.02, 1.8]} position={[1, 0.02, -1.5]} receiveShadow>
        <meshStandardMaterial color="#7c3aed" roughness={0.8} />
      </Box>
      {/* Water cooler */}
      <Cylinder args={[0.15, 0.15, 0.8, 8]} position={[4.5, 0.5, -1]}>
        <meshStandardMaterial color="#e0e8f0" roughness={0.4} metalness={0.2} />
      </Cylinder>
      <Cylinder args={[0.18, 0.15, 0.3, 8]} position={[4.5, 1, -1]}>
        <meshStandardMaterial color="#4aa3df" roughness={0.3} metalness={0.1} />
      </Cylinder>
      <NPCCharacter name={npcName} position={[0, 1.2, -2.5]} bodyColor="#e74c3c" labelColor="#fff" />
    </group>
  );
}

function GenericScene({ npcName }: { npcName: string }) {
  return (
    <group>
      <Plane args={[10, 10]} rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
        <meshStandardMaterial color="#d4c5a9" roughness={0.8} />
      </Plane>
      <Plane args={[10, 4]} position={[0, 2, -5]} receiveShadow>
        <meshStandardMaterial color="#e8dcc8" roughness={0.9} />
      </Plane>
      <NPCCharacter name={npcName} position={[0, 1.2, -3]} bodyColor="#555" />
    </group>
  );
}

const SCENE_MAP: Record<string, React.FC<{ npcName: string }>> = {
  office: OfficeScene,
  restaurant: RestaurantScene,
  airport: AirportScene,
  hospital: HospitalScene,
  school: SchoolScene,
  hotel: HotelScene,
  shop: ShopScene,
  bank: BankScene,
  park: ParkScene,
  gym: GymScene,
};

const ENVIRONMENT_PRESETS: Record<string, string> = {
  office: 'apartment',
  restaurant: 'night',
  airport: 'lobby',
  hospital: 'apartment',
  school: 'apartment',
  hotel: 'lobby',
  shop: 'apartment',
  bank: 'lobby',
  park: 'park',
  gym: 'warehouse',
};

export default function ImmersiveScene({ environment, sceneConfig, npcName }: Props) {
  const SceneComponent = SCENE_MAP[environment] || GenericScene;
  const cameraPos = sceneConfig?.camera_position || [0, 2, 5];
  const envPreset = (ENVIRONMENT_PRESETS[environment] || 'apartment') as 'apartment' | 'night' | 'lobby' | 'park' | 'warehouse';

  return (
    <Canvas
      shadows={{ type: PCFShadowMap }}
      camera={{ position: cameraPos, fov: 60 }}
      className="h-full w-full"
      gl={{ antialias: true }}
    >
      <ambientLight intensity={sceneConfig?.ambient_light || 0.5} />
      <directionalLight
        position={[5, 8, 5]}
        intensity={0.9}
        castShadow
        shadow-mapSize-width={1024}
        shadow-mapSize-height={1024}
        shadow-camera-far={20}
        shadow-camera-near={0.1}
        shadow-camera-left={-8}
        shadow-camera-right={8}
        shadow-camera-top={8}
        shadow-camera-bottom={-8}
      />
      <pointLight position={[-3, 3, 2]} intensity={0.3} />

      <SceneComponent npcName={npcName} />

      <Environment preset={envPreset} background={false} />
      <OrbitControls
        enablePan={false}
        maxPolarAngle={Math.PI / 2}
        minDistance={2}
        maxDistance={8}
      />
    </Canvas>
  );
}
