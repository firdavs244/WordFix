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
        className="flex items-start gap-2 py-1.5 px-2 rounded-md cursor-pointer transition-colors tree-item hover:bg-white/5 group"
        style={{ paddingLeft: `${depth * 20 + 8}px` }}
        onClick={() => hasChildren && setExpanded(!expanded)}
      >
        {/* Expand/collapse icon */}
        <span className="w-4 h-4 shrink-0 mt-0.5 text-[var(--color-text-muted)]">
          {hasChildren ? (
            expanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />
          ) : <span className="w-3.5" />}
        </span>

        {/* File/folder icon */}
        <span className="shrink-0 mt-0.5">
          {node.type === 'folder' ? (
            expanded ? <FolderOpen size={15} style={{ color: layerColor?.border || '#64748b' }} /> : <Folder size={15} style={{ color: layerColor?.border || '#64748b' }} />
          ) : (
            <File size={14} style={{ color: layerColor?.border || '#475569' }} />
          )}
        </span>

        {/* Name */}
        <span className={`text-sm font-mono shrink-0 ${node.type === 'folder' ? 'font-semibold text-[var(--color-text-primary)]' : 'text-[var(--color-text-secondary)]'}`}>
          {node.name}
        </span>

        {/* Layer badge */}
        {layerColor && (
          <span className="text-[10px] px-1.5 py-0.5 rounded shrink-0 ml-1 mt-0.5" style={{ background: `${layerColor.border}15`, color: layerColor.text }}>
            {layerColor.label}
          </span>
        )}

        {/* Description */}
        {node.description && (
          <span className="text-xs text-[var(--color-text-muted)] ml-2 mt-0.5 hidden md:inline opacity-0 group-hover:opacity-100 transition-opacity leading-snug">
            {node.description}
          </span>
        )}
      </div>

      {/* Children */}
      <AnimatePresence>
        {expanded && hasChildren && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }} transition={{ duration: 0.2 }}>
            <div className="tree-line" style={{ marginLeft: `${depth * 20 + 18}px` }}>
              {node.children!.map((child, i) => <TreeNode key={`${child.name}-${i}`} node={child} depth={depth + 1} />)}
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
    <motion.div initial={{ opacity: 0, y: 15 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="glass-card" style={{ borderColor: colors.border }}>
      <div className="flex items-center gap-3 mb-3">
        <span className="w-3 h-3 rounded-full" style={{ background: colors.border }} />
        <h4 className="text-base font-bold" style={{ color: colors.text }}>{layer.name} qatlami</h4>
      </div>
      <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed mb-3">{layer.description}</p>
      <div className="bg-white/5 rounded-lg px-3 py-2 mb-3">
        <span className="text-xs font-mono text-[var(--color-text-muted)]">{layer.files}</span>
      </div>
      <p className="text-xs text-[var(--color-accent-amber)] leading-relaxed">Printsip: {layer.principle}</p>
    </motion.div>
  );
}

