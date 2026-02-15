import { ClipboardCheck, Sparkles } from 'lucide-react';
import PageTransition from '@/components/shared/PageTransition';
import PageHeader from '@/components/shared/PageHeader';
import TestConfigPanel from './components/TestConfigPanel';
import RecentTestsList from './components/RecentTestsList';

export default function TestPage() {
  return (
    <PageTransition>
      <div className="space-y-8">
        <PageHeader
          title="AI Test Generator"
          description="Generate personalized vocabulary tests"
          icon={ClipboardCheck}
          action={
            <span className="flex items-center gap-1 text-xs text-primary">
              <Sparkles className="h-3.5 w-3.5" /> AI-Powered
            </span>
          }
        />
        <TestConfigPanel />
        <RecentTestsList />
      </div>
    </PageTransition>
  );
}
