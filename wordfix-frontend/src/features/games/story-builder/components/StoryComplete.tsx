import { BookOpen, Award } from 'lucide-react';

interface Props {
  fullStory: string;
  totalScore: number;
  maxScore: number;
}

export default function StoryComplete({ fullStory, totalScore, maxScore }: Props) {
  return (
    <div className="space-y-4" data-testid="story-complete">
      <div className="flex items-center justify-center gap-2">
        <Award className="h-6 w-6 text-accent" />
        <span className="font-heading text-2xl font-bold">{totalScore}/{maxScore}</span>
      </div>
      <div className="rounded-xl border border-border/50 bg-muted/10 p-5">
        <div className="mb-2 flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-primary" />
          <span className="text-sm font-semibold">Your Story</span>
        </div>
        <p className="whitespace-pre-wrap text-sm leading-relaxed text-muted-foreground">
          {fullStory}
        </p>
      </div>
    </div>
  );
}
