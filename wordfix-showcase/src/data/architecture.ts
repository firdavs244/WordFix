export interface ServiceNode {
  id: string;
  name: string;
  tech: string;
  port: string;
  description: string;
  category: 'frontend' | 'backend' | 'database' | 'infra';
  x: number;
  y: number;
}

export interface Connection {
  from: string;
  to: string;
  label?: string;
  protocol?: string;
}

export interface FlowStep {
  id: number;
  title: string;
  description: string;
  from: string;
  to: string;
  method?: string;
  path?: string;
  code?: string;
}

export const CATEGORY_COLORS = {
  frontend: { bg: '#1e3a5f', border: '#3b82f6', text: '#93c5fd', glow: 'rgba(59,130,246,0.3)' },
  backend: { bg: '#2d1b69', border: '#8b5cf6', text: '#c4b5fd', glow: 'rgba(139,92,246,0.3)' },
  database: { bg: '#064e3b', border: '#10b981', text: '#6ee7b7', glow: 'rgba(16,185,129,0.3)' },
  infra: { bg: '#78350f', border: '#f59e0b', text: '#fcd34d', glow: 'rgba(245,158,11,0.3)' },
};

export const services: ServiceNode[] = [
  { id: 'browser', name: 'Browser', tech: 'React 19 + TypeScript', port: '-', description: 'SPA frontend with Vite 6, TailwindCSS, Framer Motion', category: 'frontend', x: 450, y: 30 },
  { id: 'nginx', name: 'Nginx', tech: 'nginx:alpine', port: '30080', description: 'Reverse proxy, serves static frontend, routes /api/* to backend', category: 'frontend', x: 450, y: 130 },
  { id: 'gateway', name: 'API Gateway', tech: 'FastAPI + Python', port: '8080', description: 'Routes requests to auth-service or Django monolith, JWT validation', category: 'backend', x: 450, y: 240 },
  { id: 'auth', name: 'Auth Service', tech: 'FastAPI + SQLAlchemy', port: '8001/50051', description: 'JWT auth, Google OAuth, user registration, gRPC interface', category: 'backend', x: 200, y: 350 },
  { id: 'web', name: 'Django Monolith', tech: 'Django 5 + DRF', port: '8000', description: 'Words, tests, games, dashboard, onboarding, AI features', category: 'backend', x: 700, y: 350 },
  { id: 'celery-worker', name: 'Celery Worker', tech: 'Celery 5 + Python', port: '-', description: 'Async task processing: AI generation, spaced repetition', category: 'backend', x: 850, y: 480 },
  { id: 'celery-beat', name: 'Celery Beat', tech: 'Celery 5 Beat', port: '-', description: 'Periodic task scheduler: daily reviews, stats aggregation', category: 'backend', x: 700, y: 480 },
  { id: 'auth-db', name: 'Auth DB', tech: 'PostgreSQL 16', port: '5432', description: 'Stores users, sessions, OAuth tokens for auth-service', category: 'database', x: 100, y: 480 },
  { id: 'db', name: 'Main DB', tech: 'PostgreSQL 16', port: '5432', description: 'Stores words, tests, games, user progress, reviews', category: 'database', x: 450, y: 550 },
  { id: 'redis', name: 'Redis', tech: 'Redis 7', port: '6379', description: 'Caching, session store, Celery result backend', category: 'infra', x: 600, y: 480 },
  { id: 'rabbitmq', name: 'RabbitMQ', tech: 'RabbitMQ 3.13', port: '5672', description: 'Message broker for Celery tasks and inter-service events', category: 'infra', x: 300, y: 480 },
];

export const connections: Connection[] = [
  { from: 'browser', to: 'nginx', label: 'HTTP :30080', protocol: 'HTTP' },
  { from: 'nginx', to: 'gateway', label: '/api/*', protocol: 'HTTP' },
  { from: 'gateway', to: 'auth', label: 'Auth routes', protocol: 'HTTP' },
  { from: 'gateway', to: 'web', label: 'App routes', protocol: 'HTTP' },
  { from: 'auth', to: 'auth-db', protocol: 'TCP' },
  { from: 'web', to: 'db', protocol: 'TCP' },
  { from: 'web', to: 'redis', protocol: 'TCP' },
  { from: 'web', to: 'rabbitmq', label: 'Tasks', protocol: 'AMQP' },
  { from: 'celery-worker', to: 'rabbitmq', label: 'Consume', protocol: 'AMQP' },
  { from: 'celery-worker', to: 'db', protocol: 'TCP' },
  { from: 'celery-worker', to: 'redis', label: 'Results', protocol: 'TCP' },
  { from: 'celery-beat', to: 'rabbitmq', label: 'Schedule', protocol: 'AMQP' },
];

