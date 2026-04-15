import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect, useCallback, useRef } from 'react';
import { flowSteps, services, CATEGORY_COLORS } from '../data/architecture';

const STEP_DURATION = 2500;

export default function RequestFlow() {
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1);
  const intervalRef = useRef<number | null>(null);

  const step = flowSteps[currentStep];
  const fromNode = services.find((s) => s.id === step.from);
  const toNode = services.find((s) => s.id === step.to);

  const clearTimer = useCallback(() => {
    if (intervalRef.current) { clearInterval(intervalRef.current); intervalRef.current = null; }
  }, []);

  useEffect(() => {
    clearTimer();
    if (isPlaying) {
      intervalRef.current = window.setInterval(() => {
        setCurrentStep((s) => { if (s >= flowSteps.length - 1) { setIsPlaying(false); return s; } return s + 1; });
      }, STEP_DURATION / speed);
    }
    return clearTimer;
  }, [isPlaying, speed, clearTimer]);

  const reset = () => { setIsPlaying(false); setCurrentStep(0); };
  const stepForward = () => { if (currentStep < flowSteps.length - 1) setCurrentStep((s) => s + 1); };
  const stepBack = () => { if (currentStep > 0) setCurrentStep((s) => s - 1); };

  const nodePositions: Record<string, { x: number; y: number }> = {
    browser: { x: 100, y: 40 }, nginx: { x: 250, y: 40 }, gateway: { x: 400, y: 40 },
    auth: { x: 250, y: 140 }, web: { x: 550, y: 40 }, 'auth-db': { x: 100, y: 140 },
    db: { x: 550, y: 140 }, redis: { x: 700, y: 40 }, rabbitmq: { x: 700, y: 140 },
    'celery-worker': { x: 850, y: 90 }, 'celery-beat': { x: 850, y: 140 },
  };

  const fromPos = fromNode ? nodePositions[fromNode.id] : null;
  const toPos = toNode ? nodePositions[toNode.id] : null;

  return (
    <section id="request-flow" className="py-28 px-6">
      <motion.div initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-5xl font-bold text-center mb-5">
          <span className="gradient-text">So'rov Oqimi</span>
        </h2>
        <p className="text-center text-[var(--color-text-secondary)] mb-14 max-w-2xl mx-auto text-base leading-relaxed">
          Foydalanuvchi ro'yxatdan o'tishidan boshlab ma'lumotlar bazasiga yetguncha butun tizim bo'ylab
          so'rov oqimini kuzating — auth-service va Django o'rtasidagi avtomatik foydalanuvchi yaratish ham bor.
        </p>

        <div className="glass-card">
          {/* Flow visualization */}
          <div className="mb-8 overflow-x-auto">
            <svg viewBox="0 0 950 190" className="w-full" style={{ minHeight: 190 }}>
              {services.map((node) => {
                const pos = nodePositions[node.id];
                if (!pos) return null;
                const isActive = step.from === node.id || step.to === node.id;
                const colors = CATEGORY_COLORS[node.category];
                return (
                  <g key={node.id}>
                    <motion.rect
                      x={pos.x - 50} y={pos.y - 15} width={100} height={30} rx={8}
                      fill={isActive ? colors.bg : '#0f0f23'} stroke={isActive ? colors.border : '#1e293b'}
                      strokeWidth={isActive ? 2 : 1}
                      animate={{ filter: isActive ? `drop-shadow(0 0 10px ${colors.glow})` : 'none' }}
                      transition={{ duration: 0.3 }}
                    />
                    <text x={pos.x} y={pos.y + 4} textAnchor="middle" fill={isActive ? colors.text : '#475569'} fontSize={11} fontWeight={isActive ? 700 : 400}>
                      {node.name}
                    </text>
                  </g>
                );
              })}
              {fromPos && toPos && step.from !== step.to && (
                <motion.line x1={fromPos.x} y1={fromPos.y} x2={toPos.x} y2={toPos.y} stroke="url(#flowGradient)" strokeWidth={2} initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} key={currentStep} transition={{ duration: 0.6, ease: 'easeInOut' }} />
              )}
              {fromPos && toPos && step.from !== step.to && (
                <motion.circle r={5} fill="#3b82f6" filter="url(#glow)" initial={{ cx: fromPos.x, cy: fromPos.y }} animate={{ cx: toPos.x, cy: toPos.y }} key={`dot-${currentStep}`} transition={{ duration: 0.8, ease: 'easeInOut' }} />
              )}
              <defs>
                <linearGradient id="flowGradient" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stopColor="#3b82f6" /><stop offset="100%" stopColor="#8b5cf6" /></linearGradient>
                <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur" /><feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge></filter>
              </defs>
            </svg>
          </div>

          {/* Step details */}
          <AnimatePresence mode="wait">
            <motion.div key={currentStep} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.3 }} className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <span className="w-9 h-9 rounded-full bg-gradient-to-r from-[var(--color-accent-blue)] to-[var(--color-accent-purple)] flex items-center justify-center text-sm font-bold text-white shrink-0">{step.id}</span>
                  <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">{step.title}</h3>
                </div>
                <p className="text-sm text-[var(--color-text-secondary)] mb-4 leading-relaxed">{step.description}</p>
                {step.method && (
                  <div className="flex items-center gap-2.5 text-xs">
                    <span className={`px-2.5 py-1 rounded font-mono font-bold ${step.method === 'GET' ? 'bg-[var(--color-accent-emerald)]/20 text-[var(--color-accent-emerald)]' : step.method === 'POST' ? 'bg-[var(--color-accent-blue)]/20 text-[var(--color-accent-blue)]' : step.method === 'INSERT' || step.method === 'UPDATE' ? 'bg-[var(--color-accent-amber)]/20 text-[var(--color-accent-amber)]' : 'bg-[var(--color-accent-purple)]/20 text-[var(--color-accent-purple)]'}`}>{step.method}</span>
                    {step.path && <span className="font-mono text-[var(--color-text-muted)]">{step.path}</span>}
                  </div>
                )}
              </div>
              {step.code && (
                <div className="bg-[#0d1117] rounded-xl p-5 border border-[#21262d] overflow-x-auto">
                  <pre className="text-xs text-[#c9d1d9] font-mono whitespace-pre leading-relaxed">{step.code}</pre>
                </div>
              )}
            </motion.div>
          </AnimatePresence>

          {/* Controls */}
          <div className="flex items-center justify-center gap-3 flex-wrap mb-5">
            <button onClick={reset} className="px-4 py-2.5 rounded-lg bg-white/5 hover:bg-white/10 text-sm transition-colors text-[var(--color-text-secondary)]">Qayta boshlash</button>
            <button onClick={stepBack} disabled={currentStep === 0} className="px-4 py-2.5 rounded-lg bg-white/5 hover:bg-white/10 text-sm transition-colors disabled:opacity-30 text-[var(--color-text-secondary)]">Oldingi</button>
            <button onClick={() => setIsPlaying(!isPlaying)} className="px-8 py-2.5 rounded-lg bg-gradient-to-r from-[var(--color-accent-blue)] to-[var(--color-accent-purple)] text-white text-sm font-medium hover:opacity-90 transition-opacity">{isPlaying ? 'To\'xtatish' : 'Boshlash'}</button>
            <button onClick={stepForward} disabled={currentStep >= flowSteps.length - 1} className="px-4 py-2.5 rounded-lg bg-white/5 hover:bg-white/10 text-sm transition-colors disabled:opacity-30 text-[var(--color-text-secondary)]">Keyingi</button>
            <div className="flex items-center gap-2 ml-2">
              <span className="text-xs text-[var(--color-text-muted)]">Tezlik:</span>
              {[0.5, 1, 2].map((s) => (
                <button key={s} onClick={() => setSpeed(s)} className={`px-2.5 py-1 rounded text-xs transition-colors ${speed === s ? 'bg-[var(--color-accent-purple)] text-white' : 'bg-white/5 text-[var(--color-text-muted)] hover:bg-white/10'}`}>{s}x</button>
              ))}
            </div>
          </div>

          {/* Progress bar */}
          <div className="flex gap-1">
            {flowSteps.map((_, i) => (
              <button key={i} onClick={() => { setCurrentStep(i); setIsPlaying(false); }} className="flex-1 h-2 rounded-full transition-colors cursor-pointer" style={{ background: i <= currentStep ? 'linear-gradient(90deg, var(--color-accent-blue), var(--color-accent-purple))' : 'rgba(255,255,255,0.05)' }} />
            ))}
          </div>
          <div className="text-center mt-3 text-xs text-[var(--color-text-muted)]">{currentStep + 1}-qadam / {flowSteps.length} ta qadamdan</div>
        </div>
      </motion.div>
    </section>
  );
}
