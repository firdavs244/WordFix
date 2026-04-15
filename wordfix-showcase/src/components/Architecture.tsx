import { motion } from 'framer-motion';
import { useState } from 'react';
import { services, connections, CATEGORY_COLORS, type ServiceNode } from '../data/architecture';

function ServiceBox({ node, isHovered, onHover }: { node: ServiceNode; isHovered: boolean; onHover: (id: string | null) => void }) {
  const colors = CATEGORY_COLORS[node.category];
  return (
    <motion.g onMouseEnter={() => onHover(node.id)} onMouseLeave={() => onHover(null)} style={{ cursor: 'pointer' }}>
      <motion.rect
        x={node.x - 70} y={node.y - 22} width={140} height={44} rx={10}
        fill={colors.bg} stroke={colors.border} strokeWidth={isHovered ? 2 : 1}
        animate={{ filter: isHovered ? `drop-shadow(0 0 12px ${colors.glow})` : 'none' }}
      />
      <text x={node.x} y={node.y + 1} textAnchor="middle" fill={colors.text} fontSize={13} fontWeight={600}>{node.name}</text>
      <text x={node.x} y={node.y + 16} textAnchor="middle" fill={colors.text} fontSize={9} opacity={0.7}>{node.port !== '-' ? `:${node.port}` : node.tech.split('+')[0]}</text>
    </motion.g>
  );
}

function ConnectionLine({ from, to, label }: { from: ServiceNode; to: ServiceNode; label?: string }) {
  const midX = (from.x + to.x) / 2;
  const midY = (from.y + to.y) / 2;
  return (
    <g>
      <line x1={from.x} y1={from.y + 22} x2={to.x} y2={to.y - 22} stroke="rgba(99,102,241,0.2)" strokeWidth={1} strokeDasharray="6 4" style={{ animation: 'dash-flow 1s linear infinite' }} />
      {label && <text x={midX} y={midY} textAnchor="middle" fill="#64748b" fontSize={9}>{label}</text>}
    </g>
  );
}

export default function Architecture() {
  const [hovered, setHovered] = useState<string | null>(null);
  const hoveredNode = services.find((s) => s.id === hovered);

  return (
    <section id="architecture" className="py-28 px-6">
      <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-5">
          <span className="gradient-text">Tizim Arxitekturasi</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-14 max-w-2xl mx-auto text-base leading-relaxed">
          11 ta o'zaro bog'langan servis — mikroservis arxitektura, alohida autentifikatsiya,
          API Gateway pattern va asinxron vazifalar ishlashi.
        </p>

        <div className="glass-card relative overflow-hidden">
          <div className="flex flex-wrap justify-center gap-8 mb-8">
            {Object.entries(CATEGORY_COLORS).map(([key, val]) => (
              <div key={key} className="flex items-center gap-2.5 text-sm">
                <span className="w-3 h-3 rounded-full" style={{ background: val.border }} />
                <span className="text-[var(--color-text-secondary)] capitalize">
                  {key === 'frontend' ? 'Frontend' : key === 'backend' ? 'Backend' : key === 'database' ? 'Ma\'lumotlar bazasi' : 'Infratuzilma'}
                </span>
              </div>
            ))}
          </div>

          <svg viewBox="0 0 950 600" className="w-full" style={{ minHeight: 450 }}>
            {connections.map((conn, i) => {
              const from = services.find((s) => s.id === conn.from)!;
              const to = services.find((s) => s.id === conn.to)!;
              return <ConnectionLine key={i} from={from} to={to} label={conn.label} />;
            })}
            {services.map((node) => (
              <ServiceBox key={node.id} node={node} isHovered={hovered === node.id} onHover={setHovered} />
            ))}
          </svg>

          {hoveredNode && (
            <motion.div
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
              className="mt-6 p-5 rounded-xl border"
              style={{ borderColor: CATEGORY_COLORS[hoveredNode.category].border, background: CATEGORY_COLORS[hoveredNode.category].bg }}
            >
              <div className="flex items-center gap-3 mb-2">
                <span className="w-2.5 h-2.5 rounded-full" style={{ background: CATEGORY_COLORS[hoveredNode.category].border }} />
                <span className="font-semibold text-lg text-[var(--color-text-primary)]">{hoveredNode.name}</span>
                <span className="text-xs text-[var(--color-text-muted)] ml-auto font-mono">{hoveredNode.tech}</span>
              </div>
              <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">{hoveredNode.description}</p>
            </motion.div>
          )}
        </div>
      </motion.div>
    </section>
  );
}
