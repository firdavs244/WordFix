import { motion } from 'framer-motion';
import { Activity, CheckCircle, XCircle, AlertTriangle, Zap, RefreshCw } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useAIStatus } from '../hooks/useSystemHealth';
import { cn } from '@/lib/utils';
import type { AIProviderStatus } from '@/types';

type ProviderDisplayStatus = 'available' | 'unavailable' | 'degraded' | 'circuit_open';

function getProviderDisplayStatus(provider: AIProviderStatus): ProviderDisplayStatus {
  if (provider.circuit_breaker === 'open') return 'circuit_open';
  if (provider.available) return 'available';
  if (provider.configured && !provider.available) return 'degraded';
  return 'unavailable';
}

const statusConfig: Record<ProviderDisplayStatus, { icon: typeof CheckCircle; color: string; bg: string; label: string; variant: 'success' | 'destructive' | 'warning' }> = {
  available: { icon: CheckCircle, color: 'text-success', bg: 'bg-success/10', label: 'Online', variant: 'success' },
  unavailable: { icon: XCircle, color: 'text-destructive', bg: 'bg-destructive/10', label: 'Offline', variant: 'destructive' },
  degraded: { icon: AlertTriangle, color: 'text-warning-foreground', bg: 'bg-warning/10', label: 'Degraded', variant: 'warning' },
  circuit_open: { icon: AlertTriangle, color: 'text-orange-500', bg: 'bg-orange-500/10', label: 'Circuit Open', variant: 'warning' },
};

function ProviderRow({ name, provider, isActive }: { name: string; provider: AIProviderStatus; isActive: boolean }) {
  const displayStatus = getProviderDisplayStatus(provider);
  const config = statusConfig[displayStatus];
  const StatusIcon = config.icon;

  return (
    <div className="flex items-center justify-between rounded-lg border border-border/30 bg-background/50 px-3 py-2.5">
      <div className="flex items-center gap-2.5">
        <div className={cn('flex h-8 w-8 items-center justify-center rounded-lg', config.bg)}>
          <StatusIcon className={cn('h-4 w-4', config.color)} />
        </div>
        <div>
          <p className="text-sm font-medium capitalize">{name}</p>
          <p className="text-[10px] text-muted-foreground">
            Circuit: {provider.circuit_breaker}
          </p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        {isActive && (
          <Badge variant="default" className="text-[10px] px-1.5 py-0">
            <Zap className="mr-0.5 h-2.5 w-2.5" />
            Active
          </Badge>
        )}
        <Badge variant={config.variant} className="text-[10px]">
          {config.label}
        </Badge>
      </div>
    </div>
  );
}

interface AIStatusCardProps {
  compact?: boolean;
  className?: string;
}

export function AIStatusCard({ compact = false, className }: AIStatusCardProps) {
  const { data, isLoading, refetch, isRefetching } = useAIStatus();
  const aiStatus = data?.data;

  if (isLoading) {
    return (
      <Card className={cn('border-border/50', className)}>
        <CardContent className="p-5">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 animate-pulse rounded-lg bg-muted" />
            <div className="space-y-2 flex-1">
              <div className="h-4 w-24 animate-pulse rounded bg-muted" />
              <div className="h-3 w-40 animate-pulse rounded bg-muted" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!aiStatus) return null;

  const providers = aiStatus.providers ?? {};
  const activeProvider = aiStatus.active_provider;
  const providerEntries = Object.entries(providers);

  if (compact) {
    const activeStatus = activeProvider ? providers[activeProvider] : null;
    const displayStatus = activeStatus ? getProviderDisplayStatus(activeStatus) : 'unavailable' as ProviderDisplayStatus;
    const config = statusConfig[displayStatus];
    const StatusIcon = config.icon;

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className={cn('flex items-center gap-2 rounded-lg border border-border/40 bg-card px-3 py-2', className)}
      >
        <StatusIcon className={cn('h-4 w-4', config.color)} />
        <span className="text-xs font-medium">AI: {activeProvider ?? 'none'}</span>
        <Badge variant={config.variant} className="text-[9px] px-1.5 py-0 h-4">
          {config.label}
        </Badge>
      </motion.div>
    );
  }

  return (
    <Card className={cn('border-border/50', className)}>
      <CardContent className="p-5 space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10">
              <Activity className="h-5 w-5 text-primary" />
            </div>
            <div>
              <h3 className="font-heading text-sm font-semibold">AI Providers</h3>
              <p className="text-[11px] text-muted-foreground">
                Active: <span className="font-medium capitalize text-foreground">{activeProvider ?? 'none'}</span>
              </p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={() => refetch()}
            disabled={isRefetching}
          >
            <RefreshCw className={cn('h-4 w-4', isRefetching && 'animate-spin')} />
          </Button>
        </div>

        {/* Fallback chain */}
        {providerEntries.length > 1 && (
          <div className="rounded-lg bg-muted/30 px-3 py-2">
            <p className="text-[10px] font-medium text-muted-foreground mb-1">Provider Chain</p>
            <div className="flex items-center gap-1.5">
              {providerEntries.map(([name], i) => (
                <span key={name} className="flex items-center gap-1.5">
                  <span className={cn(
                    'rounded-full px-2 py-0.5 text-[10px] font-medium',
                    name === activeProvider ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'
                  )}>
                    {name}
                  </span>
                  {i < providerEntries.length - 1 && (
                    <span className="text-[10px] text-muted-foreground">→</span>
                  )}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Provider list */}
        <div className="space-y-2">
          {providerEntries.map(([name, provider]) => (
            <ProviderRow key={name} name={name} provider={provider} isActive={name === activeProvider} />
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
