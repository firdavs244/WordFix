import { motion } from 'framer-motion';
import { Check } from 'lucide-react';
import { Link } from 'react-router-dom';
import { bounceIn } from '@/lib/motion';

interface TextImportResultProps {
  importedCount: number;
  onImportMore: () => void;
}

export default function TextImportResult({ importedCount, onImportMore }: TextImportResultProps) {
  return (
    <div className="py-8 text-center">
      <motion.div variants={bounceIn} initial="initial" animate="animate" className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-success/10">
        <Check className="h-7 w-7 text-success" />
      </motion.div>
      <h3 className="mt-4 font-heading text-lg font-bold">Successfully Imported!</h3>
      <p className="mt-1 text-sm text-muted-foreground">{importedCount} words added to your Word Bank</p>
      <div className="mt-6 flex justify-center gap-3">
        <Link to="/words" className="flex h-10 items-center rounded-xl border border-border px-6 text-sm font-medium transition-colors hover:bg-muted">
          View Words
        </Link>
        <button onClick={onImportMore} className="flex h-10 items-center rounded-xl bg-primary px-6 text-sm font-medium text-white">
          Import More
        </button>
      </div>
    </div>
  );
}
