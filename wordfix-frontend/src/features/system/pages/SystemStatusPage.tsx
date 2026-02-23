import { PageTransition } from '@/components/animations/PageTransition';
import { AIStatusCard } from '../components/AIStatusCard';
import { HealthBanner } from '../components/HealthBanner';
import { useSystemHealth } from '../hooks/useSystemHealth';
import { Activity, Server, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { ServiceHealth } from '@/types';

const statusIcons: Record<string, typeof CheckCircle> = {
  healthy: CheckCircle,
  degraded: AlertTriangle,
  unhealthy: XCircle,
  unavailable: XCircle,
};

const statusColors: Record<string, string> = {
  healthy: 'text-success',
  degraded: 'text-warning-foreground',
  unhealthy: 'text-destructive',
  unavailable: 'text-destructive',
};

const statusVariants: Record<string, 'success' | 'warning' | 'destructive'> = {
  healthy: 'success',
  degraded: 'warning',
  unhealthy: 'destructive',
  unavailable: 'destructive',
};

function ServiceCard({ name, service }: { name: string; service: ServiceHealth }) {
  const Icon = statusIcons[service.status] || statusIcons.unhealthy;
  const color = statusColors[service.status] || statusColors.unhealthy;
  const variant = statusVariants[service.status] || statusVariants.unhealthy;

  return (
    <Card className="border-border/50">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className={cn('flex h-9 w-9 items-center justify-center rounded-lg bg-muted')}>
              <Server className="h-4 w-4 text-muted-foreground" />
            </div>
            <div>
              <p className="text-sm font-medium capitalize">{service.name || name}</p>
              {service.message && (
                <p className="text-[10px] text-muted-foreground">{service.message}</p>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Icon className={cn('h-4 w-4', color)} />
            <Badge variant={variant} className="text-[10px]">
              {service.status}
            </Badge>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function SystemStatusPage() {
  const { data } = useSystemHealth();
  const health = data?.data;

  const overallIcon = health ? (statusIcons[health.status] || statusIcons.unhealthy) : Activity;
  const OverallIcon = overallIcon;
  const overallColor = health ? (statusColors[health.status] || '') : '';

  return (
    <PageTransition>
      <div className="mx-auto max-w-4xl space-y-6">
        <HealthBanner />

        {/* Header */}
        <div>
          <h1 className="font-heading text-3xl font-bold">System Status</h1>
          <p className="mt-1 text-muted-foreground">Monitor the health of all system services</p>
        </div>

        {/* Overall status */}
        {health && (
          <Card className="border-border/50">
            <CardContent className="p-5">
              <div className="flex items-center gap-3">
                <div className={cn('flex h-12 w-12 items-center justify-center rounded-xl', 
                  health.status === 'healthy' ? 'bg-success/10' : health.status === 'degraded' ? 'bg-warning/10' : 'bg-destructive/10'
                )}>
                  <OverallIcon className={cn('h-6 w-6', overallColor)} />
                </div>
                <div>
                  <h2 className="font-heading text-xl font-bold capitalize">{health.status}</h2>
                  <p className="text-sm text-muted-foreground">
                    {health.status === 'healthy' ? 'All services are running normally' :
                     health.status === 'degraded' ? 'Some services are experiencing issues' :
                     'Critical services are down'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Services grid */}
        {health?.services && (
          <div>
            <h3 className="font-heading text-lg font-semibold mb-3">Services</h3>
            <div className="grid gap-3 sm:grid-cols-2">
              {Object.entries(health.services).map(([key, service]) => (
                <ServiceCard key={key} name={key} service={service} />
              ))}
            </div>
          </div>
        )}

        {/* AI Providers */}
        <div>
          <h3 className="font-heading text-lg font-semibold mb-3">AI Providers</h3>
          <AIStatusCard />
        </div>
      </div>
    </PageTransition>
  );
}
