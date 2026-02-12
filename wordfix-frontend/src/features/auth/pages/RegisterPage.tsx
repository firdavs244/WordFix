import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { ArrowLeft, ArrowRight, Eye, EyeOff, UserPlus } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { useAuthStore } from '@/stores/useAuthStore';
import { GoogleLoginButton } from '@/features/auth/components/GoogleLoginButton';
import { toast } from 'sonner';
import type { AxiosError } from 'axios';
import type { ApiResponse } from '@/types';

const STEPS = ['Account', 'Personal', 'Confirm'] as const;

export function RegisterPage() {
  const navigate = useNavigate();
  const register = useAuthStore((s) => s.register);
  const googleLogin = useAuthStore((s) => s.googleLogin);
  const [step, setStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // Form data
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
      // New users always go to onboarding
      navigate('/onboarding', { replace: true });
    } catch (err) {
      const axiosErr = err as AxiosError<ApiResponse>;
      const msg = axiosErr.response?.data?.message || 'Registration failed.';
      const errors = axiosErr.response?.data?.errors;
      if (errors) {
        const firstKey = Object.keys(errors)[0];
        if (firstKey) toast.error(errors[firstKey][0]);
        else toast.error(msg);
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
          {/* Step indicator */}
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
                <motion.div
                  key="step-0"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  {/* Google sign-up button at top of step 1 */}
                  <GoogleLoginButton
                    text="Sign up with Google"
                    disabled={isSubmitting || isGoogleLoading}
                    onSuccess={async (credential) => {
                      setIsGoogleLoading(true);
                      try {
                        const { has_completed_onboarding } = await googleLogin(credential);
                        if (!has_completed_onboarding) {
                          navigate('/onboarding', { replace: true });
                        } else {
                          navigate('/', { replace: true });
                        }
                      } catch (err) {
                        const axiosErr = err as AxiosError<ApiResponse>;
                        const msg = axiosErr.response?.data?.message || 'Google sign-up failed.';
                        toast.error(msg);
                      } finally {
                        setIsGoogleLoading(false);
                      }
                    }}
                    onError={() => toast.error('Google sign-in was cancelled or failed.')}
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
                      onChange={(e) => setEmail(e.target.value)}
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
                      onChange={(e) => setUsername(e.target.value)}
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
              )}

              {step === 1 && (
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
                        onChange={(e) => setPassword(e.target.value)}
                        autoComplete="new-password"
                        minLength={8}
                        required
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                        tabIndex={-1}
                      >
                        {showPassword ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      At least 8 characters with one digit
                    </p>
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
                      onChange={(e) => setPasswordConfirm(e.target.value)}
                      autoComplete="new-password"
                      required
                    />
                  </div>
                </motion.div>
              )}

              {step === 2 && (
                <motion.div
                  key="step-2"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="space-y-4"
                >
                  <div className="space-y-2">
                    <label htmlFor="fullname" className="text-sm font-medium">
                      Full Name{' '}
                      <span className="text-muted-foreground">(optional)</span>
                    </label>
                    <Input
                      id="fullname"
                      type="text"
                      placeholder="John Doe"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                    />
                  </div>
                  <div className="rounded-lg bg-muted/50 p-4 space-y-2 text-sm">
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
                <Button
                  type="submit"
                  className="flex-1 gap-2"
                  disabled={isSubmitting}
                >
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
