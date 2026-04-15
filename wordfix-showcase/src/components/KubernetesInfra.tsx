import { motion } from 'framer-motion';
import { k8sResources } from '../data/architecture';

function ResourceGroup({ title, icon, color, children }: { title: string; icon: string; color: string; children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="glass-card p-5"
    >
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">{icon}</span>
        <h3 className="text-lg font-semibold" style={{ color }}>{title}</h3>
      </div>
      <div className="space-y-2">
        {children}
      </div>
    </motion.div>
  );
}

function StatusDot() {
  return (
    <span className="relative flex h-2.5 w-2.5">
      <span className="absolute inline-flex h-full w-full rounded-full bg-[var(--color-accent-emerald)] opacity-75 animate-ping" />
      <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[var(--color-accent-emerald)]" />
    </span>
  );
}

export default function KubernetesInfra() {
  return (
    <section id="kubernetes" className="py-24 px-6 bg-[var(--color-bg-secondary)]">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="max-w-6xl mx-auto"
      >
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-4">
          <span className="gradient-text">Kubernetes Infrastructure</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-12 max-w-2xl mx-auto">
          k3s cluster on Ubuntu 24.04 — 10 pods, persistent volumes, health probes, init containers for migrations.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Deployments */}
          <ResourceGroup title="Deployments (6)" icon="D" color="var(--color-accent-blue)">
            {k8sResources.deployments.map((d) => (
              <div key={d.name} className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors">
                <StatusDot />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">{d.name}</div>
                  <div className="text-xs text-[var(--color-text-muted)] truncate">{d.image}</div>
                </div>
                <span className="text-xs text-[var(--color-accent-emerald)]">{d.replicas}/{d.replicas}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* StatefulSets */}
          <ResourceGroup title="StatefulSets (4)" icon="S" color="var(--color-accent-purple)">
            {k8sResources.statefulSets.map((s) => (
              <div key={s.name} className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors">
                <StatusDot />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">{s.name}</div>
                  <div className="text-xs text-[var(--color-text-muted)] truncate">{s.image}</div>
                </div>
                <span className="text-xs text-[var(--color-accent-amber)]">{s.storage}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* Services */}
          <ResourceGroup title="Services (8)" icon="N" color="var(--color-accent-emerald)">
            {k8sResources.services.map((s) => (
              <div key={s.name} className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors">
                <span className={`text-xs px-2 py-0.5 rounded-full ${s.type === 'NodePort' ? 'bg-[var(--color-accent-blue)]/20 text-[var(--color-accent-blue)]' : s.type === 'Headless' ? 'bg-[var(--color-accent-amber)]/20 text-[var(--color-accent-amber)]' : 'bg-[var(--color-accent-purple)]/20 text-[var(--color-accent-purple)]'}`}>
                  {s.type}
                </span>
                <span className="text-sm text-[var(--color-text-primary)] flex-1">{s.name}</span>
                <span className="text-xs text-[var(--color-text-muted)] font-mono">{s.ports}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* PVCs */}
          <ResourceGroup title="Persistent Volumes (6)" icon="V" color="var(--color-accent-amber)">
            {k8sResources.pvcs.map((p) => (
              <div key={p.name} className="flex items-center gap-3 p-2 rounded-lg hover:bg-white/5 transition-colors">
                <div className="w-2 h-2 rounded bg-[var(--color-accent-amber)]" />
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
