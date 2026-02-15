import { useState } from 'react';
import { Lock, Eye, EyeOff } from 'lucide-react';
import { AnimatePresence, motion } from 'framer-motion';
import { cn } from '@/lib/utils';

interface PasswordInputProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (v: string) => void;
  error?: string;
}

export function PasswordInput({ label = 'Password', placeholder = 'Enter your password', value, onChange, error }: PasswordInputProps) {
  const [show, setShow] = useState(false);

  return (
    <div>
      <label className="mb-1.5 block text-sm font-medium">{label}</label>
      <div className="relative">
        <Lock className="absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground/40" />
        <input
          type={show ? 'text' : 'password'}
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className={cn(
            'h-12 w-full rounded-xl border border-border/50 bg-background pl-10 pr-11 text-sm transition-all duration-200',
            'placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10',
            error && 'border-destructive/50 focus:border-destructive/50 focus:ring-destructive/10',
          )}
        />
        <button type="button" onClick={() => setShow(!show)} className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/40 transition hover:text-muted-foreground">
          <AnimatePresence mode="wait">
            <motion.span key={show ? 'on' : 'off'} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.8 }} transition={{ duration: 0.12 }}>
              {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </motion.span>
          </AnimatePresence>
        </button>
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
