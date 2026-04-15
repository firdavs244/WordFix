import { motion } from 'framer-motion';
import { k8sResources } from '../data/architecture';

function ResourceGroup({ title, icon, color, children }: { title: string; icon: string; color: string; children: React.ReactNode }) {
  return (
    <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="glass-card">
      <div className="flex items-center gap-3 mb-5">
        <span className="w-9 h-9 rounded-lg flex items-center justify-center text-sm font-bold" style={{ background: `${color}20`, color }}>{icon}</span>
        <h3 className="text-lg font-semibold" style={{ color }}>{title}</h3>
      </div>
      <div className="space-y-1.5">{children}</div>
    </motion.div>
  );
}

function StatusDot() {
  return (
    <span className="relative flex h-2.5 w-2.5 shrink-0">
      <span className="absolute inline-flex h-full w-full rounded-full bg-[var(--color-accent-emerald)] opacity-75 animate-ping" />
      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[var(--color-accent-emerald)]" />
    </span>
  );
}

export default function KubernetesInfra() {
  return (
    <section id="kubernetes" className="py-28 px-6 bg-[var(--color-bg-secondary)]">
      <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-5">
          <span className="gradient-text">Kubernetes Infratuzilmasi</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-14 max-w-2xl mx-auto text-base leading-relaxed">
          Ubuntu 24.04 da k3s klaster — 11 pod, doimiy hajmlar (PVC), health probe'lar,
          migratsiya uchun init konteynerlar.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <ResourceGroup title="Deployment'lar (7)" icon="D" color="var(--color-accent-blue)">
            {k8sResources.deployments.map((d) => (
              <div key={d.name} className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition-colors tree-item">
                <StatusDot />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">{d.name}</div>
                  <div className="text-xs text-[var(--color-text-muted)] truncate mt-0.5">{d.image}</div>
                </div>
                <span className="text-xs font-mono text-[var(--color-accent-emerald)]">{d.replicas}/{d.replicas}</span>
              </div>
            ))}
          </ResourceGroup>

          <ResourceGroup title="StatefulSet'lar (4)" icon="S" color="var(--color-accent-purple)">
            {k8sResources.statefulSets.map((s) => (
              <div key={s.name} className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition-colors tree-item">
                <StatusDot />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">{s.name}</div>
                  <div className="text-xs text-[var(--color-text-muted)] truncate mt-0.5">{s.image}</div>
                </div>
                <span className="text-xs font-mono text-[var(--color-accent-amber)]">{s.storage}</span>
              </div>
            ))}
          </ResourceGroup>

          <ResourceGroup title="Servislar (9)" icon="N" color="var(--color-accent-emerald)">
            {k8sResources.services.map((s) => (
              <div key={s.name} className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition-colors tree-item">
                <span className={`text-xs px-2 py-0.5 rounded-full shrink-0 ${s.type === 'NodePort' ? 'bg-[var(--color-accent-blue)]/20 text-[var(--color-accent-blue)]' : s.type === 'Headless' ? 'bg-[var(--color-accent-amber)]/20 text-[var(--color-accent-amber)]' : 'bg-[var(--color-accent-purple)]/20 text-[var(--color-accent-purple)]'}`}>
                  {s.type}
                </span>
                <span className="text-sm text-[var(--color-text-primary)] flex-1">{s.name}</span>
                <span className="text-xs text-[var(--color-text-muted)] font-mono">{s.ports}</span>
              </div>
            ))}
          </ResourceGroup>

          <ResourceGroup title="Doimiy Hajmlar (6)" icon="V" color="var(--color-accent-amber)">
            {k8sResources.pvcs.map((p) => (
              <div key={p.name} className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-white/5 transition-colors tree-item">
                <div className="w-2.5 h-2.5 rounded bg-[var(--color-accent-amber)] shrink-0" />
                <span className="text-sm text-[var(--color-text-primary)] flex-1">{p.name}</span>
                <span className="text-xs text-[var(--color-text-muted)]">{p.size} {p.access}</span>
              </div>
            ))}
          </ResourceGroup>
        </div>
      </motion.div>
    </section>
  );
}