export const flowSteps: FlowStep[] = [
  { id: 1, title: 'User clicks "Register"', description: 'Browser sends POST request to /api/v1/auth/register/ with email, username, password', from: 'browser', to: 'nginx', method: 'POST', path: '/api/v1/auth/register/', code: 'fetch("/api/v1/auth/register/", {\n  method: "POST",\n  body: JSON.stringify({ email, username, password })\n})' },
  { id: 2, title: 'Nginx forwards to Gateway', description: 'Nginx location /api/ block proxies request to gateway:8080', from: 'nginx', to: 'gateway', method: 'POST', path: '/api/v1/auth/register/', code: 'location /api/ {\n  proxy_pass http://gateway:8080;\n}' },
  { id: 3, title: 'Gateway routes to Auth Service', description: 'Gateway checks AUTH_PATHS set, /register/ matches → forward to auth-service:8001', from: 'gateway', to: 'auth', method: 'POST', path: '/auth/register/', code: 'AUTH_PATHS = {"register","login","logout",...}\nif path_part in AUTH_PATHS:\n    forward_to(AUTH_SERVICE_URL)' },
  { id: 4, title: 'Auth Service creates user', description: 'Auth service hashes password, generates UUID, creates user in auth DB', from: 'auth', to: 'auth-db', method: 'INSERT', path: 'wordfix_auth.users', code: 'user = UserEntity(\n  id=uuid4(),\n  email=email,\n  password=hash(password)\n)\nawait user_repo.create(user)' },
  { id: 5, title: 'JWT tokens generated', description: 'Auth service creates access + refresh tokens with user_id claim', from: 'auth', to: 'auth', code: 'access = create_jwt(\n  payload={"user_id": str(user.id),\n           "token_type": "access"},\n  secret=JWT_SECRET\n)' },
  { id: 6, title: 'Tokens return to browser', description: 'Response travels: Auth → Gateway → Nginx → Browser. Tokens stored in localStorage', from: 'auth', to: 'browser', code: '{ "access": "eyJhbG...",\n  "refresh": "eyJhbG..." }' },
  { id: 7, title: 'User clicks "Skip Onboarding"', description: 'Browser sends POST /api/v1/auth/onboarding/skip/ with Bearer token', from: 'browser', to: 'nginx', method: 'POST', path: '/api/v1/auth/onboarding/skip/' },
  { id: 8, title: 'Nginx → Gateway → Django', description: 'Gateway sees /onboarding/ not in AUTH_PATHS, forwards to Django monolith', from: 'gateway', to: 'web', method: 'POST', path: '/api/v1/auth/onboarding/skip/', code: '# Not in AUTH_PATHS → Django\nforward_to(MONOLITH_URL)' },
  { id: 9, title: 'AutoProvisionJWT authenticates', description: 'Django JWT backend decodes token, user_id not in Django DB → auto-provision triggered', from: 'web', to: 'web', code: 'class AutoProvisionJWTAuth:\n  def get_user(self, token):\n    try:\n      return super().get_user(token)\n    except AuthenticationFailed:\n      return self._provision_user(\n        token["user_id"])' },
  { id: 10, title: 'Fetch profile from Auth Service', description: 'Django calls auth-service internal API to get full user profile', from: 'web', to: 'auth', method: 'GET', path: '/auth/profile/', code: 'resp = httpx.get(\n  "http://auth-service:8001/auth/profile/",\n  headers={"Authorization":\n    f"Bearer {token}"}\n)' },
  { id: 11, title: 'Auth Service queries user data', description: 'Auth service fetches complete user profile from its database', from: 'auth', to: 'auth-db', method: 'SELECT', path: 'wordfix_auth.users' },
  { id: 12, title: 'Profile data returned', description: 'Full user entity returned: email, username, full_name, languages, proficiency', from: 'auth', to: 'web', code: '{\n  "id": "uuid",\n  "email": "user@email.com",\n  "username": "user123",\n  "native_language": "uz",\n  "learning_language": "en",\n  "proficiency_level": "A1"\n}' },
  { id: 13, title: 'User auto-provisioned in Django DB', description: 'CustomUser.objects.get_or_create() with auth-service data, UserProgress created', from: 'web', to: 'db', method: 'INSERT', path: 'wordfix.users + user_progress', code: 'user, created = CustomUser\\\n  .objects.get_or_create(\n    id=user_uuid,\n    defaults=profile_data\n  )\nUserProgress.objects\\\n  .get_or_create(user=user)' },
  { id: 14, title: 'Onboarding skip processed', description: 'User authenticated, has_completed_onboarding set to True, response 200 OK', from: 'web', to: 'db', method: 'UPDATE', path: 'wordfix.users', code: 'user.has_completed_onboarding = True\nuser.save()' },
  { id: 15, title: 'Success response to browser', description: 'HTTP 200 travels back: Django → Gateway → Nginx → Browser', from: 'web', to: 'browser', code: '{"status": "success",\n "message": "Onboarding skipped"}' },
  { id: 16, title: 'Dashboard loads', description: 'Browser fetches dashboard data, words, progress — all authenticated seamlessly', from: 'browser', to: 'nginx', method: 'GET', path: '/api/v1/dashboard/' },
  { id: 17, title: 'AI word generation triggered', description: 'User adds words → Django publishes Celery task via RabbitMQ', from: 'web', to: 'rabbitmq', method: 'PUBLISH', path: 'celery task queue', code: 'generate_ai_content\\\n  .delay(word_id=word.id)' },
  { id: 18, title: 'Worker processes AI task', description: 'Celery worker picks up task, calls Groq/Gemini API for examples, mnemonics', from: 'celery-worker', to: 'rabbitmq', method: 'CONSUME', code: '@app.task\ndef generate_ai_content(word_id):\n  word = Word.objects.get(id=word_id)\n  result = groq.generate(\n    examples_for=word.text)' },
  { id: 19, title: 'Results stored', description: 'AI-generated content saved to DB, result cached in Redis', from: 'celery-worker', to: 'db', method: 'UPDATE', path: 'wordfix.words', code: 'word.ai_examples = result\nword.save()\nredis.set(\n  f"word:{word_id}:ai", result)' },
];

