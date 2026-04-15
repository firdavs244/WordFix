import { motion } from 'framer-motion';
import { k8sResources } from '../data/architecture';

function ResourceGroup({ title, icon, color, count, children }: { title: string; icon: string; color: string; count?: number; children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      className="glass-card"
    >
      <div className="flex items-center gap-3 mb-5">
        <span
          className="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold"
          style={{ background: `${color}22`, color }}
        >
          {icon}
        </span>
        <h3 className="text-base font-semibold" style={{ color }}>{title}</h3>
        {count !== undefined && (
          <span className="text-xs text-[var(--color-text-muted)] ml-auto font-mono">({count})</span>
        )}
      </div>
      <div className="space-y-1">{children}</div>
    </motion.div>
  );
}

function StatusDot() {
  return (
    <span className="relative flex h-2 w-2 shrink-0">
      <span className="absolute inline-flex h-full w-full rounded-full bg-[var(--color-accent-emerald)] opacity-75 animate-ping" />
      <span className="relative inline-flex rounded-full h-2 w-2 bg-[var(--color-accent-emerald)]" />
    </span>
  );
}

const SERVICE_TYPE_BADGES: Record<string, string> = {
  NodePort: 'badge-blue',
  ClusterIP: 'badge-purple',
  Headless: 'badge-amber',
};

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
          <span className="gradient-text">Kubernetes Infratuzilmasi</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-12 max-w-2xl mx-auto text-base leading-relaxed">
          Ubuntu 24.04 da k3s klaster — HPA avtoskaling, PodDisruptionBudget,
          NetworkPolicy (zero-trust), SecurityContext va health probe'lar.
        </p>

        {/* Stats bar */}
        <div className="glass-card-sm mb-8">
          <div className="flex flex-wrap justify-center gap-6 text-center">
            <div>
              <div className="text-2xl font-bold text-[var(--color-accent-blue)]">15+</div>
              <div className="text-xs text-[var(--color-text-muted)]">Podlar</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-[var(--color-accent-purple)]">5</div>
              <div className="text-xs text-[var(--color-text-muted)]">HPA</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-[var(--color-accent-emerald)]">7</div>
              <div className="text-xs text-[var(--color-text-muted)]">PDB</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-[var(--color-accent-amber)]">10</div>
              <div className="text-xs text-[var(--color-text-muted)]">NetworkPolicy</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-[var(--color-accent-pink)]">11</div>
              <div className="text-xs text-[var(--color-text-muted)]">SecurityContext</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Deployments */}
          <ResourceGroup title="Deployment'lar" icon="D" color="var(--color-accent-blue)" count={k8sResources.deployments.length}>
            {k8sResources.deployments.map((d) => (
              <div key={d.name} className="flex items-center gap-3 px-3 py-2 rounded-lg tree-item">
                <StatusDot />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">{d.name}</div>
                  <div className="text-xs text-[var(--color-text-muted)] truncate">{d.image}</div>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  {d.hpa && (
                    <span className="text-[10px] px-1.5 py-0.5 rounded badge-purple font-medium">
                      HPA {d.maxReplicas}
                    </span>
                  )}
                  <span className="text-xs font-mono text-[var(--color-accent-emerald)]">
                    {d.replicas}/{d.replicas}
                  </span>
                </div>
              </div>
            ))}
          </ResourceGroup>

          {/* StatefulSets */}
          <ResourceGroup title="StatefulSet'lar" icon="S" color="var(--color-accent-purple)" count={k8sResources.statefulSets.length}>
            {k8sResources.statefulSets.map((s) => (
              <div key={s.name} className="flex items-center gap-3 px-3 py-2 rounded-lg tree-item">
                <StatusDot />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">{s.name}</div>
                  <div className="text-xs text-[var(--color-text-muted)] truncate">{s.image}</div>
                </div>
                <span className="text-xs font-mono text-[var(--color-accent-amber)] shrink-0">{s.storage}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* HPAs */}
          <ResourceGroup title="HorizontalPodAutoscaler" icon="H" color="var(--color-accent-pink)" count={k8sResources.hpas.length}>
            {k8sResources.hpas.map((h) => (
              <div key={h.name} className="flex items-center gap-3 px-3 py-2 rounded-lg tree-item">
                <span className="w-2 h-2 rounded-full bg-[var(--color-accent-pink)] shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">{h.target}</div>
                  <div className="text-xs text-[var(--color-text-muted)]">CPU: {h.cpuTarget}% · Mem: {h.memTarget}%</div>
                </div>
                <span className="text-xs font-mono text-[var(--color-accent-pink)] shrink-0">{h.minReplicas}→{h.maxReplicas}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* Services */}
          <ResourceGroup title="Servislar" icon="N" color="var(--color-accent-emerald)" count={k8sResources.services.length}>
            {k8sResources.services.map((s) => (
              <div key={s.name} className="flex items-center gap-3 px-3 py-2 rounded-lg tree-item">
                <span className={`text-[11px] px-2 py-0.5 rounded-full shrink-0 font-medium ${SERVICE_TYPE_BADGES[s.type] || 'badge-purple'}`}>
                  {s.type}
                </span>
                <span className="text-sm text-[var(--color-text-primary)] flex-1 min-w-0 truncate">{s.name}</span>
                <span className="text-xs text-[var(--color-text-muted)] font-mono shrink-0">{s.ports}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* PDBs */}
          <ResourceGroup title="PodDisruptionBudget" icon="P" color="var(--color-accent-amber)" count={k8sResources.pdbs.length}>
            {k8sResources.pdbs.map((p) => (
              <div key={p.name} className="flex items-center gap-3 px-3 py-2 rounded-lg tree-item">
                <span className="w-2 h-2 rounded-sm bg-[var(--color-accent-amber)] shrink-0" />
                <span className="text-sm text-[var(--color-text-primary)] flex-1 min-w-0 truncate">{p.target}</span>
                <span className="text-xs text-[var(--color-text-muted)] shrink-0">minAvailable: {p.minAvailable}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* Network Policies */}
          <ResourceGroup title="NetworkPolicy (Zero-Trust)" icon="🛡" color="var(--color-accent-emerald)" count={k8sResources.networkPolicies.length}>
            {k8sResources.networkPolicies.map((np) => (
              <div key={np.name} className="flex items-center gap-3 px-3 py-2 rounded-lg tree-item">
                <span className="w-2 h-2 rounded-full bg-[var(--color-accent-emerald)] shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-[var(--color-text-primary)] truncate">{np.name}</div>
                  <div className="text-xs text-[var(--color-text-muted)] truncate">{np.description}</div>
                </div>
              </div>
            ))}
          </ResourceGroup>

          {/* PVCs */}
          <ResourceGroup title="Doimiy Hajmlar" icon="V" color="var(--color-accent-amber)" count={k8sResources.pvcs.length}>
            {k8sResources.pvcs.map((p) => (
              <div key={p.name} className="flex items-center gap-3 px-3 py-2 rounded-lg tree-item">
                <div className="w-2 h-2 rounded-sm bg-[var(--color-accent-amber)] shrink-0" />
                <span className="text-sm text-[var(--color-text-primary)] flex-1 min-w-0 truncate">{p.name}</span>
                <span className="text-xs text-[var(--color-text-muted)] shrink-0">{p.size}</span>
              </div>
            ))}
          </ResourceGroup>

          {/* Security Summary */}
          <ResourceGroup title="Xavfsizlik sozlamalari" icon="🔒" color="var(--color-accent-purple)">
            <div className="space-y-2 text-sm">
              <div className="flex items-start gap-3 px-3 py-2">
                <span className="text-[var(--color-accent-emerald)] shrink-0 mt-0.5">✓</span>
                <div>
                  <span className="text-[var(--color-text-primary)]">SecurityContext</span>
                  <p className="text-xs text-[var(--color-text-muted)]">runAsNonRoot, runAsUser, drop ALL capabilities</p>
                </div>
              </div>
              <div className="flex items-start gap-3 px-3 py-2">
                <span className="text-[var(--color-accent-emerald)] shrink-0 mt-0.5">✓</span>
                <div>
                  <span className="text-[var(--color-text-primary)]">Zero-Trust Networking</span>
                  <p className="text-xs text-[var(--color-text-muted)]">Default deny + aniq ruxsatlar: nginx→gateway→web→db</p>
                </div>
              </div>
              <div className="flex items-start gap-3 px-3 py-2">
                <span className="text-[var(--color-accent-emerald)] shrink-0 mt-0.5">✓</span>
                <div>
                  <span className="text-[var(--color-text-primary)]">Rolling Updates</span>
                  <p className="text-xs text-[var(--color-text-muted)]">maxSurge:1, maxUnavailable:0 — nol downtime</p>
                </div>
              </div>
              <div className="flex items-start gap-3 px-3 py-2">
                <span className="text-[var(--color-accent-emerald)] shrink-0 mt-0.5">✓</span>
                <div>
                  <span className="text-[var(--color-text-primary)]">Graceful Shutdown</span>
                  <p className="text-xs text-[var(--color-text-muted)]">terminationGracePeriodSeconds: web 60s, celery-worker 120s</p>
                </div>
              </div>
            </div>
          </ResourceGroup>
        </div>
      </motion.div>
    </section>
  );
}
