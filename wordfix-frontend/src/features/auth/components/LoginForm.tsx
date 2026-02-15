import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Mail, Loader2 } from 'lucide-react';
import { toast } from 'sonner';
import { useAuthStore } from '@/stores/useAuthStore';
import { AuthInput } from '../components/AuthInput';
import { PasswordInput } from '../components/PasswordInput';
import { AuthDivider } from '../components/AuthDivider';
import { GoogleLoginButton } from '../components/GoogleLoginButton';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, googleLogin } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password) return;
    setLoading(true);
    try {
      const { has_completed_onboarding } = await login({ email, password });
      navigate(has_completed_onboarding ? '/' : '/onboarding');
    } catch (err: any) {
      toast.error(err?.response?.data?.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogle = async (credential: string) => {
    try {
      const { has_completed_onboarding } = await googleLogin(credential);
      navigate(has_completed_onboarding ? '/' : '/onboarding');
    } catch {
      toast.error('Google login failed.');
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit} className="rounded-2xl border border-border/50 bg-card p-6 shadow-card lg:p-8">
        <div className="space-y-5">
          <AuthInput icon={Mail} label="Email" type="email" placeholder="you@example.com" value={email} onChange={setEmail} />
          <PasswordInput label="Password" placeholder="Enter your password" value={password} onChange={setPassword} />
          <button
            type="submit"
            disabled={loading || !email || !password}
            className="flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 text-sm font-semibold text-white shadow-lg shadow-primary/15 transition-all duration-200 hover:shadow-xl hover:shadow-primary/25 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? <><Loader2 className="h-4 w-4 animate-spin" /> Signing in...</> : 'Sign In'}
          </button>
          <AuthDivider />
          <GoogleLoginButton onSuccess={handleGoogle} />
        </div>
      </form>
      <p className="mt-6 text-center text-sm">
        Don&apos;t have an account?{' '}
        <Link to="/register" className="font-medium text-primary hover:underline">Create one</Link>
      </p>
    </>
  );
}
