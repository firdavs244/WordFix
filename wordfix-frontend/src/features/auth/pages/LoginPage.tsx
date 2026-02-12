import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Eye, EyeOff, LogIn } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { useAuthStore } from '@/stores/useAuthStore';
import { GoogleLoginButton } from '@/features/auth/components/GoogleLoginButton';
import { toast } from 'sonner';
import type { AxiosError } from 'axios';
import type { ApiResponse } from '@/types';

export function LoginPage() {
  const navigate = useNavigate();
  const login = useAuthStore((s) => s.login);
  const googleLogin = useAuthStore((s) => s.googleLogin);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isGoogleLoading, setIsGoogleLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) {
      toast.error('Please fill in all fields.');
      return;
    }

    setIsSubmitting(true);
    try {
      const { has_completed_onboarding } = await login({ email, password });
      if (!has_completed_onboarding) {
        navigate('/onboarding', { replace: true });
      } else {
        navigate('/', { replace: true });
      }
    } catch (err) {
      const axiosErr = err as AxiosError<ApiResponse>;
      const msg = axiosErr.response?.data?.message || 'Login failed.';
      toast.error(msg);
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
          <CardTitle className="font-heading text-2xl">Welcome Back</CardTitle>
          <CardDescription>Sign in to continue learning</CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
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
                  autoComplete="current-password"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <Button type="submit" className="w-full gap-2" disabled={isSubmitting}>
              {isSubmitting ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              ) : (
                <LogIn className="h-4 w-4" />
              )}
              {isSubmitting ? 'Signing in...' : 'Sign In'}
            </Button>

            {/* Google OAuth divider */}
            <div className="relative flex w-full items-center gap-3">
              <Separator className="flex-1" />
              <span className="text-xs text-muted-foreground">or continue with</span>
              <Separator className="flex-1" />
            </div>

            <GoogleLoginButton
              text="Continue with Google"
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
                  const msg = axiosErr.response?.data?.message || 'Google login failed.';
                  toast.error(msg);
                } finally {
                  setIsGoogleLoading(false);
                }
              }}
              onError={() => toast.error('Google sign-in was cancelled or failed.')}
            />

            <p className="text-center text-sm text-muted-foreground">
              Don't have an account?{' '}
              <Link to="/register" className="font-medium text-primary hover:underline">
                Sign Up
              </Link>
            </p>
          </CardFooter>
        </form>
      </Card>
    </motion.div>
  );
}
