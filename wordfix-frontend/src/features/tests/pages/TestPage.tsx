import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Brain, ClipboardList, Pen, MessageSquare, Shuffle, ArrowRight, History } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PageTransition } from '@/components/animations/PageTransition';
import { useGenerateTest, useTestHistory } from '../hooks/useTests';
import type { TestType, TestDifficulty } from '@/types';
import { Link } from 'react-router-dom';
import { Badge } from '@/components/ui/badge';

const testTypes: { value: TestType; label: string; icon: typeof Brain; desc: string }[] = [
  { value: 'multiple_choice', label: 'Multiple Choice', icon: ClipboardList, desc: 'Choose the correct answer from options' },
  { value: 'fill_blank', label: 'Fill in the Blank', icon: Pen, desc: 'Type the missing word' },
  { value: 'context_guess', label: 'Context Guess', icon: MessageSquare, desc: 'Guess the word from context' },
  { value: 'mixed', label: 'Mixed', icon: Shuffle, desc: 'Mix of all question types' },
];

const difficulties: { value: TestDifficulty; label: string; color: string }[] = [
  { value: 'easy', label: 'Easy', color: 'text-green-500' },
  { value: 'medium', label: 'Medium', color: 'text-yellow-500' },
  { value: 'hard', label: 'Hard', color: 'text-red-500' },
  { value: 'adaptive', label: 'Adaptive', color: 'text-primary' },
];

export function TestPage() {
  const navigate = useNavigate();
  const [selectedType, setSelectedType] = useState<TestType>('mixed');
  const [selectedDifficulty, setSelectedDifficulty] = useState<TestDifficulty>('adaptive');
  const [questionCount, setQuestionCount] = useState(10);
  const generateTest = useGenerateTest();
  const { data: historyData } = useTestHistory();
  const recentTests = historyData?.data?.slice(0, 3) ?? [];

  const handleStart = () => {
    generateTest.mutate(
      { test_type: selectedType, question_count: questionCount, difficulty: selectedDifficulty },
      {
        onSuccess: (res) => {
          navigate(`/tests/session/${res.data.session.id}`, {
            state: { session: res.data.session, questions: res.data.questions },
          });
        },
      },
    );
  };

  return (
    <PageTransition>
      <div className="mx-auto max-w-4xl space-y-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-heading text-3xl font-bold flex items-center gap-2">
            <Brain className="h-8 w-8 text-primary" /> AI Test Generator
          </h1>
          <p className="mt-1 text-muted-foreground">Test your vocabulary knowledge with AI-generated questions</p>
        </motion.div>

        {/* Test Type Selection */}
        <div className="space-y-3">
          <h2 className="font-heading text-lg font-semibold">Question Type</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {testTypes.map((t) => (
              <motion.div key={t.value} whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Card
                  className={`cursor-pointer transition-all ${selectedType === t.value ? 'border-primary bg-primary/5 ring-1 ring-primary' : 'border-border/50 hover:border-primary/30'}`}
                  onClick={() => setSelectedType(t.value)}
                >
                  <CardContent className="flex items-center gap-3 p-4">
                    <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${selectedType === t.value ? 'bg-primary/10' : 'bg-muted'}`}>
                      <t.icon className={`h-5 w-5 ${selectedType === t.value ? 'text-primary' : 'text-muted-foreground'}`} />
                    </div>
                    <div>
                      <p className="font-medium">{t.label}</p>
                      <p className="text-xs text-muted-foreground">{t.desc}</p>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Difficulty & Count */}
        <div className="grid gap-6 sm:grid-cols-2">
          <div className="space-y-3">
            <h2 className="font-heading text-lg font-semibold">Difficulty</h2>
            <div className="flex flex-wrap gap-2">
              {difficulties.map((d) => (
                <Button
                  key={d.value}
                  variant={selectedDifficulty === d.value ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setSelectedDifficulty(d.value)}
                >
                  {d.label}
                </Button>
              ))}
            </div>
          </div>
          <div className="space-y-3">
            <h2 className="font-heading text-lg font-semibold">Questions: {questionCount}</h2>
            <input
              type="range"
              min={5}
              max={30}
              value={questionCount}
              onChange={(e) => setQuestionCount(Number(e.target.value))}
              className="w-full accent-primary"
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>5</span><span>30</span>
            </div>
          </div>
        </div>

        {/* Start Button */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
          <Button
            size="lg"
            className="w-full gap-2 text-lg shadow-lg shadow-primary/25"
            onClick={handleStart}
            disabled={generateTest.isPending}
          >
            {generateTest.isPending ? 'Generating...' : 'Start Test'}
            <ArrowRight className="h-5 w-5" />
          </Button>
        </motion.div>

        {/* Recent Tests */}
        {recentTests.length > 0 && (
          <Card className="border-border/50">
            <CardHeader className="flex flex-row items-center justify-between">
              <CardTitle className="flex items-center gap-2 text-lg">
                <History className="h-5 w-5 text-muted-foreground" /> Recent Tests
              </CardTitle>
              <Link to="/tests/history">
                <Button variant="ghost" size="sm">View All</Button>
              </Link>
            </CardHeader>
            <CardContent className="divide-y divide-border">
              {recentTests.map((t) => (
                <Link key={t.id} to={`/tests/result/${t.id}`} className="flex items-center justify-between py-3">
                  <div>
                    <p className="font-medium capitalize">{t.test_type.replace('_', ' ')}</p>
                    <p className="text-xs text-muted-foreground">{new Date(t.created_at).toLocaleDateString()}</p>
                  </div>
                  <Badge variant={t.score_percentage >= 80 ? 'success' : t.score_percentage >= 50 ? 'warning' : 'destructive'}>
                    {Math.round(t.score_percentage)}%
                  </Badge>
                </Link>
              ))}
            </CardContent>
          </Card>
        )}
      </div>
    </PageTransition>
  );
}
