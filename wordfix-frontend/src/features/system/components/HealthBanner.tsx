import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, AlertCircle, X } from 'lucide-react';
import { useSystemHealth } from '../hooks/useSystemHealth';
import type { ServiceHealth } from '@/types';

// ─── Service Name Translations ─────────────────────────────────────────────────

const serviceTranslations: Record<string, string> = {
  ai: 'AI xizmatlari (boyitish, testlar, chat)',
  tts: 'Audio xizmatlari (talaffuz)',
  cache: 'Tezlik optimizatsiyasi',
  celery: 'Fon vazifalari (boyitish)',
  redis: 'Tezlik optimizatsiyasi',
  database: "Ma'lumotlar bazasi",
  db: "Ma'lumotlar bazasi",
};

function getServiceLabel(key: string, service: ServiceHealth): string {
  return serviceTranslations[key] || service.name || key;
}

// ─── Component ─────────────────────────────────────────────────────────────────

export function HealthBanner() {
  const { data } = useSystemHealth();
  const [dismissed, setDismissed] = useState(false);
  const health = data?.data;

  // Reset dismissed state when health status changes
  useEffect(() => {
    const stored = sessionStorage.getItem('health_banner_dismissed');
    if (stored === health?.status) {
      setDismissed(true);
    } else {
      setDismissed(false);
    }
  }, [health?.status]);

  if (!health || health.status === 'healthy' || dismissed) {
    return null;
  }

  const isDegraded = health.status === 'degraded';
  const degradedServices = Object.entries(health.services).filter(
    ([, s]) => s.status !== 'healthy',
  );

  const handleDismiss = () => {
    setDismissed(true);
    sessionStorage.setItem('health_banner_dismissed', health.status);
  };

  return (
    <AnimatePresence>
      <motion.div
        initial={{ height: 0, opacity: 0 }}
        animate={{ height: 'auto', opacity: 1 }}
        exit={{ height: 0, opacity: 0 }}
        transition={{ duration: 0.3 }}
        className={
          isDegraded
            ? 'border-b border-yellow-300 bg-yellow-50 dark:border-yellow-800 dark:bg-yellow-950'
            : 'border-b border-red-300 bg-red-50 dark:border-red-800 dark:bg-red-950'
        }
      >
        <div className="mx-auto flex max-w-7xl items-start gap-3 px-4 py-3">
          {/* Icon — hidden on mobile */}
          <div className="hidden shrink-0 pt-0.5 sm:block">
            {isDegraded ? (
              <AlertTriangle className="h-5 w-5 text-yellow-600 dark:text-yellow-400" />
            ) : (
              <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400" />
            )}
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <p
              className={`text-sm font-medium ${
                isDegraded
                  ? 'text-yellow-800 dark:text-yellow-200'
                  : 'text-red-800 dark:text-red-200'
              }`}
            >
              {isDegraded
                ? "Ba'zi xizmatlar vaqtincha cheklangan"
                : "Tizim xizmatlari vaqtincha ishlamayapti"}
            </p>
            <ul className="mt-1 space-y-0.5">
              {degradedServices.map(([key, service]) => (
                <li
                  key={key}
                  className={`text-xs ${
                    isDegraded
                      ? 'text-yellow-700 dark:text-yellow-300'
                      : 'text-red-700 dark:text-red-300'
                  }`}
                >
                  • {getServiceLabel(key, service)}
                  {service.message && ` — ${service.message}`}
                </li>
              ))}
            </ul>
          </div>

          {/* Dismiss button */}
          <button
            onClick={handleDismiss}
            className={`shrink-0 rounded-md p-1 transition-colors ${
              isDegraded
                ? 'text-yellow-600 hover:bg-yellow-100 dark:text-yellow-400 dark:hover:bg-yellow-900'
                : 'text-red-600 hover:bg-red-100 dark:text-red-400 dark:hover:bg-red-900'
            }`}
            aria-label="Yopish"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
