import { FileText, Clock, BarChart3 } from 'lucide-react';

interface Props {
  totalQuestions?: number;
}

export function OnboardingStats({ totalQuestions }: Props) {
  const stats = [
    { icon: FileText, value: String(totalQuestions || 18), label: 'questions' },
    { icon: Clock, value: '3-5', label: 'minutes' },
    { icon: BarChart3, value: 'A1-C2', label: 'levels' },
  ];

  return (
    <div className="mt-6 flex justify-center gap-6 lg:gap-8">
      {stats.map((s) => (
        <div key={s.label} className="flex flex-col items-center gap-1">
          <s.icon className="h-3.5 w-3.5 text-primary/50" />
          <span className="font-heading text-sm font-bold">{s.value}</span>
          <span className="text-[10px] uppercase tracking-wide text-muted-foreground">{s.label}</span>
        </div>
      ))}
    </div>
  );
}
