import MultipleChoiceOption from './MultipleChoiceOption';

interface Props {
  options: string[];
  onSelect: (index: number) => void;
  selectedIndex?: number;
  correctIndex?: number;
  answered: boolean;
}

export default function MultipleChoiceQuestion({
  options, onSelect, selectedIndex, correctIndex, answered,
}: Props) {
  return (
    <div className="space-y-3" role="group" aria-label="Answer options">
      {options.map((text, i) => (
        <MultipleChoiceOption
          key={i}
          text={text}
          index={i}
          isSelected={selectedIndex === i}
          isCorrect={answered && correctIndex === i ? true : null}
          isWrong={answered && selectedIndex === i && correctIndex !== i ? true : null}
          disabled={answered}
          onClick={() => !answered && onSelect(i)}
        />
      ))}
    </div>
  );
}
