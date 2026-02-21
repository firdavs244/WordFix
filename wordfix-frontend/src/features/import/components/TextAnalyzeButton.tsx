import { Sparkles, Loader2 } from 'lucide-react';

interface TextAnalyzeButtonProps {
  onClick: () => void;
  isLoading: boolean;
  disabled: boolean;
}

export default function TextAnalyzeButton({ onClick, isLoading, disabled }: TextAnalyzeButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled || isLoading}
      className="flex h-11 items-center gap-2 rounded-xl bg-gradient-to-r from-primary to-primary/90 px-6 text-sm font-medium text-white shadow-lg shadow-primary/15 transition-all hover:shadow-primary/25 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {isLoading ? (
        <>
          <Loader2 className="h-4 w-4 animate-spin" />
          <span>Analyzing with AI...</span>
        </>
      ) : (
        <>
          <Sparkles className="h-4 w-4" />
          <span>Analyze Text</span>
        </>
      )}
    </button>
  );
}
