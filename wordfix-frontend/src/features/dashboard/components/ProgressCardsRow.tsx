import { motion } from 'framer-motion';
import { staggerContainer } from '@/lib/motion';
import MouseTiltCard from './MouseTiltCard';
import LevelCard from './LevelCard';
import StreakCard from './StreakCard';
import DailyProgressCard from './DailyProgressCard';

export default function ProgressCardsRow() {
  return (
    <motion.div
      variants={staggerContainer}
      initial="initial"
      animate="animate"
      className="grid grid-cols-1 md:grid-cols-3 gap-4 lg:gap-6"
    >
      <MouseTiltCard tiltAmount={3} glare>
        <LevelCard />
      </MouseTiltCard>
      <MouseTiltCard tiltAmount={3} glare>
        <StreakCard />
      </MouseTiltCard>
      <MouseTiltCard tiltAmount={3} glare>
        <DailyProgressCard />
      </MouseTiltCard>
    </motion.div>
  );
}
