import { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Loader2 } from 'lucide-react';
import { bounceIn } from '@/lib/motion';
import { useClaimBonus } from '@/features/challenges/hooks/useChallenges';
import ChallengeBonusModal from './ChallengeBonusModal';
import GlowingBorder from './GlowingBorder';

interface Props {
  allCompleted: boolean;
  bonusClaimed: boolean;
}

export default function ChallengeBonusButton({ allCompleted, bonusClaimed }: Props) {
  const [showModal, setShowModal] = useState(false);
  const claimBonus = useClaimBonus();

  if (!allCompleted) return null;

  if (bonusClaimed) {
    return (
      <div className="flex items-center justify-center gap-2 rounded-xl bg-success/[0.04] px-4 py-2.5">
        <Sparkles className="h-4 w-4 text-success" />
        <span className="text-sm font-medium text-success">Bonus Claimed! +50 XP</span>
      </div>
    );
  }

  const handleClaim = async () => {
    await claimBonus.mutateAsync();
    setShowModal(true);
  };

  return (
    <>
      <GlowingBorder color="accent" active>
        <motion.button
          variants={bounceIn}
          initial="initial"
          animate="animate"
          whileHover={{ scale: 1.01 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleClaim}
          disabled={claimBonus.isPending}
          className="w-full rounded-2xl bg-gradient-to-r from-accent via-amber-400 to-orange-400 py-3 font-semibold text-white shadow-lg transition-shadow hover:shadow-xl disabled:opacity-70"
        >
          {claimBonus.isPending ? (
            <Loader2 className="mx-auto h-5 w-5 animate-spin" />
          ) : (
            <span>Claim Bonus +50 XP ⭐</span>
          )}
        </motion.button>
      </GlowingBorder>
      <ChallengeBonusModal open={showModal} onClose={() => setShowModal(false)} />
    </>
  );
}
