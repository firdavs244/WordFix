import {
  useLearningProfile as useLearningProfileQuery,
  useAnalyzeProfile,
  useMistakePatterns,
  useWordRecommendations,
  useDomainCoverage,
  useAcceptRecommendation,
} from './useLearning';

export function useLearningProfileData() {
  const { data: profileData, isLoading: profileLoading } =
    useLearningProfileQuery();
  const analyze = useAnalyzeProfile();
  const { data: mistakesData, isLoading: mistakesLoading } =
    useMistakePatterns();
  const { data: recsData, isLoading: recsLoading } =
    useWordRecommendations();
  const { data: coverageData, isLoading: coverageLoading } =
    useDomainCoverage();
  const acceptRec = useAcceptRecommendation();

  return {
    profile: profileData?.data ?? null,
    profileLoading,
    hasAnalyzed: !!profileData?.data?.last_analyzed,
    mistakes: mistakesData?.data ?? [],
    mistakesLoading,
    recommendations: recsData?.data ?? [],
    recsLoading,
    coverage: coverageData?.data ?? null,
    coverageLoading,
    analyze: analyze.mutate,
    analyzeIsPending: analyze.isPending,
    acceptRecommendation: acceptRec.mutate,
    acceptIsPending: acceptRec.isPending,
  };
}
