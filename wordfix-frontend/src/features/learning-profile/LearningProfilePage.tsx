import { motion } from 'framer-motion';
import { pageTransition, staggerContainer } from '@/lib/motion';
import { useLearningProfileData } from './hooks/useLearningProfile';
import { LearningProfileHeader } from './components/LearningProfileHeader';
import { LearningStyleCard } from './components/LearningStyleCard';
import { OptimalTimeCard } from './components/OptimalTimeCard';
import { SkillsCard } from './components/SkillsCard';
import { LearningRecommendations } from './components/LearningRecommendations';
import { LearningMistakes } from './components/LearningMistakes';

export function LearningProfilePage() {
  const {
    profile,
    profileLoading,
    hasAnalyzed,
    mistakes,
    mistakesLoading,
    recommendations,
    recsLoading,
    analyze,
    analyzeIsPending,
    acceptRecommendation,
    acceptIsPending,
  } = useLearningProfileData();

  return (
    <motion.div
      {...pageTransition}
      className="mx-auto max-w-5xl"
    >
      <motion.div
        variants={staggerContainer}
        initial="initial"
        animate="animate"
        className="space-y-8"
      >
        <LearningProfileHeader
          hasAnalyzed={hasAnalyzed}
          lastAnalyzed={profile?.last_analyzed ?? null}
          onAnalyze={() => analyze()}
          isPending={analyzeIsPending}
        />

        <LearningStyleCard
          profile={profile}
          isLoading={profileLoading}
          hasAnalyzed={hasAnalyzed}
        />

        <div className="grid gap-6 md:grid-cols-2">
          <OptimalTimeCard
            profile={profile}
            isLoading={profileLoading}
            hasAnalyzed={hasAnalyzed}
          />
          <SkillsCard
            profile={profile}
            isLoading={profileLoading}
            hasAnalyzed={hasAnalyzed}
          />
        </div>

        <LearningRecommendations
          recommendations={recommendations}
          isLoading={recsLoading}
          onAccept={(id) => acceptRecommendation(id)}
          isPending={acceptIsPending}
        />

        <LearningMistakes
          mistakes={mistakes}
          isLoading={mistakesLoading}
        />
      </motion.div>
    </motion.div>
  );
}

export default LearningProfilePage;
