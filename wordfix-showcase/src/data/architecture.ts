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
  { id: 'browser', name: 'Brauzer', tech: 'React 19 + TypeScript', port: '-', description: 'Vite 6, TailwindCSS, Framer Motion bilan qurilgan SPA frontend', category: 'frontend', x: 450, y: 30 },
  { id: 'nginx', name: 'Nginx', tech: 'nginx:alpine', port: '30080', description: 'Teskari proksi, statik frontendni xizmat qiladi, /api/* ni backendga yo\'naltiradi', category: 'frontend', x: 450, y: 130 },
  { id: 'gateway', name: 'API Gateway', tech: 'FastAPI + Python', port: '8080', description: 'So\'rovlarni auth-service yoki Django monolitga yo\'naltiradi, JWT tekshiradi', category: 'backend', x: 450, y: 240 },
  { id: 'auth', name: 'Auth Service', tech: 'FastAPI + SQLAlchemy', port: '8001/50051', description: 'JWT autentifikatsiya, Google OAuth, foydalanuvchi ro\'yxatdan o\'tishi, gRPC interfeys', category: 'backend', x: 200, y: 350 },
  { id: 'web', name: 'Django Monolit', tech: 'Django 5 + DRF', port: '8000', description: 'So\'zlar, testlar, o\'yinlar, dashboard, onboarding, AI funksiyalari', category: 'backend', x: 700, y: 350 },
  { id: 'celery-worker', name: 'Celery Worker', tech: 'Celery 5 + Python', port: '-', description: 'Asinxron vazifalar: AI generatsiya, takroriy o\'rganish', category: 'backend', x: 850, y: 480 },
  { id: 'celery-beat', name: 'Celery Beat', tech: 'Celery 5 Beat', port: '-', description: 'Davriy vazifalar rejalashtiruvchi: kunlik takrorlash, statistika', category: 'backend', x: 700, y: 480 },
  { id: 'auth-db', name: 'Auth DB', tech: 'PostgreSQL 16', port: '5432', description: 'Auth-service uchun foydalanuvchilar, sessiyalar, OAuth tokenlar', category: 'database', x: 100, y: 480 },
  { id: 'db', name: 'Asosiy DB', tech: 'PostgreSQL 16', port: '5432', description: 'So\'zlar, testlar, o\'yinlar, foydalanuvchi progressi, takrorlashlar', category: 'database', x: 450, y: 550 },
  { id: 'redis', name: 'Redis', tech: 'Redis 7', port: '6379', description: 'Keshlash, sessiya saqlash, Celery natijalar backnedi', category: 'infra', x: 600, y: 480 },
  { id: 'rabbitmq', name: 'RabbitMQ', tech: 'RabbitMQ 3.13', port: '5672', description: 'Celery vazifalari va servislar aro xabarlar uchun broker', category: 'infra', x: 300, y: 480 },
];

export const connections: Connection[] = [
  { from: 'browser', to: 'nginx', label: 'HTTP :30080', protocol: 'HTTP' },
  { from: 'nginx', to: 'gateway', label: '/api/*', protocol: 'HTTP' },
  { from: 'gateway', to: 'auth', label: 'Auth yo\'nalish', protocol: 'HTTP' },
  { from: 'gateway', to: 'web', label: 'App yo\'nalish', protocol: 'HTTP' },
  { from: 'auth', to: 'auth-db', protocol: 'TCP' },
  { from: 'web', to: 'db', protocol: 'TCP' },
  { from: 'web', to: 'redis', protocol: 'TCP' },
  { from: 'web', to: 'rabbitmq', label: 'Vazifalar', protocol: 'AMQP' },
  { from: 'celery-worker', to: 'rabbitmq', label: 'Iste\'mol', protocol: 'AMQP' },
  { from: 'celery-worker', to: 'db', protocol: 'TCP' },
  { from: 'celery-worker', to: 'redis', label: 'Natijalar', protocol: 'TCP' },
  { from: 'celery-beat', to: 'rabbitmq', label: 'Rejalashtirish', protocol: 'AMQP' },
];

