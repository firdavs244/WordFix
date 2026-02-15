import { ClipboardCheck, Gamepad2 } from 'lucide-react';
import QuickActionCard from './QuickActionCard';

export default function QuickActionsGrid() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <QuickActionCard
        title="Take a Test"
        description="AI-generated vocabulary assessments"
        icon={ClipboardCheck}
        href="/tests"
        gradient="from-secondary/10 to-cyan-500/5"
        iconColor="text-secondary"
      />
      <QuickActionCard
        title="Play a Game"
        description="Learn through 5 fun game modes"
        icon={Gamepad2}
        href="/games"
        gradient="from-primary/10 to-violet-500/5"
        iconColor="text-primary"
      />
    </div>
  );
}
