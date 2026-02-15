import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, CheckCircle2, Circle } from 'lucide-react';
import { PasswordInput } from './PasswordInput';
import { PasswordStrengthBar } from './PasswordStrengthBar';
import { usePasswordValidation } from '../hooks/usePasswordValidation';

interface Props {
  formData: { password: string; confirmPassword: string };
  onChange: (field: string, value: string) => void;
  onNext: () => void;
  onBack: () => void;
  direction: number;
}

const slideVariants = {
  enter: (d: number) => ({ x: d > 0 ? 30 : -30, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (d: number) => ({ x: d > 0 ? -30 : 30, opacity: 0 }),
};

export function RegisterStepPassword({ formData, onChange, onNext, onBack, direction }: Props) {
  const { hasMinLength, hasNumber, passwordsMatch, isValid } = usePasswordValidation(formData.password, formData.confirmPassword);

  const rules = [
    { ok: hasMinLength, text: 'At least 8 characters' },
    { ok: hasNumber, text: 'Contains a number' },
    { ok: passwordsMatch, text: 'Passwords match' },
  ];

  return (
    <motion.div custom={direction} variants={slideVariants} initial="enter" animate="center" exit="exit" transition={{ duration: 0.25 }}>
      <div className="rounded-2xl border border-border/50 bg-card p-6 shadow-card lg:p-7">
        <div className="space-y-4">
          <PasswordInput label="Password" placeholder="Create a strong password" value={formData.password} onChange={(v) => onChange('password', v)} />
          <PasswordStrengthBar password={formData.password} />
          <div className="mt-2 space-y-1">
            {rules.map((r) => (
              <div key={r.text} className="flex items-center gap-2 text-[11px]">
                {r.ok ? <CheckCircle2 className="h-3 w-3 text-success" /> : <Circle className="h-3 w-3 text-muted-foreground/30" />}
                <span className={r.ok ? 'text-success' : 'text-muted-foreground/50'}>{r.text}</span>
              </div>
            ))}
          </div>
          <PasswordInput label="Confirm Password" placeholder="Repeat your password" value={formData.confirmPassword} onChange={(v) => onChange('confirmPassword', v)} />
          <div className="flex gap-3">
            <button type="button" onClick={onBack} className="flex h-11 flex-1 items-center justify-center gap-1 rounded-xl border border-border/50 text-sm font-medium transition hover:bg-muted/30">
              <ArrowLeft className="h-4 w-4" /> Back
            </button>
            <button type="button" onClick={onNext} disabled={!isValid} className="flex h-11 flex-1 items-center justify-center gap-1 rounded-xl bg-gradient-to-r from-primary to-primary/90 text-sm font-semibold text-white transition-all hover:shadow-lg disabled:opacity-50">
              Continue <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
