import { type LucideIcon } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface AuthInputProps {
  icon: LucideIcon;
  label: string;
  type?: string;
  placeholder?: string;
  value: string;
  onChange: (v: string) => void;
  error?: string;
}

export function AuthInput({ icon: Icon, label, type = 'text', placeholder, value, onChange, error }: AuthInputProps) {
  return (
    <div>
      <label className="mb-1.5 block text-sm font-medium">{label}</label>
      <div className="relative">
        <Icon className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground/40" />
        <input
          type={type}
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className={cn(
            'h-12 w-full rounded-xl border border-border/50 bg-background pl-10 pr-4 text-sm transition-all duration-200',
            'placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10',
            error && 'border-destructive/50 focus:border-destructive/50 focus:ring-destructive/10',
          )}
        />
      </div>
      <AnimatePresence>
        {error && (
          <motion.p initial={{ opacity: 0, y: -4 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -4 }} className="mt-1 text-xs text-destructive">
            {error}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}
