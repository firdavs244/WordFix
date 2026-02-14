import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, ClipboardCheck, Gamepad2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export function DashboardQuickActions() {
  return (
    <motion.div
      className="grid gap-4 sm:grid-cols-2"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.18 }}
    >
      <Link to="/tests">
        <Card className="cursor-pointer border-border/50 transition-all hover:-translate-y-0.5 hover:shadow-md">
          <CardContent className="flex items-center gap-4 p-5">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-500/10">
              <ClipboardCheck className="h-6 w-6 text-indigo-500" />
            </div>
            <div className="flex-1">
              <p className="font-heading text-lg font-semibold">Take a Test</p>
              <p className="text-sm text-muted-foreground">AI generates tests from your words</p>
            </div>
            <ArrowRight className="h-5 w-5 text-muted-foreground" />
          </CardContent>
        </Card>
      </Link>
      <Link to="/games">
        <Card className="cursor-pointer border-border/50 transition-all hover:-translate-y-0.5 hover:shadow-md">
          <CardContent className="flex items-center gap-4 p-5">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-pink-500/10">
              <Gamepad2 className="h-6 w-6 text-pink-500" />
            </div>
            <div className="flex-1">
              <p className="font-heading text-lg font-semibold">Play a Game</p>
              <p className="text-sm text-muted-foreground">
                3 game modes to boost your vocabulary
              </p>
            </div>
            <ArrowRight className="h-5 w-5 text-muted-foreground" />
          </CardContent>
        </Card>
      </Link>
    </motion.div>
  );
}