export const k8sResources = {
  deployments: [
    { name: 'nginx', replicas: 1, image: 'wordfix/frontend:latest', status: 'Running' },
    { name: 'gateway', replicas: 1, image: 'wordfix/api-gateway:latest', status: 'Running' },
    { name: 'auth-service', replicas: 1, image: 'wordfix/auth-service:latest', status: 'Running' },
    { name: 'web', replicas: 1, image: 'wordfix/monolith:latest', status: 'Running' },
    { name: 'celery-worker', replicas: 1, image: 'wordfix/monolith:latest', status: 'Running' },
    { name: 'celery-beat', replicas: 1, image: 'wordfix/monolith:latest', status: 'Running' },
  ],
  statefulSets: [
    { name: 'db', replicas: 1, image: 'postgres:16-alpine', storage: '5Gi', status: 'Running' },
    { name: 'auth-db', replicas: 1, image: 'postgres:16-alpine', storage: '2Gi', status: 'Running' },
    { name: 'redis', replicas: 1, image: 'redis:7-alpine', storage: '1Gi', status: 'Running' },
    { name: 'rabbitmq', replicas: 1, image: 'rabbitmq:3.13-alpine', storage: '1Gi', status: 'Running' },
  ],
  services: [
    { name: 'nginx', type: 'NodePort', ports: '80:30080' },
    { name: 'gateway', type: 'ClusterIP', ports: '8080' },
    { name: 'auth-service', type: 'ClusterIP', ports: '8001, 50051' },
    { name: 'web', type: 'ClusterIP', ports: '8000' },
    { name: 'db', type: 'Headless', ports: '5432' },
    { name: 'auth-db', type: 'Headless', ports: '5432' },
    { name: 'redis', type: 'Headless', ports: '6379' },
    { name: 'rabbitmq', type: 'Headless', ports: '5672, 15672' },
  ],
  pvcs: [
    { name: 'media-pvc', size: '5Gi', access: 'RWO' },
    { name: 'backend-logs-pvc', size: '1Gi', access: 'RWO' },
    { name: 'db data', size: '5Gi', access: 'RWO (volumeClaimTemplate)' },
    { name: 'auth-db data', size: '2Gi', access: 'RWO (volumeClaimTemplate)' },
    { name: 'redis data', size: '1Gi', access: 'RWO (volumeClaimTemplate)' },
    { name: 'rabbitmq data', size: '1Gi', access: 'RWO (volumeClaimTemplate)' },
  ],
};

export const techStack = [
  { name: 'React 19', category: 'Frontend', icon: 'Code2' },
  { name: 'TypeScript', category: 'Frontend', icon: 'FileCode2' },
  { name: 'Vite 6', category: 'Frontend', icon: 'Zap' },
  { name: 'TailwindCSS', category: 'Frontend', icon: 'Palette' },
  { name: 'Framer Motion', category: 'Frontend', icon: 'Move' },
  { name: 'Django 5', category: 'Backend', icon: 'Server' },
  { name: 'FastAPI', category: 'Backend', icon: 'Rocket' },
  { name: 'Celery', category: 'Backend', icon: 'Clock' },
  { name: 'PostgreSQL 16', category: 'Database', icon: 'Database' },
  { name: 'Redis 7', category: 'Database', icon: 'HardDrive' },
  { name: 'RabbitMQ', category: 'Infra', icon: 'MessageSquare' },
  { name: 'Kubernetes (k3s)', category: 'Infra', icon: 'Container' },
  { name: 'Nginx', category: 'Infra', icon: 'Globe' },
  { name: 'Docker', category: 'Infra', icon: 'Box' },
  { name: 'Groq AI', category: 'AI', icon: 'Brain' },
  { name: 'Gemini AI', category: 'AI', icon: 'Sparkles' },
];
