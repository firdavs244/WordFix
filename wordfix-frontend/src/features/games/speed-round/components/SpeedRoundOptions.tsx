import { useState, useCallback } from 'react';
import SpeedRoundOption from './SpeedRoundOption';

interface Props {
  options: string[];
  correctAnswer: string;
  onAnswer: (selected: string, correct: boolean) => void;
}

export default function SpeedRoundOptions({ options, correctAnswer, onAnswer }: Props) {
  const [selectedIdx, setSelectedIdx] = useState<number | null>(null);
  const [state, setState] = useState<('default' | 'correct' | 'wrong')[]>(
    options.map(() => 'default'),
  );

  const handleClick = useCallback((idx: number) => {
    if (selectedIdx !== null) return;
    setSelectedIdx(idx);
    const correct = options[idx] === correctAnswer;
    const newState = options.map((_, i) => {
      if (i === idx) return correct ? 'correct' : 'wrong';
      if (options[i] === correctAnswer) return 'correct';
      return 'default';
    }) as ('default' | 'correct' | 'wrong')[];
    setState(newState);
    setTimeout(() => onAnswer(options[idx], correct), 500);
  }, [selectedIdx, options, correctAnswer, onAnswer]);

  return (
    <div className="grid grid-cols-2 gap-3">
      {options.map((opt, i) => (
        <SpeedRoundOption
          key={i}
          text={opt}
          index={i}
          state={state[i]}
          disabled={selectedIdx !== null}
          onClick={() => handleClick(i)}
        />
      ))}
    </div>
  );
}
