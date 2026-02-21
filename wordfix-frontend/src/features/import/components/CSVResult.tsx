import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { Link } from 'react-router-dom';
import { bounceIn } from '@/lib/motion';
import { cn } from '@/lib/utils';
import type { CSVImportResult as ResultType } from '@/types';

interface CSVResultProps {
  result: ResultType;
  onImportMore: () => void;
}

export default function CSVResult({ result, onImportMore }: CSVResultProps) {
  const stats = [
    { label: 'Imported', value: result.imported, color: 'text-success' },
    { label: 'Duplicates', value: result.skipped_duplicate, color: 'text-warning' },
    { label: 'Invalid', value: result.skipped_invalid, color: 'text-destructive' },
  ];

  return (
    <div className="py-8 text-center">
      <motion.div variants={bounceIn} initial="initial" animate="animate" className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-success/10">
        <Check className="h-7 w-7 text-success" />
      </motion.div>
      <h3 className="mt-4 font-heading text-lg font-bold">Import Complete!</h3>
      <div className="mt-4 flex justify-center gap-6">
        {stats.map((s) => (
          <div key={s.label} className="text-center">
            <p className={cn('text-xl font-heading font-bold', s.color)}>{s.value}</p>
            <p className="text-[10px] text-muted-foreground">{s.label}</p>
          </div>
        ))}
      </div>
      <div className="mt-6 flex justify-center gap-3">
        <Link to="/words" className="flex h-10 items-center rounded-xl border border-border px-6 text-sm font-medium hover:bg-muted">View Words</Link>
        <button onClick={onImportMore} className="flex h-10 items-center rounded-xl bg-primary px-6 text-sm font-medium text-white">Import More</button>
      </div>
    </div>
  );
}