export default function DDDArchitecture() {
  const [activeTree, setActiveTree] = useState<'monolith' | 'auth' | 'gateway'>('monolith');
  const trees = { monolith: monolithTree, auth: authServiceTree, gateway: gatewayTree };
  const labels = { monolith: 'Django Monolit', auth: 'Auth Service', gateway: 'API Gateway' };

  return (
    <section id="ddd" className="py-28 px-6 bg-[var(--color-bg-secondary)]">
      <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-5">
          <span className="gradient-text">{dddExplanation.title}</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-14 max-w-3xl mx-auto text-base leading-relaxed">
          {dddExplanation.description}
        </p>

        {/* DDD Layer explanations */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-16">
          {dddExplanation.layers.map((layer) => <LayerCard key={layer.key} layer={layer} />)}
        </div>

        {/* Layer flow diagram */}
        <div className="glass-card mb-16">
          <h3 className="text-xl font-bold text-[var(--color-text-primary)] mb-6 text-center">Qatlamlar orasidagi bog'lanish</h3>
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-0">
            {dddExplanation.layers.map((layer, i) => {
              const colors = DDD_LAYER_COLORS[layer.key];
              return (
                <div key={layer.key} className="flex items-center gap-4">
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    className="px-6 py-4 rounded-xl text-center min-w-[160px]"
                    style={{ background: colors.bg, border: `1px solid ${colors.border}` }}
                  >
                    <div className="text-sm font-bold mb-1" style={{ color: colors.text }}>{layer.name}</div>
                    <div className="text-[10px] text-[var(--color-text-muted)]">
                      {layer.key === 'domain' ? 'Entities, VOs, ABCs' : layer.key === 'application' ? 'Use Cases' : layer.key === 'infrastructure' ? 'ORM, APIs, Tasks' : 'Views, URLs, DI'}
                    </div>
                  </motion.div>
                  {i < dddExplanation.layers.length - 1 && (
                    <svg width="40" height="20" className="hidden md:block shrink-0"><line x1="0" y1="10" x2="30" y2="10" stroke="var(--color-text-muted)" strokeWidth="1" strokeDasharray="4 3" /><polygon points="30,5 40,10 30,15" fill="var(--color-text-muted)" /></svg>
                  )}
                </div>
              );
            })}
          </div>
          <p className="text-center text-xs text-[var(--color-text-muted)] mt-6">
            Dependency Rule: har bir qatlam faqat o'zidan yuqoridagi qatlamga bog'langan. Presentation → Application → Domain ← Infrastructure
          </p>
        </div>

        {/* File tree browser */}
        <div className="glass-card">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-6">
            <h3 className="text-xl font-bold text-[var(--color-text-primary)]">Fayl strukturasi</h3>
            <div className="flex gap-2">
              {(Object.keys(trees) as Array<keyof typeof trees>).map((key) => (
                <button
                  key={key}
                  onClick={() => setActiveTree(key)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTree === key ? 'bg-gradient-to-r from-[var(--color-accent-blue)] to-[var(--color-accent-purple)] text-white' : 'bg-white/5 text-[var(--color-text-secondary)] hover:bg-white/10'}`}
                >
                  {labels[key]}
                </button>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="flex flex-wrap gap-4 mb-5 pb-5 border-b border-[var(--color-border-glass)]">
            {Object.entries(DDD_LAYER_COLORS).map(([key, val]) => (
              <div key={key} className="flex items-center gap-2 text-xs">
                <span className="w-2.5 h-2.5 rounded-sm" style={{ background: val.border }} />
                <span style={{ color: val.text }}>{val.label}</span>
              </div>
            ))}
          </div>

          {/* Tree */}
          <div className="font-mono text-sm overflow-x-auto max-h-[600px] overflow-y-auto pr-2">
            <AnimatePresence mode="wait">
              <motion.div key={activeTree} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }} transition={{ duration: 0.2 }}>
                <TreeNode node={trees[activeTree]} />
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Details below tree */}
          <div className="mt-6 pt-5 border-t border-[var(--color-border-glass)]">
            <p className="text-xs text-[var(--color-text-muted)] text-center leading-relaxed">
              {activeTree === 'monolith' && 'Django monolit 3 ta bounded context (users, words, immersive) ga ega, har biri to\'rt qatlamli DDD strutukraga ega. 50+ test fayl, 9 ta repository, 12 ta view modul.'}
              {activeTree === 'auth' && 'Auth service monolith bilan bir xil DDD pattern, lekin FastAPI + SQLAlchemy bilan. HTTP va gRPC ikkala transport qatlamiga ega. Django bilan mos parol xeshlash.'}
              {activeTree === 'gateway' && 'API Gateway DDD qo\'llamaydi chunki domain logika yo\'q. Faqat routing + proxy. AUTH_PATHS orqali aqlli yo\'naltirish qiladi.'}
            </p>
          </div>
        </div>
      </motion.div>
    </section>
  );
}
