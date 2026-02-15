import { PageTransition } from '@/components/shared';
import WelcomeHeader from '../components/WelcomeHeader';
import ProgressCardsRow from '../components/ProgressCardsRow';
import DailyChallengesSection from '../components/DailyChallengesSection';
import XPChart from '../components/XPChart';
import ReviewCTABanner from '../components/ReviewCTABanner';
import QuickActionsGrid from '../components/QuickActionsGrid';
import DashboardStatsRow from '../components/DashboardStatsRow';
import AverageConfidenceBar from '../components/AverageConfidenceBar';
import RecentWordsList from '../components/RecentWordsList';
import DomainCoverageWidget from '../components/DomainCoverageWidget';
import RecommendationsWidget from '../components/RecommendationsWidget';
import MistakePatternsWidget from '../components/MistakePatternsWidget';

export function DashboardPage() {
  return (
    <PageTransition>
      <div className="space-y-8 lg:space-y-10">
        <WelcomeHeader />
        <ProgressCardsRow />
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-2">
            <DailyChallengesSection />
          </div>
          <XPChart />
        </div>
        <ReviewCTABanner />
        <QuickActionsGrid />
        <DashboardStatsRow />
        <AverageConfidenceBar />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <RecentWordsList />
          </div>
          <DomainCoverageWidget compact />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RecommendationsWidget />
          <MistakePatternsWidget />
        </div>
      </div>
    </PageTransition>
  );
}
