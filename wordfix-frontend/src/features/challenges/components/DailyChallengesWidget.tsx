import { useState } from 'react';
import { motion } from 'framer-motion';
import { ClipboardList, Gift, Sparkles } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { ChallengeCard } from './ChallengeCard';
import { ChallengeBonusModal } from './ChallengeBonusModal';
import { useDailyChallenges, useClaimBonus } from '../hooks/useChallenges';

interface DailyChallengesWidgetProps {
  compact?: boolean;
}

export function DailyChallengesWidget({ compact = false }: DailyChallengesWidgetProps) {
  const { data, isLoading } = useDailyChallenges();
  const claimBonus = useClaimBonus();
  const [showBonusModal, setShowBonusModal] = useState(false);

  const challenges = data?.data;
  const completedCount = challenges?.challenges.filter((c) => c.completed).length ?? 0;
  const totalCount = challenges?.challenges.length ?? 3;

  if (isLoading) {
    return compact ? (
      <Skeleton className="h-8 w-20" />
    ) : (
      <Card className="border-border/50">
        <CardContent className="p-4">
          <Skeleton className="h-24 w-full" />
        </CardContent>
      </Card>
    );
  }

  if (!challenges) return null;

  const handleClaimBonus = () => {
    claimBonus.mutate(undefined, {
      onSuccess: () => {
        setShowBonusModal(true);
      },
    });
  };

  // Compact version for sidebar
  if (compact) {
    return (
      <div className="flex items-center gap-2 rounded-lg bg-muted/50 px-3 py-2">
        <ClipboardList className="h-4 w-4 text-primary" />
        <div className="flex items-center gap-1">
          <span className="text-sm font-bold">{completedCount}/{totalCount}</span>
          {challenges.all_completed && challenges.bonus_claimed && (
            <Sparkles className="h-3.5 w-3.5 text-amber-500" />
          )}
        </div>
      </div>
    );
  }

  // Full version for dashboard
  return (
    <>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <Card className={`border-border/50 ${challenges.all_completed && challenges.bonus_claimed ? 'border-green-500/30' : ''}`}>
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center gap-2 text-lg">
                <ClipboardList className="h-5 w-5 text-primary" />
                Daily Challenges
              </CardTitle>
              <span className="text-sm font-medium text-muted-foreground">
                {completedCount}/{totalCount} Done
              </span>
            </div>
          </CardHeader>
          <CardContent className="space-y-2">
            {challenges.challenges.map((challenge, i) => (
              <ChallengeCard key={`${challenge.type}-${i}`} challenge={challenge} />
            ))}

            {/* Bonus section */}
            <div className="mt-3 pt-3 border-t border-border/50">
              {challenges.all_completed && challenges.bonus_claimed ? (
                <motion.div
                  className="flex items-center justify-center gap-2 rounded-lg bg-green-500/10 p-3"
                  initial={{ scale: 0.95 }}
                  animate={{ scale: 1 }}
                >
                  <Sparkles className="h-5 w-5 text-green-500" />
                  <span className="text-sm font-medium text-green-600 dark:text-green-400">
                    🎉 All Done! +50 XP Bonus Claimed!
                  </span>
                </motion.div>
              ) : challenges.all_completed && !challenges.bonus_claimed ? (
                <motion.div
                  animate={{ boxShadow: ['0 0 0 0 rgba(59,130,246,0)', '0 0 15px 3px rgba(59,130,246,0.3)', '0 0 0 0 rgba(59,130,246,0)'] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <Button
                    onClick={handleClaimBonus}
                    className="w-full gap-2"
                    size="lg"
                    disabled={claimBonus.isPending}
                  >
                    <Gift className="h-5 w-5" />
                    Claim Bonus +50 XP ⭐
                  </Button>
                </motion.div>
              ) : (
                <p className="text-center text-xs text-muted-foreground">
                  ⭐ Complete all {totalCount} for +50 XP bonus!
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </motion.div>

      <ChallengeBonusModal
        isOpen={showBonusModal}
        onClose={() => setShowBonusModal(false)}
      />
    </>
  );
}
