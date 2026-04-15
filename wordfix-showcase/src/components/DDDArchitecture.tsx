import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import {
  type FileTreeNode, DDD_LAYER_COLORS, dddExplanation,
  monolithTree, authServiceTree, gatewayTree,
} from '../data/architecture';
import { ChevronRight, ChevronDown, File, Folder, FolderOpen } from 'lucide-react';

function TreeNode({ node, depth = 0 }: { node: FileTreeNode; depth?: number }) {
  const [expanded, setExpanded] = useState(depth < 2);
  const hasChildren = node.children && node.children.length > 0;
  const layerColor = node.layer ? DDD_LAYER_COLORS[node.layer] : null;

  return (
    <div>
      <div
        className="flex items-start gap-2 py-1 px-2 rounded-md cursor-pointer tree-item group"
        style={{ paddingLeft: `${depth * 18 + 8}px` }}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        <span className="w-4 h-4 shrink-0 mt-0.5 text-[var(--color-text-muted)]">
          {hasChildren ? (expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />) : <span className="inline-block w-3.5" />}
        </span>

        <span className="shrink-0 mt-0.5">
          {node.type === 'folder' ? (
            expanded
              ? <FolderOpen size={14} style={{ color: layerColor?.border || '#64748b' }} />
              : <Folder size={14} style={{ color: layerColor?.border || '#64748b' }} />
          ) : (
            <File size={13} style={{ color: layerColor?.border || '#475569' }} />
          )}
        </span>

        <span className={`text-[13px] font-mono shrink-0 ${node.type === 'folder' ? 'font-semibold text-[var(--color-text-primary)]' : 'text-[var(--color-text-secondary)]'}`}>
          {node.name}
        </span>

        {layerColor && (
          <span
            className="text-[10px] px-1.5 py-px rounded shrink-0 ml-1 font-medium"
            style={{ background: `${layerColor.border}18`, color: layerColor.text }}
          >
            {layerColor.label}
          </span>
        )}

        {node.description && (
          <span className="text-xs text-[var(--color-text-muted)] ml-auto pl-3 hidden lg:inline opacity-0 group-hover:opacity-100 transition-opacity truncate max-w-[320px]">
            {node.description}
          </span>
        )}
      </div>

      <AnimatePresence>
        {expanded && hasChildren && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="overflow-hidden"
          >
            <div className="tree-line" style={{ marginLeft: `${depth * 18 + 18}px` }}>
              {node.children!.map((child, i) => (
                <TreeNode key={`${child.name}-${i}`} node={child} depth={depth + 1} />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function LayerCard({ layer }: { layer: typeof dddExplanation.layers[0] }) {
  const colors = DDD_LAYER_COLORS[layer.key];
  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="glass-card-sm"
      style={{ borderColor: colors.border }}
    >
      <div className="flex items-center gap-2.5 mb-3">
        <span className="w-2.5 h-2.5 rounded-full shrink-0" style={{ background: colors.border }} />
        <h4 className="text-base font-bold" style={{ color: colors.text }}>{layer.name} qatlami</h4>
      </div>
      <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed mb-3">{layer.description}</p>
      <div className="rounded-lg px-3 py-2 mb-3" style={{ background: 'rgba(255,255,255,0.03)' }}>
        <span className="text-xs font-mono text-[var(--color-text-muted)] leading-relaxed">{layer.files}</span>
      </div>
      <p className="text-xs text-[var(--color-accent-amber)] leading-relaxed">
        <strong>Printsip:</strong> {layer.principle}
      </p>
    </motion.div>
  );
}

export default function DDDArchitecture() {
  const [activeTree, setActiveTree] = useState<'monolith' | 'auth' | 'gateway'>('monolith');
  const trees = { monolith: monolithTree, auth: authServiceTree, gateway: gatewayTree };
  const labels = { monolith: 'Django Monolit', auth: 'Auth Service', gateway: 'API Gateway' };

  return (
    <section id="ddd" className="py-24 px-6 bg-[var(--color-bg-secondary)]">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-6xl mx-auto"
      >
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-4">
          <span className="gradient-text">{dddExplanation.title}</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-12 max-w-3xl mx-auto text-base leading-relaxed">
          {dddExplanation.description}
        </p>

        {/* DDD Layer explanations grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-14">
          {dddExplanation.layers.map((layer) => (
            <LayerCard key={layer.key} layer={layer} />
          ))}
        </div>

        {/* Layer dependency flow */}
        <div className="glass-card mb-14">
          <h3 className="text-lg font-bold text-[var(--color-text-primary)] mb-6 text-center">
            Qatlamlar orasidagi bog'lanish
          </h3>

          {/* Desktop: horizontal flow */}
          <div className="hidden md:flex items-center justify-center gap-3">
            {dddExplanation.layers.map((layer, i) => {
              const colors = DDD_LAYER_COLORS[layer.key];
              return (
                <div key={layer.key} className="contents">
                  <motion.div
                    whileHover={{ scale: 1.03 }}
                    className="px-5 py-3 rounded-xl text-center"
                    style={{ background: colors.bg, border: `1px solid ${colors.border}`, minWidth: 140 }}
                  >
                    <div className="text-sm font-bold mb-0.5" style={{ color: colors.text }}>{layer.name}</div>
                    <div className="text-[10px] text-[var(--color-text-muted)]">
                      {layer.key === 'domain' ? 'Entities, VOs, ABCs' :
                       layer.key === 'application' ? 'Use Cases' :
                       layer.key === 'infrastructure' ? 'ORM, APIs, Tasks' : 'Views, URLs, DI'}
                    </div>
                  </motion.div>
                  {i < dddExplanation.layers.length - 1 && (
                    <svg width="32" height="16" className="shrink-0">
                      <line x1="0" y1="8" x2="22" y2="8" stroke="var(--color-text-muted)" strokeWidth="1" strokeDasharray="3 2" />
                      <polygon points="22,4 32,8 22,12" fill="var(--color-text-muted)" />
                    </svg>
                  )}
                </div>
              );
            })}
          </div>

          {/* Mobile: vertical flow */}
          <div className="flex md:hidden flex-col items-center gap-2">
            {dddExplanation.layers.map((layer, i) => {
              const colors = DDD_LAYER_COLORS[layer.key];
              return (
                <div key={layer.key} className="flex flex-col items-center">
                  <div
                    className="px-5 py-3 rounded-xl text-center w-48"
                    style={{ background: colors.bg, border: `1px solid ${colors.border}` }}
                  >
                    <div className="text-sm font-bold" style={{ color: colors.text }}>{layer.name}</div>
                  </div>
                  {i < dddExplanation.layers.length - 1 && (
                    <svg width="16" height="24" className="my-1">
                      <line x1="8" y1="0" x2="8" y2="16" stroke="var(--color-text-muted)" strokeWidth="1" strokeDasharray="3 2" />
                      <polygon points="4,16 8,24 12,16" fill="var(--color-text-muted)" />
                    </svg>
                  )}
                </div>
              );
            })}
          </div>

          <p className="text-center text-xs text-[var(--color-text-muted)] mt-6 leading-relaxed">
            Dependency Rule: Presentation &rarr; Application &rarr; Domain &larr; Infrastructure
          </p>
        </div>

        {/* File tree browser */}
        <div className="glass-card">
          {/* Header + tabs */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-6">
            <h3 className="text-lg font-bold text-[var(--color-text-primary)]">Fayl strukturasi</h3>
            <div className="flex gap-2">
              {(Object.keys(trees) as Array<keyof typeof trees>).map((key) => (
                <button
                  key={key}
                  onClick={() => setActiveTree(key)}
                  className={`btn text-sm py-1.5 px-4 ${
                    activeTree === key ? 'btn-primary' : 'btn-ghost'
                  }`}
                >
                  {labels[key]}
                </button>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-x-5 gap-y-2 mb-5 pb-4 border-b border-[var(--color-border-glass)]">
            {Object.entries(DDD_LAYER_COLORS).map(([, val]) => (
              <div key={val.label} className="flex items-center gap-1.5 text-xs">
                <span className="w-2 h-2 rounded-sm shrink-0" style={{ background: val.border }} />
                <span style={{ color: val.text }}>{val.label}</span>
              </div>
            ))}
          </div>

          {/* Tree content */}
          <div className="overflow-x-auto max-h-[550px] overflow-y-auto">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTree}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                transition={{ duration: 0.2 }}
              >
                <TreeNode node={trees[activeTree]} />
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Summary */}
          <div className="mt-5 pt-4 border-t border-[var(--color-border-glass)]">
            <p className="text-xs text-[var(--color-text-muted)] text-center leading-relaxed">
              {activeTree === 'monolith' && '3 ta bounded context (users, words, immersive), har biri to\'rt qatlamli DDD. 50+ test fayl, 9 ta repository, 12 ta view modul.'}
              {activeTree === 'auth' && 'Monolith bilan bir xil DDD pattern — FastAPI + SQLAlchemy. HTTP va gRPC ikkala transport qatlami. Django-mos parol xeshlash.'}
              {activeTree === 'gateway' && 'DDD qo\'llamaydi — domain logika yo\'q. Faqat routing + proxy. AUTH_PATHS orqali aqlli yo\'naltirish.'}
            </p>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
