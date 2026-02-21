import { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, FileSpreadsheet } from 'lucide-react';
import { cn } from '@/lib/utils';
import TextImportFlow from './TextImportFlow';
import CSVImportFlow from './CSVImportFlow';

const TABS = [
  { id: 'text', label: 'From Text', icon: FileText },
  { id: 'csv', label: 'From CSV', icon: FileSpreadsheet },
] as const;

export default function ImportTabs() {
  const [active, setActive] = useState<'text' | 'csv'>('text');

  return (
    <div>
      <div className="mb-6 inline-flex rounded-xl bg-muted/50 p-1">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActive(tab.id)}
            className={cn(
              'relative flex items-center gap-1.5 rounded-lg px-5 py-2 text-sm font-medium transition-all',
              active === tab.id ? 'text-foreground' : 'text-muted-foreground hover:text-foreground/70',
            )}
          >
            {active === tab.id && (
              <motion.div layoutId="import-tab-indicator" className="absolute inset-0 rounded-lg bg-card shadow-sm" />
            )}
            <span className="relative z-10 flex items-center gap-1.5">
              <tab.icon className="h-3.5 w-3.5" />
              {tab.label}
            </span>
          </button>
        ))}
      </div>
      {active === 'text' ? <TextImportFlow /> : <CSVImportFlow />}
    </div>
  );
}
