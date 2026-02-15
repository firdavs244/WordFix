import { Shield } from 'lucide-react';

export function SocialProofBadge() {
  return (
    <div className="mt-8 flex items-center justify-center gap-2">
      <Shield className="h-3 w-3 text-success/50" />
      <span className="text-[10px] text-muted-foreground/40">
        256-bit encrypted · Trusted by 500+ learners
      </span>
    </div>
  );
}
