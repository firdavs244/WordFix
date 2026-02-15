import { Component, type ErrorInfo, type ReactNode } from 'react';
import { motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { scaleIn } from '@/lib/motion';

interface Props { children: ReactNode; fallback?: ReactNode }
interface State { hasError: boolean; error: Error | null }

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('ErrorBoundary:', error, info);
  }

  render() {
    if (!this.state.hasError) return this.props.children;
    if (this.props.fallback) return this.props.fallback;

    return (
      <div className="flex h-[50vh] items-center justify-center">
        <motion.div variants={scaleIn} initial="initial" animate="animate" className="flex flex-col items-center gap-4 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-full bg-destructive/10">
            <AlertTriangle className="h-6 w-6 text-destructive" />
          </div>
          <h2 className="font-heading text-xl font-semibold">Something went wrong</h2>
          {this.state.error && <p className="max-w-md text-sm text-muted-foreground">{this.state.error.message}</p>}
          <Button variant="destructive" onClick={() => this.setState({ hasError: false, error: null })}>
            Try Again
          </Button>
        </motion.div>
      </div>
    );
  }
}
