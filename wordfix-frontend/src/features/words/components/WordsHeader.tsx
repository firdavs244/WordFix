import { useState } from 'react';
import { BookOpen, Plus } from 'lucide-react';
import { PageHeader } from '@/components/shared';
import { useWordStats } from '../hooks/useWords';
import AddWordModal from './AddWordModal';

export default function WordsHeader() {
  const [showModal, setShowModal] = useState(false);
  const { data } = useWordStats();
  const total = data?.data?.total ?? 0;

  return (
    <>
      <PageHeader
        title="Word Bank"
        icon={BookOpen}
        action={
          <div className="flex items-center gap-3">
            <span className="rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium">
              {total} words
            </span>
            <button
              onClick={() => setShowModal(true)}
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-all hover:scale-[1.02] hover:shadow-glow-primary"
            >
              <Plus className="h-4 w-4" />
              Add Word
            </button>
          </div>
        }
      />
      {showModal && <AddWordModal onClose={() => setShowModal(false)} />}
    </>
  );
}
