import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { useDomainCoverage } from '../hooks/useLearning';

// ─── Domain Config ─────────────────────────────────────────────────────────────

const domainConfig: Record<string, { label: string; color: string; barColor: string; masteredColor: string }> = {
  academic: { label: 'Academic', color: 'text-blue-600', barColor: 'bg-blue-400', masteredColor: 'bg-blue-600' },
  business: { label: 'Business', color: 'text-green-600', barColor: 'bg-green-400', masteredColor: 'bg-green-600' },
  technology: { label: 'Technology', color: 'text-purple-600', barColor: 'bg-purple-400', masteredColor: 'bg-purple-600' },
  daily_life: { label: 'Daily Life', color: 'text-orange-600', barColor: 'bg-orange-400', masteredColor: 'bg-orange-600' },
  science: { label: 'Science', color: 'text-teal-600', barColor: 'bg-teal-400', masteredColor: 'bg-teal-600' },
  arts: { label: 'Arts', color: 'text-pink-600', barColor: 'bg-pink-400', masteredColor: 'bg-pink-600' },
  travel: { label: 'Travel', color: 'text-rose-600', barColor: 'bg-rose-400', masteredColor: 'bg-rose-600' },
  medical: { label: 'Medical', color: 'text-red-600', barColor: 'bg-red-400', masteredColor: 'bg-red-600' },
  legal: { label: 'Legal', color: 'text-slate-600', barColor: 'bg-slate-400', masteredColor: 'bg-slate-600' },
  social: { label: 'Social', color: 'text-indigo-600', barColor: 'bg-indigo-400', masteredColor: 'bg-indigo-600' },
};

// ─── Component ─────────────────────────────────────────────────────────────────

export function DomainCoverageWidget({ compact = true }: { compact?: boolean }) {
  const { data, isLoading } = useDomainCoverage();
  const coverage = data?.data;

  const entries = coverage
    ? Object.entries(coverage)
        .map(([key, val]) => ({
          key,
          ...val,
          config: domainConfig[key] ?? { label: key, color: 'text-gray-600', barColor: 'bg-gray-400', masteredColor: 'bg-gray-600' },
        }))
        .sort((a, b) => b.coverage - a.coverage)
    : [];

  const displayed = compact ? entries.slice(0, 5) : entries;

  return (
    <Card className="border-border/50">
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2 text-lg">
          📊 So&apos;z sohalari
        </CardTitle>
        {compact && entries.length > 5 && (
          <Link to="/learning-profile">
            <Button variant="ghost" size="sm" className="gap-1 text-primary">
              Barchasini ko&apos;rish
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        )}
      </CardHeader>
      <CardContent>
        {isLoading ? (
          <div className="space-y-3">
            {[1, 2, 3, 4, 5].map((i) => (
              <Skeleton key={i} className="h-6 w-full" />
            ))}
          </div>
        ) : entries.length === 0 ? (
          <p className="py-4 text-center text-sm text-muted-foreground">
            Ma&apos;lumot yo&apos;q
          </p>
        ) : (
          <div className="space-y-3">
            {displayed.map((d, i) => (
              <motion.div
                key={d.key}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: i * 0.04 }}
                className="flex items-center gap-3"
              >
                <span className={`w-20 text-sm font-medium truncate ${d.config.color}`}>
                  {d.config.label}
                </span>
                <div className="flex-1 h-4 overflow-hidden rounded-full bg-muted">
                  <motion.div
                    className={`h-full rounded-full ${d.config.barColor} relative`}
                    initial={{ width: 0 }}
                    animate={{ width: `${Math.min(d.coverage, 100)}%` }}
                    transition={{ duration: 0.8, ease: 'easeOut', delay: i * 0.04 }}
                  >
                    {d.mastered > 0 && d.coverage > 0 && (
                      <div
                        className={`absolute inset-y-0 left-0 rounded-full ${d.config.masteredColor}`}
                        style={{ width: `${Math.min((d.mastered / Math.max(d.coverage, 1)) * 100, 100)}%` }}
                      />
                    )}
                  </motion.div>
                </div>
                <span className="w-10 text-right text-sm text-muted-foreground">
                  {d.coverage > 0 ? `${Math.round(d.coverage)}%` : (
                    <span className="text-xs">—</span>
                  )}
                </span>
              </motion.div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