export const flowSteps: FlowStep[] = [
  { id: 1, title: 'Foydalanuvchi "Ro\'yxatdan o\'tish" bosadi', description: 'Brauzer /api/v1/auth/register/ ga POST so\'rov yuboradi: email, username, parol', from: 'browser', to: 'nginx', method: 'POST', path: '/api/v1/auth/register/', code: 'fetch("/api/v1/auth/register/", {\n  method: "POST",\n  body: JSON.stringify({\n    email, username, password\n  })\n})' },
  { id: 2, title: 'Nginx so\'rovni Gateway ga uzatadi', description: 'Nginx /api/ location bloki so\'rovni gateway:8080 ga proksileydi', from: 'nginx', to: 'gateway', method: 'POST', path: '/api/v1/auth/register/', code: 'location /api/ {\n  proxy_pass http://gateway:8080;\n}' },
  { id: 3, title: 'Gateway Auth Service ga yo\'naltiradi', description: 'Gateway AUTH_PATHS to\'plamini tekshiradi, /register/ mos keladi → auth-service:8001 ga yuboradi', from: 'gateway', to: 'auth', method: 'POST', path: '/auth/register/', code: 'AUTH_PATHS = {\n  "register","login","logout",...\n}\nif path_part in AUTH_PATHS:\n    forward_to(AUTH_SERVICE_URL)' },
  { id: 4, title: 'Auth Service foydalanuvchi yaratadi', description: 'Auth service parolni xeshlaydi, UUID generatsiya qiladi, auth bazasida foydalanuvchi yaratadi', from: 'auth', to: 'auth-db', method: 'INSERT', path: 'wordfix_auth.users', code: 'user = UserEntity(\n  id=uuid4(),\n  email=email,\n  password=hash(password)\n)\nawait user_repo.create(user)' },
  { id: 5, title: 'JWT tokenlar generatsiya qilinadi', description: 'Auth service user_id claim bilan access + refresh tokenlar yaratadi', from: 'auth', to: 'auth', code: 'access = create_jwt(\n  payload={\n    "user_id": str(user.id),\n    "token_type": "access"\n  },\n  secret=JWT_SECRET\n)' },
  { id: 6, title: 'Tokenlar brauzerga qaytadi', description: 'Javob: Auth → Gateway → Nginx → Brauzer. Tokenlar localStorage da saqlanadi', from: 'auth', to: 'browser', code: '{\n  "access": "eyJhbG...",\n  "refresh": "eyJhbG..."\n}' },
  { id: 7, title: 'Foydalanuvchi "Onboardingni o\'tkazib yuborish" bosadi', description: 'Brauzer POST /api/v1/auth/onboarding/skip/ ga Bearer token bilan yuboradi', from: 'browser', to: 'nginx', method: 'POST', path: '/api/v1/auth/onboarding/skip/' },
  { id: 8, title: 'Nginx → Gateway → Django', description: 'Gateway /onboarding/ AUTH_PATHS da emas, Django monolitga yo\'naltiradi', from: 'gateway', to: 'web', method: 'POST', path: '/api/v1/auth/onboarding/skip/', code: '# AUTH_PATHS da emas → Django\nforward_to(MONOLITH_URL)' },
  { id: 9, title: 'AutoProvisionJWT autentifikatsiya qiladi', description: 'Django JWT backend tokenni dekodlaydi, user_id Django bazasida yo\'q → avtomatik yaratish boshlanadi', from: 'web', to: 'web', code: 'class AutoProvisionJWTAuth:\n  def get_user(self, token):\n    try:\n      return super().get_user(token)\n    except AuthenticationFailed:\n      return self._provision_user(\n        token["user_id"])' },
  { id: 10, title: 'Auth Service dan profil so\'raladi', description: 'Django auth-service ichki API ga murojaat qilib to\'liq foydalanuvchi profilini oladi', from: 'web', to: 'auth', method: 'GET', path: '/auth/profile/', code: 'resp = httpx.get(\n  "http://auth-service:8001"\n  "/auth/profile/",\n  headers={"Authorization":\n    f"Bearer {token}"}\n)' },
  { id: 11, title: 'Auth Service foydalanuvchi ma\'lumotini so\'raydi', description: 'Auth service o\'z bazasidan to\'liq foydalanuvchi profilini oladi', from: 'auth', to: 'auth-db', method: 'SELECT', path: 'wordfix_auth.users' },
  { id: 12, title: 'Profil ma\'lumotlari qaytariladi', description: 'To\'liq foydalanuvchi: email, username, full_name, tillar, daraja', from: 'auth', to: 'web', code: '{\n  "id": "uuid",\n  "email": "user@email.com",\n  "username": "user123",\n  "native_language": "uz",\n  "learning_language": "en",\n  "proficiency_level": "A1"\n}' },
  { id: 13, title: 'Django bazasida foydalanuvchi yaratiladi', description: 'CustomUser.objects.get_or_create() auth-service ma\'lumotlari bilan, UserProgress yaratiladi', from: 'web', to: 'db', method: 'INSERT', path: 'wordfix.users + user_progress', code: 'user, created = CustomUser\\\n  .objects.get_or_create(\n    id=user_uuid,\n    defaults=profile_data\n  )\nUserProgress.objects\\\n  .get_or_create(user=user)' },
  { id: 14, title: 'Onboarding o\'tkazib yuborildi', description: 'Foydalanuvchi autentifikatsiya qilindi, has_completed_onboarding = True, javob 200 OK', from: 'web', to: 'db', method: 'UPDATE', path: 'wordfix.users', code: 'user.has_completed_onboarding\\\n  = True\nuser.save()' },
  { id: 15, title: 'Muvaffaqiyatli javob brauzerga', description: 'HTTP 200 qaytadi: Django → Gateway → Nginx → Brauzer', from: 'web', to: 'browser', code: '{"status": "success",\n "message": "Onboarding\n   o\'tkazib yuborildi"}' },
  { id: 16, title: 'Dashboard yuklanadi', description: 'Brauzer dashboard, so\'zlar, progress ma\'lumotlarini so\'raydi — hammasi autentifikatsiya bilan', from: 'browser', to: 'nginx', method: 'GET', path: '/api/v1/dashboard/' },
  { id: 17, title: 'AI so\'z generatsiyasi boshlandi', description: 'Foydalanuvchi so\'z qo\'shadi → Django RabbitMQ orqali Celery vazifa chiqaradi', from: 'web', to: 'rabbitmq', method: 'PUBLISH', path: 'celery task queue', code: 'generate_ai_content\\\n  .delay(word_id=word.id)' },
  { id: 18, title: 'Worker AI vazifani bajaradi', description: 'Celery worker vazifani oladi, Groq/Gemini API ga murojaat qilib misollar yaratadi', from: 'celery-worker', to: 'rabbitmq', method: 'CONSUME', code: '@app.task\ndef generate_ai_content(\n    word_id):\n  word = Word.objects.get(\n    id=word_id)\n  result = groq.generate(\n    examples_for=word.text)' },
  { id: 19, title: 'Natijalar saqlanadi', description: 'AI yaratgan kontent bazaga yoziladi, natija Redis da keshlanadi', from: 'celery-worker', to: 'db', method: 'UPDATE', path: 'wordfix.words', code: 'word.ai_examples = result\nword.save()\nredis.set(\n  f"word:{word_id}:ai",\n  result)' },
];

