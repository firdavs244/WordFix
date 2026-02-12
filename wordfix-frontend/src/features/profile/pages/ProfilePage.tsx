import { useState } from 'react';
import { Link } from 'react-router-dom';
import { User as UserIcon, Mail, Globe, Target, Shield, Save, Lock, GraduationCap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { PageTransition } from '@/components/animations/PageTransition';
import { useAuthStore } from '@/stores/useAuthStore';
import { authApi } from '@/features/auth/api/authApi';
import type { ProficiencyLevel, UpdateProfileData, ChangePasswordData } from '@/types';
import { toast } from 'sonner';

const proficiencyLevels: ProficiencyLevel[] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

export function ProfilePage() {
  const user = useAuthStore((s) => s.user);
  const setUser = useAuthStore((s) => s.setUser);
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [showChangePassword, setShowChangePassword] = useState(false);

  // Edit form state
  const [fullName, setFullName] = useState(user?.full_name ?? '');
  const [dailyGoal, setDailyGoal] = useState(user?.daily_goal ?? 10);
  const [proficiency, setProficiency] = useState<ProficiencyLevel>(user?.proficiency_level ?? 'A1');
  const [timezone, setTimezone] = useState(user?.timezone ?? 'UTC');

  // Password form state
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newPasswordConfirm, setNewPasswordConfirm] = useState('');
  const [isChangingPassword, setIsChangingPassword] = useState(false);

  if (!user) return null;

  const handleSaveProfile = async () => {
    setIsSaving(true);
    try {
      const data: UpdateProfileData = {
        full_name: fullName,
        daily_goal: dailyGoal,
        proficiency_level: proficiency,
        timezone,
      };
      const response = await authApi.updateProfile(data);
      setUser(response.data);
      setIsEditing(false);
      toast.success('Profile updated!');
    } catch {
      toast.error('Failed to update profile.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== newPasswordConfirm) {
      toast.error('Passwords do not match.');
      return;
    }
    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters.');
      return;
    }
    setIsChangingPassword(true);
    try {
      const data: ChangePasswordData = {
        old_password: oldPassword,
        new_password: newPassword,
        new_password_confirm: newPasswordConfirm,
      };
      await authApi.changePassword(data);
      toast.success('Password changed successfully!');
      setShowChangePassword(false);
      setOldPassword('');
      setNewPassword('');
      setNewPasswordConfirm('');
    } catch {
      toast.error('Failed to change password. Check your old password.');
    } finally {
      setIsChangingPassword(false);
    }
  };

  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-6">
        <h1 className="font-heading text-3xl font-bold">Profile</h1>

        {/* User Info Card */}
        <Card className="border-border/50">
          <CardHeader className="flex flex-row items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary text-2xl font-bold text-white">
              {user.username[0].toUpperCase()}
            </div>
            <div className="flex-1">
              <CardTitle className="text-xl">{user.full_name || user.username}</CardTitle>
              <p className="text-sm text-muted-foreground">{user.email}</p>
              <div className="flex items-center gap-2 mt-1">
                <Badge variant="outline">{user.proficiency_level}</Badge>
                {user.is_premium_active && <Badge variant="default">Premium</Badge>}
              </div>
            </div>
            <Button
              variant={isEditing ? 'default' : 'outline'}
              size="sm"
              onClick={() => setIsEditing(!isEditing)}
            >
              {isEditing ? 'Cancel' : 'Edit'}
            </Button>
          </CardHeader>
          <CardContent className="space-y-4">
            {isEditing ? (
              <>
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-2">
                    <UserIcon className="h-4 w-4" /> Full Name
                  </label>
                  <Input value={fullName} onChange={(e) => setFullName(e.target.value)} />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-2">
                    <Target className="h-4 w-4" /> Daily Goal
                  </label>
                  <Input
                    type="number"
                    min={1}
                    max={100}
                    value={dailyGoal}
                    onChange={(e) => setDailyGoal(Number(e.target.value))}
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-2">
                    <Shield className="h-4 w-4" /> Proficiency Level
                  </label>
                  <div className="flex gap-2 flex-wrap">
                    {proficiencyLevels.map((level) => (
                      <Button
                        key={level}
                        type="button"
                        variant={proficiency === level ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setProficiency(level)}
                      >
                        {level}
                      </Button>
                    ))}
                  </div>
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium flex items-center gap-2">
                    <Globe className="h-4 w-4" /> Timezone
                  </label>
                  <Input value={timezone} onChange={(e) => setTimezone(e.target.value)} />
                </div>
                <Button onClick={handleSaveProfile} disabled={isSaving} className="gap-2">
                  {isSaving ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  ) : (
                    <Save className="h-4 w-4" />
                  )}
                  Save Changes
                </Button>
              </>
            ) : (
              <div className="space-y-3">
                <InfoRow icon={<Mail className="h-4 w-4" />} label="Email" value={user.email} />
                <InfoRow icon={<UserIcon className="h-4 w-4" />} label="Username" value={user.username} />
                <InfoRow icon={<UserIcon className="h-4 w-4" />} label="Full Name" value={user.full_name || '—'} />
                <InfoRow icon={<Target className="h-4 w-4" />} label="Daily Goal" value={`${user.daily_goal} words/day`} />
                <InfoRow icon={<Shield className="h-4 w-4" />} label="Level" value={user.proficiency_level} />
                <InfoRow icon={<Globe className="h-4 w-4" />} label="Timezone" value={user.timezone} />
                <InfoRow
                  icon={<Globe className="h-4 w-4" />}
                  label="Joined"
                  value={new Date(user.date_joined).toLocaleDateString()}
                />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Change Password Card */}
        <Card className="border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <Lock className="h-5 w-5" />
              Password
            </CardTitle>
          </CardHeader>
          <CardContent>
            {showChangePassword ? (
              <form onSubmit={handleChangePassword} className="space-y-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Current Password</label>
                  <Input
                    type="password"
                    value={oldPassword}
                    onChange={(e) => setOldPassword(e.target.value)}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">New Password</label>
                  <Input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    minLength={8}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium">Confirm New Password</label>
                  <Input
                    type="password"
                    value={newPasswordConfirm}
                    onChange={(e) => setNewPasswordConfirm(e.target.value)}
                    required
                  />
                </div>
                <div className="flex gap-2">
                  <Button type="submit" disabled={isChangingPassword} className="gap-2">
                    {isChangingPassword ? (
                      <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                    ) : (
                      <Save className="h-4 w-4" />
                    )}
                    Change Password
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setShowChangePassword(false)}>
                    Cancel
                  </Button>
                </div>
              </form>
            ) : (
              <Button variant="outline" onClick={() => setShowChangePassword(true)}>
                Change Password
              </Button>
            )}
          </CardContent>
        </Card>

        {/* Learning Level Card */}
        <Card className="border-border/50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-lg">
              <GraduationCap className="h-5 w-5" />
              Learning Level
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-sm font-bold text-primary ring-2 ring-primary/30">
                {user.proficiency_level}
              </div>
              <div>
                <p className="font-medium">Current Level: {user.proficiency_level}</p>
                <p className="text-sm text-muted-foreground">
                  {user.has_completed_onboarding
                    ? 'Determined by your level test'
                    : 'Default level — take the test to update'}
                </p>
              </div>
            </div>
            <Button variant="outline" asChild>
              <Link to="/onboarding">
                <GraduationCap className="mr-2 h-4 w-4" />
                Retake Level Test
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </PageTransition>
  );
}

function InfoRow({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <div className="flex items-center gap-3 text-sm">
      <span className="text-muted-foreground">{icon}</span>
      <span className="text-muted-foreground w-24">{label}:</span>
      <span className="font-medium">{value}</span>
    </div>
  );
}
