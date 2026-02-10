// ─── API Types ─────────────────────────────────────────────────────────────────

export interface ApiResponse<T = unknown> {
  success: boolean;
  data: T;
  message: string;
  errors: Record<string, string[]> | null;
  meta: PaginationMeta | null;
}

export interface PaginationMeta {
  page: number;
  total_pages: number;
  total_count: number;
  page_size: number;
}

export interface HealthCheckResponse {
  status: 'healthy' | 'degraded';
  version: string;
  services: { db: 'up' | 'down'; redis: 'up' | 'down'; celery: 'up' | 'down' };
}
