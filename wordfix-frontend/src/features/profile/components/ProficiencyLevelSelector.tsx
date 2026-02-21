import { motion } from 'framer-motion';
import type { ProficiencyLevel } from '@/types';

const LEVELS: ProficiencyLevel[] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

interface ProficiencyLevelSelectorProps {
  value: ProficiencyLevel;
  onChange: (level: ProficiencyLevel) => void;
}

export default function ProficiencyLevelSelector({ value, onChange }: ProficiencyLevelSelectorProps) {
  return (
    <div>
      <label className="text-sm font-medium mb-2 block">Proficiency Level</label>
      <div className="grid grid-cols-6 gap-1.5">
        {LEVELS.map((level) => (
          <button
            key={level}
            type="button"
            onClick={() => onChange(level)}
            className="relative h-10 rounded-lg text-xs font-bold"
          >
            {value === level && (
              <motion.div
                layoutId="proficiency-indicator"
                className="absolute inset-0 bg-primary rounded-lg shadow-sm"
                transition={{ type: 'spring', stiffness: 500, damping: 30 }}
              />
            )}
            <span
              className={`relative z-10 ${
                value === level
                  ? 'text-white'
                  : 'text-muted-foreground hover:text-foreground bg-muted/50 border border-border/30 rounded-lg h-full w-full flex items-center justify-center'
              }`}
            >
              {level}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}
