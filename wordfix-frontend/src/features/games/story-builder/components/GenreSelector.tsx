import { useState } from 'react';
import GenreCard from './GenreCard';

const GENRES = [
  { genre: 'adventure', icon: '⚔️', gradient: 'from-amber-500/20 to-orange-500/10' },
  { genre: 'mystery', icon: '🔍', gradient: 'from-purple-500/20 to-indigo-500/10' },
  { genre: 'romance', icon: '💕', gradient: 'from-pink-500/20 to-rose-500/10' },
  { genre: 'sci-fi', icon: '🚀', gradient: 'from-cyan-500/20 to-blue-500/10' },
  { genre: 'fantasy', icon: '🐉', gradient: 'from-violet-500/20 to-purple-500/10' },
  { genre: 'comedy', icon: '😂', gradient: 'from-yellow-500/20 to-amber-500/10' },
];

interface Props {
  onSelect: (genre: string) => void;
  isLoading: boolean;
}

export default function GenreSelector({ onSelect, isLoading }: Props) {
  const [selected, setSelected] = useState('');

  const handleSelect = (genre: string) => {
    setSelected(genre);
    onSelect(genre);
  };

  return (
    <div className="mx-auto max-w-md py-8 text-center">
      <h2 className="mb-2 font-heading text-2xl font-bold">Choose a Genre</h2>
      <p className="mb-6 text-sm text-muted-foreground">Pick a genre for your AI-collaborative story</p>
      <div className="grid grid-cols-3 gap-3">
        {GENRES.map((g) => (
          <GenreCard
            key={g.genre}
            {...g}
            isSelected={selected === g.genre}
            onClick={() => !isLoading && handleSelect(g.genre)}
          />
        ))}
      </div>
    </div>
  );
}
