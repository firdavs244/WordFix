import { GraduationCap, RefreshCw } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '@/stores/useAuthStore';

export default function LearningLevelCard() {
  const user = useAuthStore((s) => s.user);
  if (!user) return null;

  return (
    <div className="rounded-2xl shadow-card border border-border/50 p-6 bg-card">
      <div className="flex items-center gap-2">
        <GraduationCap className="h-[18px] w-[18px] text-muted-foreground" />
        <h3 className="text-base font-heading font-semibold">Learning Level</h3>
      </div>
      <div className="mt-4 flex items-center gap-3">
        <span className="text-lg font-bold px-3 py-1.5 rounded-xl bg-primary/10 text-primary">
          {user.proficiency_level}
        </span>
        <p className="text-sm text-muted-foreground">Current proficiency level</p>
      </div>
      <Link
        to="/onboarding"
        className="inline-flex items-center gap-1 mt-4 text-sm text-primary font-medium hover:underline"
      >
        <RefreshCw className="h-3.5 w-3.5" />
        Retake Assessment
      </Link>
    </div>
  );
}
