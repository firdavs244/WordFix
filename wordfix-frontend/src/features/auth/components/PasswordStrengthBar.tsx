import { motion } from 'framer-motion';

const labels = ['', 'Weak', 'Fair', 'Good', 'Strong'] as const;
const colors = ['', 'bg-destructive', 'bg-warning', 'bg-accent', 'bg-success'] as const;
const textColors = ['', 'text-destructive', 'text-warning', 'text-accent', 'text-success'] as const;

function getStrength(password: string): number {
  let s = 0;
  if (password.length >= 8) s++;
  if (/\d/.test(password)) s++;
  if (/[A-Z]/.test(password)) s++;
  if (/[^a-zA-Z0-9]/.test(password)) s++;
  return s;
}

export function PasswordStrengthBar({ password }: { password: string }) {
  const strength = getStrength(password);
  if (!password) return null;

  return (
    <div className="mt-2">
      <div className="flex h-1.5 gap-1 overflow-hidden rounded-full">
        {[1, 2, 3, 4].map((i) => (
          <motion.div
            key={i}
            className={`h-full flex-1 rounded-full ${i <= strength ? colors[strength] : 'bg-muted'}`}
            initial={{ scaleX: 0 }}
            animate={{ scaleX: i <= strength ? 1 : 0 }}
            transition={{ duration: 0.3, delay: i * 0.05 }}
            style={{ originX: 0 }}
          />
        ))}
      </div>
      {strength > 0 && (
        <p className={`mt-1 text-[10px] font-medium ${textColors[strength]}`}>{labels[strength]}</p>
      )}
    </div>
  );
}
