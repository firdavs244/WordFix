import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, ArrowRight, UserPlus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { useAuthStore } from '@/stores/useAuthStore';
import { toast } from 'sonner';
import type { AxiosError } from 'axios';
import type { ApiResponse } from '@/types';
import { RegisterAccountStep, RegisterPasswordStep, RegisterConfirmStep } from '../components/RegisterSteps';

const STEPS = ['Account', 'Personal', 'Confirm'] as const;

export function RegisterPage() {
  const navigate = useNavigate();
  const register = useAuthStore((s) => s.register);
  const googleLogin = useAuthStore((s) => s.googleLogin);
  const [step, setStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirm, setPasswordConfirm] = useState('');
  const [fullName, setFullName] = useState('');

  const canAdvance = () => {
    if (step === 0) return email.length > 0 && username.length >= 3;
    if (step === 1) return password.length >= 8 && password === passwordConfirm;
    return true;
  };

  const handleNext = () => {
    if (step === 0 && !email.includes('@')) {
      toast.error('Please enter a valid email.');
      return;
    }
    if (step === 0 && username.length < 3) {
      toast.error('Username must be at least 3 characters.');
      return;
    }
    if (step === 1 && password.length < 8) {
      toast.error('Password must be at least 8 characters.');
      return;
    }
    if (step === 1 && !/\d/.test(password)) {
      toast.error('Password must contain at least one digit.');
      return;
    }
    if (step === 1 && password !== passwordConfirm) {
      toast.error('Passwords do not match.');
      return;
    }
    setStep((s) => Math.min(s + 1, 2));
  };

  const handleGoogleSuccess = async (credential: string) => {
    setIsGoogleLoading(true);
    try {
      const { has_completed_onboarding } = await googleLogin(credential);
      navigate(has_completed_onboarding ? '/' : '/onboarding', { replace: true });
    } catch (err) {
      const axiosErr = err as AxiosError<ApiResponse>;
      toast.error(axiosErr.response?.data?.message || 'Google sign-up failed.');
    } finally {
      setIsGoogleLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await register({
        email,
        username,
        password,
        password_confirm: passwordConfirm,
        full_name: fullName || undefined,
      });
      navigate('/onboarding', { replace: true });
    } catch (err) {
      const axiosErr = err as AxiosError<ApiResponse>;
      const msg = axiosErr.response?.data?.message || 'Registration failed.';
      const errors = axiosErr.response?.data?.errors;
      if (errors) {
        const firstKey = Object.keys(errors)[0];
        toast.error(firstKey ? errors[firstKey][0] : msg);
      } else {
        toast.error(msg);
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <Card className="border-border/50 shadow-xl">
        <CardHeader className="text-center">
          <CardTitle className="font-heading text-2xl">Create Account</CardTitle>
          <CardDescription>
            Step {step + 1} of {STEPS.length}: {STEPS[step]}
          </CardDescription>
          <div className="mt-4 flex justify-center gap-2">
            {STEPS.map((_, i) => (
              <div
                key={i}
                className={`h-2 w-10 rounded-full transition-colors ${
                  i <= step ? 'bg-primary' : 'bg-muted'
                }`}
              />
            ))}
          </div>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="min-h-[200px]">
            <AnimatePresence mode="wait">
              {step === 0 && (
                <RegisterAccountStep
                  email={email}
                  username={username}
                  onEmailChange={setEmail}
                  onUsernameChange={setUsername}
                  isSubmitting={isSubmitting}
                  isGoogleLoading={isGoogleLoading}
                  onGoogleSuccess={handleGoogleSuccess}
                  onGoogleError={() => toast.error('Google sign-in was cancelled or failed.')}
                />
              )}
              {step === 1 && (
                <RegisterPasswordStep
                  password={password}
                  passwordConfirm={passwordConfirm}
                  showPassword={showPassword}
                  onPasswordChange={setPassword}
                  onPasswordConfirmChange={setPasswordConfirm}
                  onToggleShowPassword={() => setShowPassword(!showPassword)}
                />
              )}
              {step === 2 && (
                <RegisterConfirmStep
                  email={email}
                  username={username}
                  fullName={fullName}
                  onFullNameChange={setFullName}
                />
              )}
            </AnimatePresence>
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <div className="flex w-full gap-2">
              {step > 0 && (
                <Button
                  type="button"
                  variant="outline"
                  className="flex-1 gap-2"
                  onClick={() => setStep((s) => s - 1)}
                >
                  <ArrowLeft className="h-4 w-4" />
                  Back
                </Button>
              )}
              {step < 2 ? (
                <Button
                  type="button"
                  className="flex-1 gap-2"
                  onClick={handleNext}
                  disabled={!canAdvance()}
                >
                  Next
                  <ArrowRight className="h-4 w-4" />
                </Button>
              ) : (
                <Button type="submit" className="flex-1 gap-2" disabled={isSubmitting}>
                  {isSubmitting ? (
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
                  ) : (
                    <UserPlus className="h-4 w-4" />
                  )}
                  {isSubmitting ? 'Creating...' : 'Create Account'}
                </Button>
              )}
            </div>
            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{' '}
              <Link to="/login" className="font-medium text-primary hover:underline">
                Sign In
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </motion.div>
  );
}
