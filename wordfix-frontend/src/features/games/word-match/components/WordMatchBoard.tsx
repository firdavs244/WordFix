import WordMatchItem from './WordMatchItem';

interface Pair {
  wordId: string;
  word: string;
  translation: string;
  matched: boolean;
}

interface Props {
  pairs: Pair[];
  translations: string[];
  selectedWord: string | null;
  selectedTranslation: string | null;
  wrongPair: { word: string; translation: string } | null;
  onSelectWord: (word: string) => void;
  onSelectTranslation: (translation: string) => void;
}

export default function WordMatchBoard({
  pairs, translations, selectedWord, selectedTranslation, wrongPair,
  onSelectWord, onSelectTranslation,
}: Props) {
  const matchedTranslations = pairs.filter((p) => p.matched).map((p) => p.translation);

  return (
    <div className="grid grid-cols-2 gap-6" data-testid="match-board">
      <div className="space-y-3">
        <p className="text-center text-xs font-medium text-muted-foreground">Words</p>
        {pairs.map((p) => (
          <WordMatchItem
            key={p.wordId}
            text={p.word}
            type="word"
            isSelected={selectedWord === p.word}
            isMatched={p.matched}
            isWrong={wrongPair?.word === p.word}
            onClick={() => onSelectWord(p.word)}
          />
        ))}
      </div>
      <div className="space-y-3">
        <p className="text-center text-xs font-medium text-muted-foreground">Translations</p>
        {translations.map((t) => (
          <WordMatchItem
            key={t}
            text={t}
            type="translation"
            isSelected={selectedTranslation === t}
            isMatched={matchedTranslations.includes(t)}
            isWrong={wrongPair?.translation === t}
            onClick={() => onSelectTranslation(t)}
          />
        ))}
      </div>
    </div>
  );
}
