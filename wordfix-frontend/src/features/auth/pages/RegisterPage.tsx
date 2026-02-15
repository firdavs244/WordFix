import { useState, useRef } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { scaleIn } from '@/lib/motion';
import { Logo } from '@/components/shared';
import { useAuthStore } from '@/stores/useAuthStore';
import { RegisterStepIndicator } from '../components/RegisterStepIndicator';
import { RegisterStepAccount } from '../components/RegisterStepAccount';
import { RegisterStepPassword } from '../components/RegisterStepPassword';
import { RegisterStepConfirm } from '../components/RegisterStepConfirm';
import { SocialProofBadge } from '../components/SocialProofBadge';

export function RegisterPage() {
  const [step, setStep] = useState(0);
  const [formData, setFormData] = useState({ email: '', username: '', password: '', confirmPassword: '', fullName: '' });
  const [loading, setLoading] = useState(false);
  const direction = useRef(1);
  const navigate = useNavigate();
  const { register, googleLogin } = useAuthStore();

  const onChange = (field: string, value: string) => setFormData((p) => ({ ...p, [field]: value }));

  const next = () => {
    if (step === 0) {
      if (!formData.email.includes('@')) { toast.error('Please enter a valid email.'); return; }
      if (formData.username.length < 3) { toast.error('Username must be at least 3 characters.'); return; }
    }
    direction.current = 1;
    setStep((s) => Math.min(s + 1, 2));
  };

  const back = () => { direction.current = -1; setStep((s) => Math.max(s - 1, 0)); };

  const handleGoogle = async (credential: string) => {
    try {
      const { has_completed_onboarding } = await googleLogin(credential);
      navigate(has_completed_onboarding ? '/' : '/onboarding', { replace: true });
    } catch { toast.error('Google sign-up failed.'); }
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      await register({ email: formData.email, username: formData.username, password: formData.password, password_confirm: formData.confirmPassword, full_name: formData.fullName || undefined });
      navigate('/onboarding', { replace: true });
    } catch (err: any) {
      const msg = err?.response?.data?.message || 'Registration failed.';
      const errors = err?.response?.data?.errors;
      toast.error(errors ? Object.values(errors).flat()[0] as string : msg);
    } finally { setLoading(false); }
  };

  return (
    <motion.div variants={scaleIn} initial="initial" animate="animate" className="mx-auto w-full max-w-md">
      <div className="mb-6 text-center">
        <Logo size="md" className="mx-auto mb-5" />
        <h1 className="font-heading text-2xl font-bold">Create Account</h1>
        <p className="mt-1 text-sm text-muted-foreground">Start your vocabulary journey today</p>
      </div>
      <RegisterStepIndicator currentStep={step} />
      <div className="mt-6 overflow-hidden">
        <AnimatePresence mode="wait" custom={direction.current}>
          {step === 0 && <RegisterStepAccount key="account" formData={formData} onChange={onChange} onNext={next} onGoogle={handleGoogle} direction={direction.current} />}
          {step === 1 && <RegisterStepPassword key="password" formData={formData} onChange={onChange} onNext={next} onBack={back} direction={direction.current} />}
          {step === 2 && <RegisterStepConfirm key="confirm" formData={formData} onChange={onChange} onBack={back} onSubmit={handleSubmit} isLoading={loading} direction={direction.current} />}
        </AnimatePresence>
      </div>
      <p className="mt-6 text-center text-sm">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-primary hover:underline">Sign In</Link>
      </p>
      <SocialProofBadge />
    </motion.div>
  );
}
