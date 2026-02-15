import { motion } from 'framer-motion';
import { Mail, AtSign, ArrowRight } from 'lucide-react';
import { AuthInput } from './AuthInput';
import { AuthDivider } from './AuthDivider';
import { GoogleLoginButton } from './GoogleLoginButton';

interface Props {
  formData: { email: string; username: string };
  onChange: (field: string, value: string) => void;
  onNext: () => void;
  onGoogle: (credential: string) => void;
  direction: number;
}

const slideVariants = {
  enter: (d: number) => ({ x: d > 0 ? 30 : -30, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (d: number) => ({ x: d > 0 ? -30 : 30, opacity: 0 }),
};

export function RegisterStepAccount({ formData, onChange, onNext, onGoogle, direction }: Props) {
  const valid = formData.email.length > 0 && formData.username.length >= 3;

  return (
    <motion.div custom={direction} variants={slideVariants} initial="enter" animate="center" exit="exit" transition={{ duration: 0.25 }}>
      <div className="rounded-2xl border border-border/50 bg-card p-6 shadow-card lg:p-7">
        <div className="space-y-4">
          <AuthInput icon={Mail} label="Email" type="email" placeholder="you@example.com" value={formData.email} onChange={(v) => onChange('email', v)} />
          <AuthInput icon={AtSign} label="Username" placeholder="your_username" value={formData.username} onChange={(v) => onChange('username', v)} />
          <AuthDivider />
          <GoogleLoginButton onSuccess={onGoogle} />
          <button
            type="button"
            onClick={onNext}
            disabled={!valid}
            className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 text-sm font-semibold text-white transition-all hover:shadow-lg disabled:opacity-50"
          >
            Continue <ArrowRight className="h-4 w-4" />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
