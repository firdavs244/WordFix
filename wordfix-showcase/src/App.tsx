import Hero from './components/Hero';
import Architecture from './components/Architecture';
import KubernetesInfra from './components/KubernetesInfra';
import RequestFlow from './components/RequestFlow';
import DDDArchitecture from './components/DDDArchitecture';
import TechStack from './components/TechStack';

function App() {
  return (
    <div className="min-h-screen">
      <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-[var(--color-bg-primary)]/80 border-b border-[var(--color-border-glass)]">
        <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
          <span className="text-lg font-bold gradient-text">WordFix</span>
          <div className="hidden lg:flex items-center gap-6 text-sm text-[var(--color-text-secondary)]">
            <a href="#architecture" className="hover:text-white transition-colors">Arxitektura</a>
            <a href="#kubernetes" className="hover:text-white transition-colors">Kubernetes</a>
            <a href="#request-flow" className="hover:text-white transition-colors">So'rov Oqimi</a>
            <a href="#ddd" className="hover:text-white transition-colors">DDD</a>
            <a href="#tech-stack" className="hover:text-white transition-colors">Texnologiyalar</a>
          </div>
          <a
            href="http://161.97.129.229:30080"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs px-4 py-2 rounded-full border border-[var(--color-border-glass)] text-[var(--color-text-secondary)] hover:text-white hover:border-[var(--color-accent-purple)] transition-colors"
          >
            Ilovani Ochish
          </a>
        </div>
      </nav>

      <Hero />
      <Architecture />
      <KubernetesInfra />
      <RequestFlow />
      <DDDArchitecture />
      <TechStack />

      <footer className="py-16 px-6 text-center border-t border-[var(--color-border-glass)]">
        <p className="text-sm text-[var(--color-text-muted)]">
          WordFix Texnik Namoyish &mdash; React, TypeScript, Tailwind, Framer Motion
        </p>
        <p className="text-xs text-[var(--color-text-muted)] mt-3">
          k3s da deploy qilingan &middot; 161.97.129.229
        </p>
      </footer>
    </div>
  );
}

export default App;
