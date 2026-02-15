import { motion } from 'framer-motion';
import { Check } from 'lucide-react';

const STEPS = ['Account', 'Security', 'Confirm'];

export function RegisterStepIndicator({ currentStep }: { currentStep: number }) {
  return (
    <div className="mb-2">
      <div className="flex items-center justify-center gap-0">
        {STEPS.map((label, i) => (
          <div key={label} className="flex items-center">
            {/* Circle */}
            <div className="flex flex-col items-center">
              <motion.div
                className={`flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold transition-colors ${
                  i < currentStep
                    ? 'border-2 border-primary bg-primary text-white shadow-glow-primary'
                    : i === currentStep
                      ? 'border-2 border-primary bg-primary text-white ring-4 ring-primary/15'
                      : 'border-2 border-border/50 bg-muted text-muted-foreground'
                }`}
                animate={i === currentStep ? { scale: [1, 1.05, 1] } : {}}
                transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
              >
                {i < currentStep ? <Check className="h-3.5 w-3.5" /> : i + 1}
              </motion.div>
              <span className={`mt-2 text-[10px] font-medium ${
                i === currentStep ? 'font-semibold text-primary' : 'text-muted-foreground/60'
              }`}>
                {label}
              </span>
            </div>
            {/* Connecting line */}
            {i < STEPS.length - 1 && (
              <motion.div
                className={`mx-2 mb-5 h-0.5 w-16 rounded-full ${i < currentStep ? 'bg-primary' : 'bg-border/40'}`}
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ duration: 0.4 }}
                style={{ originX: 0 }}
              />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
