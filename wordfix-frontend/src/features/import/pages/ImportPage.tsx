import { Upload } from 'lucide-react';
import { PageTransition, PageHeader } from '@/components/shared';
import ImportTabs from '../components/ImportTabs';

export default function ImportPage() {
  return (
    <PageTransition>
      <div className="space-y-6">
        <PageHeader title="Smart Import" description="Import words from text or CSV files" icon={Upload} />
        <ImportTabs />
      </div>
    </PageTransition>
  );
}
