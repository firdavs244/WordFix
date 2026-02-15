import { motion } from 'framer-motion';
import { User, ArrowLeft, Loader2 } from 'lucide-react';
import { AuthInput } from './AuthInput';

interface Props {
  formData: { email: string; username: string; fullName: string };
  onChange: (field: string, value: string) => void;
  onBack: () => void;
  onSubmit: () => void;
  isLoading: boolean;
  direction: number;
}

const slideVariants = {
  enter: (d: number) => ({ x: d > 0 ? 30 : -30, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (d: number) => ({ x: d > 0 ? -30 : 30, opacity: 0 }),
};

export function RegisterStepConfirm({ formData, onChange, onBack, onSubmit, isLoading, direction }: Props) {
  return (
    <motion.div custom={direction} variants={slideVariants} initial="enter" animate="center" exit="exit" transition={{ duration: 0.25 }}>
      <div className="rounded-2xl border border-border/50 bg-card p-6 shadow-card lg:p-7">
        <div className="space-y-4">
          <div>
            <AuthInput icon={User} label="Full Name (optional)" placeholder="Enter your full name" value={formData.fullName} onChange={(v) => onChange('fullName', v)} />
            <p className="-mt-1 text-[10px] text-muted-foreground/50">You can add this later</p>
          </div>

          <div className="space-y-2.5 rounded-xl border border-border/30 bg-muted/30 p-4">
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Email</span>
              <span className="max-w-[180px] truncate text-sm font-medium">{formData.email}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Username</span>
              <span className="text-sm font-medium">{formData.username}</span>
            </div>
          </div>

          <div className="flex gap-3">
            <button type="button" onClick={onBack} className="flex h-11 flex-1 items-center justify-center gap-1 rounded-xl border border-border/50 text-sm font-medium transition hover:bg-muted/30">
              <ArrowLeft className="h-4 w-4" /> Back
            </button>
            <button type="button" onClick={onSubmit} disabled={isLoading} className="flex h-11 flex-1 items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 text-sm font-semibold text-white transition-all hover:shadow-lg disabled:opacity-60">
              {isLoading ? <><Loader2 className="h-4 w-4 animate-spin" /> Creating...</> : 'Create Account'}
            </button>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
