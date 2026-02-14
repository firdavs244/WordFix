import { motion, AnimatePresence } from 'framer-motion';
import { ArrowRight, Brain, Lightbulb, BookOpen } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import type { DrillData } from '../types';

interface DrillExplanationProps {
  drill: DrillData;
  onStartQuiz: () => void;
}

export function DrillExplanation({ drill, onStartQuiz }: DrillExplanationProps) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key="explanation"
        initial={{ opacity: 0, x: 30 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: -30 }}
        className="space-y-6"
      >
        <div className="flex items-center gap-2">
          <Brain className="h-6 w-6 text-primary" />
          <h2 className="font-heading text-xl font-bold">Understanding the Difference</h2>
        </div>

        <Card className="border-border/50">
          <CardHeader className="pb-2">
            <CardTitle className="flex items-center gap-2 text-base">
              <BookOpen className="h-4 w-4 text-blue-500" />
              Explanation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm leading-relaxed">{drill.explanation}</p>
          </CardContent>
        </Card>

        <Card className="border-amber-500/30 bg-amber-500/5">
          <CardContent className="flex items-start gap-3 p-4">
            <Lightbulb className="mt-0.5 h-5 w-5 text-amber-500" />
            <div>
              <p className="text-sm font-medium text-amber-600 dark:text-amber-400">
                Memory Trick
              </p>
              <p className="mt-1 text-sm">{drill.mnemonic}</p>
            </div>
          </CardContent>
        </Card>

        <div className="grid gap-4 sm:grid-cols-2">
          {drill.word_1_examples.length > 0 && (
            <Card className="border-border/50">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-primary">Examples</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {drill.word_1_examples.map((ex, i) => (
                  <div key={i} className="text-sm">
                    <p className="italic">&ldquo;{ex.sentence}&rdquo;</p>
                    <p className="text-xs text-muted-foreground">{ex.translation}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
          {drill.word_2_examples.length > 0 && (
            <Card className="border-border/50">
              <CardHeader className="pb-2">
                <CardTitle className="text-sm text-primary">Examples</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                {drill.word_2_examples.map((ex, i) => (
                  <div key={i} className="text-sm">
                    <p className="italic">&ldquo;{ex.sentence}&rdquo;</p>
                    <p className="text-xs text-muted-foreground">{ex.translation}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </div>

        <Button onClick={onStartQuiz} className="w-full gap-2" size="lg">
          Start Practice Quiz
          <ArrowRight className="h-5 w-5" />
        </Button>
      </motion.div>
    </AnimatePresence>
  );
}
