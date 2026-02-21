import { Lock } from 'lucide-react';
import ChangePasswordForm from './ChangePasswordForm';

export default function ChangePasswordCard() {
  return (
    <div className="rounded-2xl shadow-card border border-border/50 p-6 bg-card">
      <div className="flex items-center gap-2">
        <Lock className="h-[18px] w-[18px] text-muted-foreground" />
        <h3 className="text-base font-heading font-semibold">Security</h3>
      </div>
      <ChangePasswordForm />
    </div>
  );
}
