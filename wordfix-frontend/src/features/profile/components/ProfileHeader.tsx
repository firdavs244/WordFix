import { useAuthStore } from '@/stores/useAuthStore';
import ProfileAvatar from './ProfileAvatar';

export default function ProfileHeader() {
  const user = useAuthStore((s) => s.user);
  if (!user) return null;

  return (
    <div className="rounded-2xl shadow-card border border-border/50 overflow-hidden bg-card">
      <div className="h-24 bg-gradient-to-r from-primary/20 via-secondary/10 to-accent/10" />
      <div className="px-6 pb-6">
        <div className="-mt-10 relative">
          <ProfileAvatar name={user.full_name || user.username} size="lg" />
        </div>
        <h2 className="text-xl font-heading font-bold mt-3">{user.full_name || user.username}</h2>
        <p className="text-sm text-muted-foreground">{user.email}</p>
        <div className="flex gap-2 mt-2">
          <span className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-primary/10 text-primary">
            {user.proficiency_level}
          </span>
        </div>
      </div>
    </div>
  );
}