export const k8sResources = {
  deployments: [
    { name: 'nginx', replicas: 1, image: 'wordfix/frontend:latest', status: 'Running' },
    { name: 'gateway', replicas: 1, image: 'wordfix/api-gateway:latest', status: 'Running' },
    { name: 'auth-service', replicas: 1, image: 'wordfix/auth-service:latest', status: 'Running' },
    { name: 'web', replicas: 1, image: 'wordfix/monolith:latest', status: 'Running' },
    { name: 'celery-worker', replicas: 1, image: 'wordfix/monolith:latest', status: 'Running' },
    { name: 'celery-beat', replicas: 1, image: 'wordfix/monolith:latest', status: 'Running' },
    { name: 'showcase', replicas: 1, image: 'wordfix/showcase:latest', status: 'Running' },
  ],
  statefulSets: [
    { name: 'db', replicas: 1, image: 'postgres:16-alpine', storage: '5Gi', status: 'Running' },
    { name: 'auth-db', replicas: 1, image: 'postgres:16-alpine', storage: '2Gi', status: 'Running' },
    { name: 'redis', replicas: 1, image: 'redis:7-alpine', storage: '1Gi', status: 'Running' },
    { name: 'rabbitmq', replicas: 1, image: 'rabbitmq:3.13-alpine', storage: '1Gi', status: 'Running' },
  ],
  services: [
    { name: 'nginx', type: 'NodePort', ports: '80:30080' },
    { name: 'showcase', type: 'NodePort', ports: '80:30081' },
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
  { name: 'PostgreSQL 16', category: 'Ma\'lumotlar bazasi', icon: 'Database' },
  { name: 'Redis 7', category: 'Ma\'lumotlar bazasi', icon: 'HardDrive' },
  { name: 'RabbitMQ', category: 'Infratuzilma', icon: 'MessageSquare' },
  { name: 'Kubernetes (k3s)', category: 'Infratuzilma', icon: 'Container' },
  { name: 'Nginx', category: 'Infratuzilma', icon: 'Globe' },
  { name: 'Docker', category: 'Infratuzilma', icon: 'Box' },
  { name: 'Groq AI', category: 'Sun\'iy intellekt', icon: 'Brain' },
  { name: 'Gemini AI', category: 'Sun\'iy intellekt', icon: 'Sparkles' },
];

// DDD File Structure Data
export interface FileTreeNode {
  name: string;
  type: 'file' | 'folder';
  description?: string;
  layer?: 'domain' | 'application' | 'infrastructure' | 'presentation' | 'config';
  children?: FileTreeNode[];
}

export const DDD_LAYER_COLORS = {
  domain: { bg: '#1a2e1a', border: '#22c55e', text: '#86efac', label: 'Domain' },
  application: { bg: '#1a1a2e', border: '#3b82f6', text: '#93c5fd', label: 'Application' },
  infrastructure: { bg: '#2e1a2e', border: '#a855f7', text: '#d8b4fe', label: 'Infrastructure' },
  presentation: { bg: '#2e2a1a', border: '#f59e0b', text: '#fcd34d', label: 'Presentation' },
  config: { bg: '#1a2a2e', border: '#6b7280', text: '#d1d5db', label: 'Konfiguratsiya' },
};

export const dddExplanation = {
  title: 'Domain-Driven Design (DDD) arxitekturasi',
  description: 'Har bir bounded context (users, words, immersive) bir xil to\'rt qatlamli DDD strukturaga ega. Bu qatlamlar bir-biridan mustaqil va faqat yuqoridan pastga bog\'langan.',
  layers: [
    {
      name: 'Domain',
      key: 'domain' as const,
      description: 'Sof Python kodi — hech qanday framework import yo\'q. Biznes logika, entity\'lar, value object\'lar va repository interfeyslari.',
      files: 'entities.py, value_objects.py, repositories.py (ABC), services/',
      principle: 'Framework mustaqilligi — Django, FastAPI yoki boshqa framework o\'zgarganda bu qatlam o\'zgarmaydi',
    },
    {
      name: 'Application',
      key: 'application' as const,
      description: 'Use Case\'lar — har bir biznes operatsiya uchun bitta klass. Repository interfeyslari orqali constructor injection.',
      files: 'use_cases/ — AddWordUseCase, LoginUserUseCase, StartReviewUseCase va boshqalar',
      principle: 'Bitta mas\'uliyat — har bir use case faqat bitta biznes operatsiyani bajaradi',
    },
    {
      name: 'Infrastructure',
      key: 'infrastructure' as const,
      description: 'Framework-ga bog\'liq implementatsiyalar. Django ORM modellari, repository implementatsiyalari, Celery vazifalar, tashqi servislar.',
      files: 'models/, repositories/, tasks.py, adapters.py',
      principle: 'Dependency Inversion — domain interfeyslari shu yerda implement qilinadi',
    },
    {
      name: 'Presentation',
      key: 'presentation' as const,
      description: 'HTTP API yuzasi. DRF View\'lar, serializer\'lar, URL routing, dependency factory\'lar.',
      files: 'views/, serializers/, urls.py, dependencies/',
      principle: 'Yupqa qatlam — faqat HTTP bilan ishlaydi, biznes logika use case\'larga delegatsiya qilinadi',
    },
  ],
};

export const monolithTree: FileTreeNode = {
  name: 'wordfix-backend/', type: 'folder', description: 'Django 5 Monolit — DDD arxitektura', children: [
    { name: 'config/', type: 'folder', layer: 'config', description: 'Loyiha konfiguratsiyasi', children: [
      { name: 'settings/', type: 'folder', description: 'Muhit sozlamalari', children: [
        { name: 'base.py', type: 'file', description: 'Umumiy sozlamalar, REST Framework, JWT, DB konfiguratsiya' },
        { name: 'production.py', type: 'file', description: 'Prod muhit — DEBUG=False, xavfsizlik' },
        { name: 'development.py', type: 'file', description: 'Dev muhit — DEBUG=True' },
      ]},
      { name: 'urls.py', type: 'file', description: 'Asosiy URL router — /api/v1/*' },
      { name: 'celery.py', type: 'file', description: 'Celery dastur konfiguratsiyasi' },
      { name: 'wsgi.py', type: 'file', description: 'WSGI server kirish nuqtasi' },
    ]},
    { name: 'core/', type: 'folder', description: 'Umumiy yadro — AI provayderlar va TTS', children: [
      { name: 'interfaces/', type: 'folder', layer: 'domain', description: 'Abstrakt interfeyalar', children: [
        { name: 'ai_provider.py', type: 'file', description: 'AbstractAIProvider — barcha AI provayderlar uchun interfeys' },
        { name: 'tts_provider.py', type: 'file', description: 'AbstractTTSProvider — Text-to-Speech interfeys' },
      ]},
      { name: 'services/ai/', type: 'folder', layer: 'infrastructure', description: 'AI provayder implementatsiyalari', children: [
        { name: 'ai_factory.py', type: 'file', description: 'Factory pattern — Groq/OpenAI/Gemini tanlaydi' },
        { name: 'groq_provider.py', type: 'file', description: 'Groq AI implementatsiyasi' },
        { name: 'gemini_provider.py', type: 'file', description: 'Google Gemini implementatsiyasi' },
        { name: 'openai_provider.py', type: 'file', description: 'OpenAI implementatsiyasi' },
        { name: 'prompts/', type: 'folder', description: 'AI prompt shablonlari — enrichment, game, test, chat' },
      ]},
    ]},
    { name: 'apps/', type: 'folder', description: 'Bounded Context\'lar (DDD)', children: [
      { name: 'common/', type: 'folder', layer: 'infrastructure', description: 'Umumiy infratuzilma moduli', children: [
        { name: 'authentication.py', type: 'file', description: 'AutoProvisionJWTAuthentication — auth-service va Django o\'rtasidagi ko\'prik' },
        { name: 'circuit_breaker.py', type: 'file', description: 'Circuit Breaker pattern — tashqi servislar uchun xavfsizlik' },
        { name: 'exceptions.py', type: 'file', description: 'Domain exception\'lar iyerarxiyasi' },
        { name: 'middleware/', type: 'folder', description: 'X-Request-ID propagatsiyasi' },
        { name: 'pagination.py', type: 'file', description: 'Standartlashtirilgan cursor/page paginatsiya' },
        { name: 'health.py', type: 'file', description: 'Health check registr — barcha servislarni tekshiradi' },
      ]},
      { name: 'users/', type: 'folder', description: 'Foydalanuvchilar Bounded Context', children: [
        { name: 'domain/', type: 'folder', layer: 'domain', description: 'Sof biznes logika', children: [
          { name: 'entities.py', type: 'file', description: 'UserEntity dataclass — sof Python' },
          { name: 'value_objects.py', type: 'file', description: 'Email, Password — frozen dataclass\'lar' },
          { name: 'repositories.py', type: 'file', description: 'AbstractUserRepository (ABC) — interfeys' },
          { name: 'services/', type: 'folder', description: 'badge, xp, onboarding, notification servislar' },
        ]},
        { name: 'application/', type: 'folder', layer: 'application', description: 'Use Case\'lar', children: [
          { name: 'use_cases/', type: 'folder', description: 'Register, Login, GetProfile, UpdateProfile' },
          { name: 'learning_use_cases/', type: 'folder', description: 'Profil sinxronlash, xato tahlili, tavsiyalar' },
        ]},
        { name: 'infrastructure/', type: 'folder', layer: 'infrastructure', description: 'Django implements', children: [
          { name: 'models/', type: 'folder', description: 'CustomUser, UserProgress, Streak, XPTransaction ORM' },
          { name: 'repositories/', type: 'folder', description: 'DjangoUserRepository — ABC implementatsiyasi' },
          { name: 'tasks.py', type: 'file', description: 'Celery asinxron vazifalar' },
        ]},
        { name: 'presentation/', type: 'folder', layer: 'presentation', description: 'HTTP API', children: [
          { name: 'views/', type: 'folder', description: 'Auth, Profile DRF view\'lar' },
          { name: 'serializers.py', type: 'file', description: 'So\'rov/javob serializer\'lar' },
          { name: 'urls.py', type: 'file', description: '/api/v1/auth/* URL yo\'nalishlari' },
          { name: 'dependencies.py', type: 'file', description: 'Use-case factory — DI (Dependency Injection)' },
        ]},
      ]},
      { name: 'words/', type: 'folder', description: 'So\'zlar Bounded Context (eng katta)', children: [
        { name: 'domain/', type: 'folder', layer: 'domain', description: 'Sof biznes logika', children: [
          { name: 'value_objects.py', type: 'file', description: 'WordText, Definition, MasteryLevel' },
          { name: 'entities/', type: 'folder', description: 'WordEntity, ReviewSession, TestSession, GameSession' },
          { name: 'repositories/', type: 'folder', description: 'AbstractWordRepo, AbstractReviewRepo va boshqalar' },
          { name: 'services/', type: 'folder', description: 'SM-2 spaced repetition, combo/streak logika' },
        ]},
        { name: 'application/', type: 'folder', layer: 'application', description: 'Use Case\'lar', children: [
          { name: 'use_cases/', type: 'folder', description: 'CRUD, Review, Enrichment, Chat, Analytics, Import' },
          { name: 'use_cases/games/', type: 'folder', description: 'Word Match, Speed Round, Story Builder, Listening' },
          { name: 'use_cases/testing/', type: 'folder', description: 'AI test generatsiya, test sessiya boshqaruvi' },
        ]},
        { name: 'infrastructure/', type: 'folder', layer: 'infrastructure', description: 'Django implements', children: [
          { name: 'models/', type: 'folder', description: 'Word, Review, Test, Game, Chat, Challenge ORM' },
          { name: 'repositories/', type: 'folder', description: '9 ta repository implementatsiyasi' },
          { name: 'tasks.py', type: 'file', description: 'AI enrichment, kontent generatsiya vazifalari' },
        ]},
        { name: 'presentation/', type: 'folder', layer: 'presentation', description: 'HTTP API', children: [
          { name: 'views/', type: 'folder', description: '12 ta view moduli — har bir funksiya uchun' },
          { name: 'serializers/', type: 'folder', description: '9 ta serializer moduli' },
          { name: 'dependencies/', type: 'folder', description: '12 ta DI factory — har bir use case uchun' },
          { name: '*.urls.py', type: 'file', description: '8 ta URL modul: words, review, tests, games, chat...' },
        ]},
      ]},
      { name: 'immersive/', type: 'folder', description: 'Immersive o\'rganish Bounded Context', children: [
        { name: 'domain/', type: 'folder', layer: 'domain', description: 'Scenario, NPC, Session, Scoring entity\'lar' },
        { name: 'application/', type: 'folder', layer: 'application', description: 'Ssenariy, sessiya, suhbat use case\'lari' },
        { name: 'infrastructure/', type: 'folder', layer: 'infrastructure', description: 'ORM, repo, Groq STT, TTS servislar' },
        { name: 'presentation/', type: 'folder', layer: 'presentation', description: 'Immersive API view\'lar va serializer\'lar' },
      ]},
    ]},
  ],
};

export const authServiceTree: FileTreeNode = {
  name: 'services/auth-service/', type: 'folder', description: 'FastAPI + SQLAlchemy Mikroservis', children: [
    { name: 'app/', type: 'folder', children: [
      { name: 'main.py', type: 'file', layer: 'config', description: 'FastAPI dastur + gRPC server boshqaruvi' },
      { name: 'config.py', type: 'file', layer: 'config', description: 'Pydantic Settings — DB, JWT, Redis, OAuth' },
      { name: 'database.py', type: 'file', layer: 'infrastructure', description: 'SQLAlchemy async engine + session factory' },
      { name: 'domain/', type: 'folder', layer: 'domain', children: [
        { name: 'entities.py', type: 'file', description: 'UserEntity — monolitdagi entity bilan bir xil' },
        { name: 'repositories.py', type: 'file', description: 'AbstractUserRepository (async ABC)' },
      ]},
      { name: 'application/', type: 'folder', layer: 'application', children: [
        { name: 'use_cases/', type: 'folder', description: 'Register, Login, Logout, TokenRefresh, GoogleLogin, Profile' },
      ]},
      { name: 'infrastructure/', type: 'folder', layer: 'infrastructure', children: [
        { name: 'models.py', type: 'file', description: 'SQLAlchemy User modeli' },
        { name: 'repositories.py', type: 'file', description: 'SQLAlchemy async repository' },
        { name: 'jwt_service.py', type: 'file', description: 'JWT token yaratish/tekshirish + Redis qora ro\'yxat' },
        { name: 'password.py', type: 'file', description: 'PBKDF2 xeshlash — Django bilan mos format' },
        { name: 'google_oauth.py', type: 'file', description: 'Google token tekshirish' },
      ]},
      { name: 'presentation/', type: 'folder', layer: 'presentation', children: [
        { name: 'schemas.py', type: 'file', description: 'Pydantic so\'rov/javob modellari' },
        { name: 'dependencies.py', type: 'file', description: 'FastAPI Depends() DI factory\'lar' },
        { name: 'routes/', type: 'folder', description: 'auth, google, profile, health endpointlar' },
      ]},
      { name: 'grpc/', type: 'folder', layer: 'presentation', description: 'gRPC transport qatlami', children: [
        { name: 'server.py', type: 'file', description: 'gRPC server (port 50051)' },
        { name: 'servicers/', type: 'folder', description: 'AuthService + UserService gRPC handler\'lar' },
      ]},
    ]},
    { name: 'alembic/', type: 'folder', layer: 'infrastructure', description: 'Ma\'lumotlar bazasi migratsiyalari' },
  ],
};

export const gatewayTree: FileTreeNode = {
  name: 'services/api-gateway/', type: 'folder', description: 'FastAPI API Gateway — routing + proxy', children: [
    { name: 'app/', type: 'folder', children: [
      { name: 'main.py', type: 'file', layer: 'config', description: 'FastAPI dastur, middleware stack, route registratsiya' },
      { name: 'config.py', type: 'file', layer: 'config', description: 'AUTH_SERVICE_URL, MONOLITH_URL, JWT konfiguratsiya' },
      { name: 'middleware/', type: 'folder', layer: 'infrastructure', children: [
        { name: 'request_id.py', type: 'file', description: 'X-Request-ID propagatsiya — distributed tracing' },
      ]},
      { name: 'routes/', type: 'folder', layer: 'presentation', children: [
        { name: 'auth.py', type: 'file', description: 'Aqlli router — AUTH_PATHS → auth-service, qolganlar → Django' },
        { name: 'monolith.py', type: 'file', description: 'Catch-all proxy → Django, X-User-ID header inject qiladi' },
        { name: 'health.py', type: 'file', description: 'Agregatsiyalangan health — ikkala servisni ping qiladi' },
      ]},
      { name: 'services/', type: 'folder', layer: 'infrastructure', children: [
        { name: 'proxy.py', type: 'file', description: 'httpx.AsyncClient — connection pooling bilan proksi' },
      ]},
    ]},
  ],
};
