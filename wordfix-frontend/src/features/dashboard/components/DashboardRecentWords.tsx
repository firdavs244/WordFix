import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { BookOpen, ArrowRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';

const difficultyColors = {
  easy: 'success' as const,
  medium: 'warning' as const,
  hard: 'destructive' as const,
};

interface RecentWord {
  id: string;
  original_word: string;
  translation?: string;
  definition?: string;
  difficulty_level: string;
}

interface DashboardRecentWordsProps {
  words: RecentWord[];
  isLoading: boolean;
}

export function DashboardRecentWords({ words, isLoading }: DashboardRecentWordsProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.3 }}
    >
      <Card className="border-border/50">
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="flex items-center gap-2 text-xl">
            <BookOpen className="h-5 w-5 text-muted-foreground" />
            Recent Words
          </CardTitle>
          <Link to="/words">
            <Button variant="ghost" size="sm" className="gap-1 text-primary">
              View All
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between py-3">
                  <div className="space-y-1">
                    <Skeleton className="h-5 w-32" />
                    <Skeleton className="h-4 w-48" />
                  </div>
                  <Skeleton className="h-6 w-16 rounded-full" />
                </div>
              ))}
            </div>
          ) : words.length > 0 ? (
            <div className="divide-y divide-border">
              {words.map((word, index) => (
                <motion.div
                  key={word.id}
                  className="flex items-center justify-between py-3 first:pt-0 last:pb-0"
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: 0.4 + index * 0.05 }}
                >
                  <div>
                    <p className="font-medium">{word.original_word}</p>
                    <p className="text-sm text-muted-foreground">
                      {word.translation || word.definition || 'No translation'}
                    </p>
                  </div>
                  <Badge
                    variant={
                      difficultyColors[word.difficulty_level as keyof typeof difficultyColors] ??
                      'outline'
                    }
                  >
                    {word.difficulty_level}
                  </Badge>
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="py-8 text-center text-muted-foreground">
              No words yet. Start by adding your first word!
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
