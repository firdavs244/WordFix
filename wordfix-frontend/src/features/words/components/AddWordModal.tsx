import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { X } from 'lucide-react';
import { fadeIn, scaleIn } from '@/lib/motion';
import AddWordForm from './AddWordForm';

interface Props {
  onClose: () => void;
}

export default function AddWordModal({ onClose }: Props) {
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handler);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handler);
      document.body.style.overflow = '';
    };
  }, [onClose]);

  return (
    <motion.div
      variants={fadeIn}
      initial="initial"
      animate="animate"
      exit="exit"
      className="fixed inset-0 z-50 flex items-start justify-center bg-black/60 backdrop-blur-md"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-label="Add New Word"
    >
      <motion.div
        variants={scaleIn}
        initial="initial"
        animate="animate"
        exit="exit"
        className="mt-[10vh] w-full max-w-lg rounded-3xl border border-border/30 bg-card shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-6 pt-6">
          <h2 className="font-heading text-lg font-semibold">Add New Word</h2>
          <button onClick={onClose} className="flex h-8 w-8 items-center justify-center rounded-lg transition-colors hover:bg-muted" aria-label="Close">
            <X className="h-4 w-4" />
          </button>
        </div>
        <AddWordForm onSuccess={onClose} />
      </motion.div>
    </motion.div>
  );
}
