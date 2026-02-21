import { useState } from 'react';
import { motion } from 'framer-motion';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { ConfusingPairCard } from './ConfusingPairCard';
import type { ConfusingPair } from '../types';

interface ResolvedPairsSectionProps {
  pairs: ConfusingPair[];
  onDrill: (id: string) => void;
  onResolve: (id: string) => void;
}

export default function ResolvedPairsSection({ pairs, onDrill, onResolve }: ResolvedPairsSectionProps) {
  const [show, setShow] = useState(false);

  if (pairs.length === 0) return null;

  return (
    <div className="space-y-3">
      <Button
        variant="ghost"
        className="gap-2 text-muted-foreground"
        onClick={() => setShow(!show)}
      >
        {show ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
        Resolved Pairs ({pairs.length})
      </Button>
      {show && (
        <motion.div className="space-y-3" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          {pairs.map((pair) => (
            <ConfusingPairCard key={pair.id} pair={pair} onDrill={onDrill} onResolve={onResolve} />
          ))}
        </motion.div>
      )}
    </div>
  );
}
