import { motion } from 'framer-motion';
import { Eye, EyeOff } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { GoogleLoginButton } from '@/features/auth/components/GoogleLoginButton';

// ─── Step 0: Account ───────────────────────────────────────────────────────────

interface AccountStepProps {
  email: string;
  username: string;
  onEmailChange: (v: string) => void;
  onUsernameChange: (v: string) => void;
  isSubmitting: boolean;
  isGoogleLoading: boolean;
  onGoogleSuccess: (credential: string) => void;
  onGoogleError: () => void;
}

export function RegisterAccountStep({
  email,
  username,
  onEmailChange,
  onUsernameChange,
  isSubmitting,
  isGoogleLoading,
  onGoogleSuccess,
  onGoogleError,
}: AccountStepProps) {
  return (
    <motion.div
      key="step-0"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="space-y-4"
    >
      <GoogleLoginButton
        text="Sign up with Google"
        disabled={isSubmitting || isGoogleLoading}
        onSuccess={onGoogleSuccess}
        onError={onGoogleError}
      />

      <div className="relative flex items-center gap-3">
        <Separator className="flex-1" />
        <span className="text-xs text-muted-foreground">or use email</span>
        <Separator className="flex-1" />
      </div>

      <div className="space-y-2">
        <label htmlFor="email" className="text-sm font-medium">
          Email
        </label>
        <Input
          id="email"
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => onEmailChange(e.target.value)}
          autoComplete="email"
          required
        />
      </div>
      <div className="space-y-2">
        <label htmlFor="username" className="text-sm font-medium">
          Username
        </label>
        <Input
          id="username"
          type="text"
          placeholder="john_doe"
          value={username}
          onChange={(e) => onUsernameChange(e.target.value)}
          autoComplete="username"
          minLength={3}
          maxLength={30}
          required
        />
        <p className="text-xs text-muted-foreground">
          3-30 characters, letters, numbers, underscores, hyphens
        </p>
      </div>
    </motion.div>
  );
}

// ─── Step 1: Password ──────────────────────────────────────────────────────────

interface PasswordStepProps {
  password: string;
  passwordConfirm: string;
  showPassword: boolean;
  onPasswordChange: (v: string) => void;
  onPasswordConfirmChange: (v: string) => void;
  onToggleShowPassword: () => void;
}

export function RegisterPasswordStep({
  password,
  passwordConfirm,
  showPassword,
  onPasswordChange,
  onPasswordConfirmChange,
  onToggleShowPassword,
}: PasswordStepProps) {
  return (
    <motion.div
      key="step-1"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="space-y-4"
    >
      <div className="space-y-2">
        <label htmlFor="password" className="text-sm font-medium">
          Password
        </label>
        <div className="relative">
          <Input
            id="password"
            type={showPassword ? 'text' : 'password'}
            placeholder="••••••••"
            value={password}
            onChange={(e) => onPasswordChange(e.target.value)}
            autoComplete="new-password"
            minLength={8}
            required
          />
          <button
            type="button"
            onClick={onToggleShowPassword}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
            tabIndex={-1}
          >
            {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
        <p className="text-xs text-muted-foreground">At least 8 characters with one digit</p>
      </div>
      <div className="space-y-2">
        <label htmlFor="password_confirm" className="text-sm font-medium">
          Confirm Password
        </label>
        <Input
          id="password_confirm"
          type="password"
          placeholder="••••••••"
          value={passwordConfirm}
          onChange={(e) => onPasswordConfirmChange(e.target.value)}
          autoComplete="new-password"
          required
        />
      </div>
    </motion.div>
  );
}

// ─── Step 2: Confirm ───────────────────────────────────────────────────────────

interface ConfirmStepProps {
  email: string;
  username: string;
  fullName: string;
  onFullNameChange: (v: string) => void;
}

export function RegisterConfirmStep({
  email,
  username,
  fullName,
  onFullNameChange,
}: ConfirmStepProps) {
  return (
    <motion.div
      key="step-2"
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      className="space-y-4"
    >
      <div className="space-y-2">
        <label htmlFor="fullname" className="text-sm font-medium">
          Full Name <span className="text-muted-foreground">(optional)</span>
        </label>
        <Input
          id="fullname"
          type="text"
          placeholder="John Doe"
          value={fullName}
          onChange={(e) => onFullNameChange(e.target.value)}
        />
      </div>
      <div className="space-y-2 rounded-lg bg-muted/50 p-4 text-sm">
        <p className="font-medium">Review your details:</p>
        <p>
          <span className="text-muted-foreground">Email:</span> {email}
        </p>
        <p>
          <span className="text-muted-foreground">Username:</span> {username}
        </p>
        {fullName && (
          <p>
            <span className="text-muted-foreground">Name:</span> {fullName}
          </p>
        )}
      </div>
    </motion.div>
  );
}
