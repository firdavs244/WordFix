import { Link } from 'react-router-dom';
import { Skeleton } from '@/components/ui/skeleton';
import { useDomainCoverage } from '@/features/learning/hooks/useLearning';
import DomainBar from './DomainBar';

const DOMAIN_COLORS: Record<string, string> = {
  academic: 'bg-blue-500', business: 'bg-emerald-500', technology: 'bg-violet-500',
  daily_life: 'bg-orange-500', science: 'bg-teal-500', arts: 'bg-pink-500',
  travel: 'bg-rose-500', medical: 'bg-red-500', legal: 'bg-slate-500', social: 'bg-indigo-500',
};

interface Props {
  compact?: boolean;
}

export default function DomainCoverageWidget({ compact }: Props) {
  const { data, isLoading } = useDomainCoverage();
  const domains = data?.data;

  if (isLoading) {
    return (
      <div className="rounded-2xl border border-border/50 bg-card p-5 shadow-card">
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => <Skeleton key={i} className="h-6 rounded" />)}
        </div>
      </div>
    );
  }

  const entries = domains
    ? Object.entries(domains).map(([key, val]) => ({ key, ...val }))
    : [];

  const visible = compact ? entries.slice(0, 5) : entries;

  return (
    <div className="rounded-2xl border border-border/50 bg-card shadow-card">
      <div className="flex items-center justify-between px-5 pt-5">
        <h3 className="text-base font-heading font-semibold">So'z sohalari</h3>
        {compact && (
          <Link to="/learning-profile" className="text-xs font-medium text-primary hover:underline">
            Barchasini ko'rish →
          </Link>
        )}
      </div>

      <div className="space-y-3 px-5 py-4">
        {visible.length === 0 ? (
          <p className="py-6 text-center text-sm text-muted-foreground">Ma'lumot yo'q</p>
        ) : (
          visible.map((domain) => (
            <DomainBar
              key={domain.key}
              domain={domain}
              color={DOMAIN_COLORS[domain.key] ?? 'bg-gray-500'}
            />
          ))
        )}
      </div>
    </div>
  );
}
