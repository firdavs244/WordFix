import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Brain, Gamepad2, TrendingUp, ArrowRight, Sun, Moon, Monitor, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Logo } from '@/components/common/Logo';
import { useTheme } from '@/hooks/useTheme';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Learning',
    description:
      'Smart algorithms adapt to your learning pace and help you memorize words more effectively.',
    color: 'from-primary to-primary-light',
  },
  {
    icon: Gamepad2,
    title: 'Smart Games',
    description:
      'Fun and engaging games that make vocabulary building an enjoyable daily habit.',
    color: 'from-secondary to-emerald-400',
  },
  {
    icon: TrendingUp,
    title: 'Track Progress',
    description:
      'Detailed analytics and insights to visualize your learning journey and achievements.',
    color: 'from-accent to-orange-400',
  },
];

export function LandingPage() {
  const { theme, setTheme } = useTheme();

  const cycleTheme = () => {
    if (theme === 'light') setTheme('dark');
    else if (theme === 'dark') setTheme('system');
    else setTheme('light');
  };

  const ThemeIcon = theme === 'light' ? Sun : theme === 'dark' ? Moon : Monitor;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="fixed top-0 z-50 w-full border-b border-border/50 bg-background/80 backdrop-blur-lg">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <Logo />
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="icon" onClick={cycleTheme}>
              <ThemeIcon className="h-5 w-5" />
            </Button>
            <Link to="/login">
              <Button variant="outline" size="sm">
                Sign In
              </Button>
            </Link>
            <Link to="/register">
              <Button size="sm">Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 pt-16">
        {/* Background gradient */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute left-1/2 top-0 h-[600px] w-[800px] -translate-x-1/2 rounded-full bg-primary/10 blur-3xl" />
          <div className="absolute bottom-0 right-0 h-[400px] w-[600px] rounded-full bg-secondary/10 blur-3xl" />
        </div>

        <div className="mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: 'easeOut' }}
          >
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm text-primary">
              <Sparkles className="h-4 w-4" />
              AI-Powered Vocabulary Learning
            </div>

            <h1 className="font-heading text-5xl font-extrabold tracking-tight sm:text-6xl lg:text-7xl">
              Master{' '}
              <span className="text-gradient">Every Word</span>
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground sm:text-xl">
              Build your English vocabulary with AI-powered learning, smart games,
              and spaced repetition. Join thousands of learners mastering new words
              every day.
            </p>
          </motion.div>

          <motion.div
            className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <Link to="/register">
              <Button size="lg" className="gap-2 px-8 text-base shadow-lg shadow-primary/25">
                Get Started Free
                <ArrowRight className="h-5 w-5" />
              </Button>
            </Link>
            <Button variant="outline" size="lg" className="gap-2 px-8 text-base">
              Learn More
            </Button>
          </motion.div>

          {/* Stats */}
          <motion.div
            className="mt-16 grid grid-cols-3 gap-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            {[
              { value: '10K+', label: 'Words' },
              { value: '50K+', label: 'Learners' },
              { value: '95%', label: 'Success Rate' },
            ].map((stat) => (
              <div key={stat.label}>
                <div className="font-heading text-3xl font-bold text-foreground">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t border-border bg-muted/30 py-24">
        <div className="mx-auto max-w-6xl px-4">
          <motion.div
            className="text-center"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
          >
            <h2 className="font-heading text-3xl font-bold sm:text-4xl">
              Why WordFix?
            </h2>
            <p className="mt-4 text-lg text-muted-foreground">
              Everything you need to build a powerful vocabulary
            </p>
          </motion.div>

          <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                className="group rounded-2xl border border-border bg-card p-8 shadow-sm transition-shadow hover:shadow-lg"
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                whileHover={{ scale: 1.02, y: -4 }}
              >
                <div
                  className={`mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${feature.color}`}
                >
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="font-heading text-xl font-semibold">
                  {feature.title}
                </h3>
                <p className="mt-2 text-muted-foreground">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-border py-24">
        <motion.div
          className="mx-auto max-w-3xl px-4 text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="font-heading text-3xl font-bold sm:text-4xl">
            Ready to expand your vocabulary?
          </h2>
          <p className="mt-4 text-lg text-muted-foreground">
            Start learning today — it&apos;s free. No credit card required.
          </p>
          <Link to="/register">
            <Button size="lg" className="mt-8 gap-2 px-8 text-base shadow-lg shadow-primary/25">
              Start Learning Now
              <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border bg-muted/30 py-8">
        <div className="mx-auto max-w-6xl px-4 text-center">
          <Logo className="mx-auto mb-4 justify-center" />
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} WordFix. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
