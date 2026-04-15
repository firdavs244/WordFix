import Hero from './components/Hero';
import Architecture from './components/Architecture';
import KubernetesInfra from './components/KubernetesInfra';
import RequestFlow from './components/RequestFlow';
import TechStack from './components/TechStack';

function App() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-[var(--color-bg-primary)]/80 border-b border-[var(--color-border-glass)]">
        <div className="max-w-6xl mx-auto px-6 py-3 flex items-center justify-between">
          <span className="text-lg font-bold gradient-text">WordFix</span>
          <div className="hidden md:flex items-center gap-6 text-sm text-[var(--color-text-secondary)]">
            <a href="#architecture" className="hover:text-white transition-colors">Architecture</a>
            <a href="#kubernetes" className="hover:text-white transition-colors">Kubernetes</a>
            <a href="#request-flow" className="hover:text-white transition-colors">Request Flow</a>
            <a href="#tech-stack" className="hover:text-white transition-colors">Tech Stack</a>
          </div>
          <a
            href="http://161.97.129.229:30080"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs px-3 py-1.5 rounded-full border border-[var(--color-border-glass)] text-[var(--color-text-secondary)] hover:text-white hover:border-[var(--color-accent-purple)] transition-colors"
          >
            Open App
          </a>
        </div>
      </nav>

      <Hero />
      <Architecture />
      <KubernetesInfra />
      <RequestFlow />
      <TechStack />

      {/* Footer */}
      <footer className="py-12 px-6 text-center border-t border-[var(--color-border-glass)]">
        <p className="text-sm text-[var(--color-text-muted)]">
          WordFix Technical Showcase &mdash; Built with React, TypeScript, Tailwind, Framer Motion
        </p>
        <p className="text-xs text-[var(--color-text-muted)] mt-2">
          Deployed on k3s &middot; 161.97.129.229
        </p>
      </footer>
    </div>
  );
}

export default App;
