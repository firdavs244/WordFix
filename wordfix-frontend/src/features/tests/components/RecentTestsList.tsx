import { ClipboardList } from 'lucide-react';
import { useRecentTests } from '../hooks/useTests';
import RecentTestItem from './RecentTestItem';

export default function RecentTestsList() {
  const { data: tests, isLoading } = useRecentTests();

  if (isLoading) return null;

  return (
    <div className="rounded-2xl border border-border/50 p-6 shadow-card">
      <h3 className="mb-4 text-sm font-semibold">Recent Tests</h3>
      {!tests?.length ? (
        <div className="flex flex-col items-center py-8 text-center">
          <ClipboardList className="mb-2 h-8 w-8 text-muted-foreground/40" />
          <p className="text-sm text-muted-foreground">No tests taken yet</p>
        </div>
      ) : (
        <div className="space-y-1">
          {tests.slice(0, 5).map((t) => (
            <RecentTestItem key={t.id} test={t} />
          ))}
        </div>
      )}
    </div>
  );
}
