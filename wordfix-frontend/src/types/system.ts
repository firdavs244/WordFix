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

// ─── AI Status Types ───────────────────────────────────────────────────────────

export interface AIProviderStatus {
  configured: boolean;
  available: boolean;
  circuit_breaker: 'closed' | 'open' | 'half_open';
}

export interface AIStatusResponse {
  active_provider: string;
  providers: Record<string, AIProviderStatus>;
  fallback_active: boolean;
}
