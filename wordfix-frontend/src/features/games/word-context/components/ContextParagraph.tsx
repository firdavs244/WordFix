interface Props {
  context: string;
  answered: boolean;
  correctAnswer?: string;
  userAnswer?: string;
  isCorrect?: boolean;
}

export default function ContextParagraph({ context, answered, correctAnswer, userAnswer, isCorrect }: Props) {
  const parts = context.split('___');

  return (
    <div className="rounded-xl border border-border/50 bg-muted/20 p-5">
      <p className="text-base leading-relaxed">
        {parts[0]}
        <span
          className={`inline-block min-w-[60px] rounded border-b-2 px-3 py-0.5 text-center font-medium ${
            !answered ? 'border-primary/30 bg-primary/10 text-primary' :
            isCorrect ? 'border-success/30 bg-success/10 text-success' :
            'border-destructive/30 bg-destructive/10 text-destructive line-through'
          }`}
        >
          {answered ? userAnswer || '___' : '___'}
        </span>
        {parts[1]}
      </p>
      {answered && !isCorrect && correctAnswer && (
        <p className="mt-2 text-sm font-medium text-success">Correct answer: {correctAnswer}</p>
      )}
    </div>
  );
}
