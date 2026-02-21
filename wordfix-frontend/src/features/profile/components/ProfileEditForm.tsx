import { useState } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuthStore } from '@/stores/useAuthStore';
import { useUpdateProfile } from '../hooks/useProfile';
import ProfileDailyGoalSlider from './ProfileDailyGoalSlider';
import ProficiencyLevelSelector from './ProficiencyLevelSelector';
import type { ProficiencyLevel } from '@/types';

interface ProfileEditFormProps {
  onCancel: () => void;
}

export default function ProfileEditForm({ onCancel }: ProfileEditFormProps) {
  const user = useAuthStore((s) => s.user);
  const updateProfile = useUpdateProfile();

  const [fullName, setFullName] = useState(user?.full_name || '');
  const [dailyGoal, setDailyGoal] = useState(user?.daily_goal || 10);
  const [proficiencyLevel, setProficiencyLevel] = useState<ProficiencyLevel>(
    (user?.proficiency_level as ProficiencyLevel) || 'B1',
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    updateProfile.mutate(
      { full_name: fullName, daily_goal: dailyGoal, proficiency_level: proficiencyLevel },
      { onSuccess: () => onCancel() },
    );
  };

  const handleCancel = () => {
    setFullName(user?.full_name || '');
    setDailyGoal(user?.daily_goal || 10);
    setProficiencyLevel((user?.proficiency_level as ProficiencyLevel) || 'B1');
    onCancel();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 mt-4">
      <div>
        <label className="text-sm font-medium">Full Name</label>
        <input
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          className="mt-1 w-full rounded-lg border border-border bg-background px-3 py-2 text-sm"
          placeholder="Your full name"
        />
      </div>
      <ProfileDailyGoalSlider value={dailyGoal} onChange={setDailyGoal} />
      <ProficiencyLevelSelector value={proficiencyLevel} onChange={setProficiencyLevel} />
      <div className="flex gap-3 mt-4">
        <Button type="button" variant="outline" className="h-10" onClick={handleCancel}>
          Cancel
        </Button>
        <Button type="submit" className="h-10" disabled={updateProfile.isPending}>
          {updateProfile.isPending ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Saving...</> : 'Save Changes'}
        </Button>
      </div>
    </form>
  );
}
