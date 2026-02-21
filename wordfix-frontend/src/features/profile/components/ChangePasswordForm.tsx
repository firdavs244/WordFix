import { useState } from 'react';
import { Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { PasswordInput } from '@/features/auth/components/PasswordInput';
import { PasswordStrengthBar } from '@/features/auth/components/PasswordStrengthBar';
import { useChangePassword } from '../hooks/useProfile';

export default function ChangePasswordForm() {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<string[]>([]);
  const changePassword = useChangePassword();

  const validate = () => {
    const errs: string[] = [];
    if (newPassword.length < 8) errs.push('Password must be at least 8 characters');
    if (!/\d/.test(newPassword)) errs.push('Password must contain a number');
    if (newPassword !== confirmPassword) errs.push('Passwords do not match');
    setErrors(errs);
    return errs.length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    changePassword.mutate(
      { old_password: currentPassword, new_password: newPassword, new_password_confirm: confirmPassword },
      { onSuccess: () => { setCurrentPassword(''); setNewPassword(''); setConfirmPassword(''); setErrors([]); } },
    );
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 mt-4">
      <PasswordInput label="Current Password" placeholder="Enter current password" value={currentPassword} onChange={setCurrentPassword} />
      <div>
        <PasswordInput label="New Password" placeholder="Enter new password" value={newPassword} onChange={setNewPassword} />
        <PasswordStrengthBar password={newPassword} />
      </div>
      <PasswordInput label="Confirm New Password" placeholder="Confirm new password" value={confirmPassword} onChange={setConfirmPassword} />
      {errors.length > 0 && (
        <div className="space-y-1">
          {errors.map((err) => (
            <p key={err} className="text-xs text-destructive">{err}</p>
          ))}
        </div>
      )}
      <Button type="submit" className="h-10 w-full" disabled={changePassword.isPending}>
        {changePassword.isPending ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Changing...</> : 'Change Password'}
      </Button>
    </form>
  );
}
