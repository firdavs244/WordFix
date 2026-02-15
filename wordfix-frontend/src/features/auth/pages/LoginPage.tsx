import { motion } from 'framer-motion';
import { scaleIn } from '@/lib/motion';
import { Logo } from '@/components/shared';
import { LoginForm } from '../components/LoginForm';
import { SocialProofBadge } from '../components/SocialProofBadge';

export function LoginPage() {
  return (
    <motion.div variants={scaleIn} initial="initial" animate="animate" className="mx-auto w-full max-w-md">
      <div className="mb-8 text-center">
        <Logo size="md" className="mx-auto mb-6" />
        <h1 className="font-heading text-2xl font-bold tracking-tight">Welcome Back</h1>
        <p className="mt-1.5 text-sm text-muted-foreground">Sign in to continue your learning journey</p>
      </div>
      <LoginForm />
      <SocialProofBadge />
    </motion.div>
  );
}
