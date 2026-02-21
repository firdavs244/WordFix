import { cn } from '@/lib/utils';

interface ImportStepIndicatorProps {
  currentStep: number;
  steps: string[];
}

export default function ImportStepIndicator({ currentStep, steps }: ImportStepIndicatorProps) {
  return (
    <div className="flex items-center justify-center gap-0">
      {steps.map((step, i) => (
        <div key={step} className="flex items-center">
          <div className="flex flex-col items-center">
            <div
              className={cn(
                'flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold transition-all',
                i < currentStep && 'bg-primary text-white',
                i === currentStep && 'bg-primary text-white ring-4 ring-primary/20',
                i > currentStep && 'bg-muted text-muted-foreground',
              )}
            >
              {i < currentStep ? '✓' : i + 1}
            </div>
            <span className="mt-1 text-[10px] font-medium text-muted-foreground">{step}</span>
          </div>
          {i < steps.length - 1 && (
            <div className={cn('mx-2 h-0.5 w-12', i < currentStep ? 'bg-primary' : 'bg-muted')} />
          )}
        </div>
      ))}
    </div>
  );
}
