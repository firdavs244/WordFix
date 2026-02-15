import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, X } from 'lucide-react';
import { useSystemHealth } from '@/features/system/hooks/useSystemHealth';
import type { ServiceHealth } from '@/types';

const serviceNames: Record<string, string> = {
  ai: 'AI xizmatlari (boyitish, testlar, chat)',
  tts: 'Audio xizmatlari (talaffuz)',
  cache: 'Tezlik optimizatsiyasi',
  celery: 'Fon vazifalari (boyitish)',
  redis: 'Tezlik optimizatsiyasi',
  database: "Ma'lumotlar bazasi",
  db: "Ma'lumotlar bazasi",
};

function label(key: string, s: ServiceHealth) {
  return serviceNames[key] || s.name || key;
}

export function HealthBanner() {
  const { data } = useSystemHealth();
  const [dismissed, setDismissed] = useState(false);
  const health = data?.data;

  useEffect(() => {
    const stored = sessionStorage.getItem('health_banner_dismissed');
    setDismissed(stored === health?.status);
  }, [health?.status]);

  if (!health || health.status === 'healthy' || dismissed) return null;

  const isDegraded = health.status === 'degraded';
  const broken = Object.entries(health.services).filter(([, s]) => s.status !== 'healthy');

  const dismiss = () => {
    setDismissed(true);
    sessionStorage.setItem('health_banner_dismissed', health.status);
  };

  const bg = isDegraded ? 'bg-warning/10 border-warning/20' : 'bg-destructive/10 border-destructive/20';
  const text = isDegraded ? 'text-warning' : 'text-destructive';

  return (
    <AnimatePresence>
      <motion.div
        initial={{ height: 0, opacity: 0 }}
        animate={{ height: 'auto', opacity: 1 }}
        exit={{ height: 0, opacity: 0 }}
        transition={{ duration: 0.3 }}
        className={`border-b ${bg}`}
      >
        <div className="mx-auto flex max-w-7xl items-start gap-3 px-4 py-3">
          <AlertTriangle className={`hidden h-5 w-5 shrink-0 sm:block ${text}`} />
          <div className="min-w-0 flex-1">
            <p className={`text-sm font-medium ${text}`}>
              {isDegraded ? "Ba'zi xizmatlar vaqtincha cheklangan" : "Tizim xizmatlari vaqtincha ishlamayapti"}
            </p>
            <ul className="mt-1 space-y-0.5">
              {broken.map(([k, s]) => (
                <li key={k} className={`text-xs ${text}/80`}>• {label(k, s)}{s.message && ` — ${s.message}`}</li>
              ))}
            </ul>
          </div>
          <button onClick={dismiss} className={`shrink-0 rounded-md p-1 transition-colors ${text} hover:bg-muted/50`} aria-label="Yopish">
            <X className="h-4 w-4" />
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
