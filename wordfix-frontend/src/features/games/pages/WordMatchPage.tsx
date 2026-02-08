import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shuffle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { PageTransition } from '@/components/animations/PageTransition';
import { useStartWordMatch, useSubmitWordMatch } from '../hooks/useGames';
import type { WordMatchPair } from '@/types';

export function WordMatchPage() {
  const navigate = useNavigate();
  const startGame = useStartWordMatch();
  const submitGame = useSubmitWordMatch();

  const [sessionId, setSessionId] = useState<string | null>(null);
  const [words, setWords] = useState<{ word_id: string; word: string }[]>([]);
  const [translations, setTranslations] = useState<string[]>([]);
  const [started, setStarted] = useState(false);
  const [selectedWord, setSelectedWord] = useState<number | null>(null);
  const [selectedTranslation, setSelectedTranslation] = useState<number | null>(null);
  const [matchedPairs, setMatchedPairs] = useState<WordMatchPair[]>([]);
  const [matchedWordIdxs, setMatchedWordIdxs] = useState<Set<number>>(new Set());
  const [matchedTransIdxs, setMatchedTransIdxs] = useState<Set<number>>(new Set());

  const handleStart = () => {
    startGame.mutate(undefined, {
      onSuccess: (res) => {
        setSessionId(res.data.session_id);
        setWords(res.data.words);
        setTranslations(res.data.translations);
        setStarted(true);
      },
    });
  };

  const tryMatch = (wordIdx: number, transIdx: number) => {
    const pair: WordMatchPair = {
      word_id: words[wordIdx].word_id,
      matched_translation: translations[transIdx],
    };
    setMatchedPairs((p) => [...p, pair]);
    setMatchedWordIdxs((s) => new Set(s).add(wordIdx));
    setMatchedTransIdxs((s) => new Set(s).add(transIdx));
    setSelectedWord(null);
    setSelectedTranslation(null);

    // Check if all matched
    if (matchedPairs.length + 1 === words.length) {
      submitGame.mutate(
        { sessionId: sessionId!, pairs: [...matchedPairs, pair], timeSeconds: 0 },
        {
          onSuccess: (res) => {
            navigate(`/games/result/${sessionId}`, {
              replace: true,
              state: {
                game_type: 'word_match',
                score: res.data.score,
                max_score: res.data.max_score,
                xp_earned: res.data.xp_earned,
                correct_answers: res.data.correct_answers,
                total_questions: res.data.total_questions,
              },
            });
          },
        },
      );
    }
  };

  const handleWordClick = (idx: number) => {
    if (matchedWordIdxs.has(idx)) return;
    setSelectedWord(idx);
    if (selectedTranslation !== null) tryMatch(idx, selectedTranslation);
  };

  const handleTransClick = (idx: number) => {
    if (matchedTransIdxs.has(idx)) return;
    setSelectedTranslation(idx);
    if (selectedWord !== null) tryMatch(selectedWord, idx);
  };

  if (!started) {
    return (
      <PageTransition>
        <div className="mx-auto flex max-w-md flex-col items-center justify-center gap-6 py-20">
          <div className="rounded-2xl bg-blue-500/10 p-6">
            <Shuffle className="h-16 w-16 text-blue-500" />
          </div>
          <h1 className="text-2xl font-bold">Word Match</h1>
          <p className="text-center text-muted-foreground">
            Match each word with its correct translation. Select a word on the left, then its translation on the right.
          </p>
          <Button size="lg" onClick={handleStart} disabled={startGame.isPending}>
            {startGame.isPending ? 'Loading...' : 'Start Game'}
          </Button>
          {startGame.isError && (
            <p className="text-sm text-red-500">Not enough words to play. Add more words first!</p>
          )}
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="mx-auto max-w-2xl space-y-6">
        <div className="text-center">
          <h2 className="text-lg font-semibold">Match the Words</h2>
          <p className="text-sm text-muted-foreground">
            {matchedPairs.length}/{words.length} matched
          </p>
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Words Column */}
          <div className="space-y-2">
            {words.map((w, i) => (
              <motion.div key={w.word_id} layout>
                <Button
                  variant={matchedWordIdxs.has(i) ? 'default' : selectedWord === i ? 'secondary' : 'outline'}
                  className={`w-full justify-center h-auto py-3 ${matchedWordIdxs.has(i) ? 'opacity-60' : ''}`}
                  onClick={() => handleWordClick(i)}
                  disabled={matchedWordIdxs.has(i)}
                >
                  {w.word}
                </Button>
              </motion.div>
            ))}
          </div>

          {/* Translations Column */}
          <div className="space-y-2">
            {translations.map((t, i) => (
              <motion.div key={`${t}-${i}`} layout>
                <Button
                  variant={matchedTransIdxs.has(i) ? 'default' : selectedTranslation === i ? 'secondary' : 'outline'}
                  className={`w-full justify-center h-auto py-3 ${matchedTransIdxs.has(i) ? 'opacity-60' : ''}`}
                  onClick={() => handleTransClick(i)}
                  disabled={matchedTransIdxs.has(i)}
                >
                  {t}
                </Button>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
