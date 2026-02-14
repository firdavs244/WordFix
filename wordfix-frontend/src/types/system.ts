// ─── System Types ──────────────────────────────────────────────────────────────

export interface ServiceHealth {
  name: string;
  status: 'healthy' | 'degraded' | 'unavailable';
  message: string;
  circuit_state: 'closed' | 'open' | 'half_open';
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'unhealthy';
  services: Record<string, ServiceHealth>;
}

export interface ConfigStatus {
  services: Record<string, unknown>;
  defaults_used: string[];
}
