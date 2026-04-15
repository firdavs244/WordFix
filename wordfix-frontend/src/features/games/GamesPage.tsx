import { Gamepad2, Zap, Link2, FileText, Pencil, Headphones, ArrowLeftRight, BookType, Globe } from 'lucide-react';
import PageTransition from '@/components/shared/PageTransition';
import PageHeader from '@/components/shared/PageHeader';
import GameCard from './components/GameCard';

const GAMES = [
  { id: 'immersive', title: 'Immersive 3D', description: 'Practice English in realistic 3D scenarios with AI NPCs', icon: Globe, gradient: 'from-indigo-500/10 to-fuchsia-500/5', iconGradient: 'from-indigo-500 to-fuchsia-500', route: '/immersive' },
  { id: 'speed-round', title: 'Speed Round', description: 'Translate words against the clock', icon: Zap, gradient: 'from-amber-500/10 to-yellow-500/5', iconGradient: 'from-amber-500 to-yellow-500', route: '/games/speed-round' },
  { id: 'word-match', title: 'Word Match', description: 'Match words with their translations', icon: Link2, gradient: 'from-cyan-500/10 to-teal-500/5', iconGradient: 'from-cyan-500 to-teal-500', route: '/games/word-match' },
  { id: 'word-context', title: 'Word Context', description: 'Guess words from context clues', icon: FileText, gradient: 'from-violet-500/10 to-purple-500/5', iconGradient: 'from-violet-500 to-purple-500', route: '/games/word-context' },
  { id: 'story-builder', title: 'Story Builder', description: 'Create stories with target vocabulary', icon: Pencil, gradient: 'from-rose-500/10 to-pink-500/5', iconGradient: 'from-rose-500 to-pink-500', route: '/games/story-builder' },
  { id: 'listening', title: 'Listening', description: 'Identify words from audio pronunciation', icon: Headphones, gradient: 'from-indigo-500/10 to-blue-500/5', iconGradient: 'from-indigo-500 to-blue-500', route: '/games/listening' },
  { id: 'synonym-antonym', title: 'Synonym & Antonym', description: 'Find synonyms and antonyms of words', icon: ArrowLeftRight, gradient: 'from-emerald-500/10 to-green-500/5', iconGradient: 'from-emerald-500 to-green-500', route: '/games/synonym-antonym' },
  { id: 'irregular-verbs', title: 'Irregular Verbs', description: 'Practice past simple & past participle forms', icon: BookType, gradient: 'from-orange-500/10 to-red-500/5', iconGradient: 'from-orange-500 to-red-500', route: '/games/irregular-verbs' },
];

export default function GamesPage() {
  return (
    <PageTransition>
      <div className="space-y-8">
        <PageHeader title="Games" description="Learn through play with 8 fun game modes" icon={Gamepad2} />
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 lg:gap-6">
          {GAMES.map((game) => (
            <GameCard key={game.id} {...game} />
          ))}
        </div>
      </div>
    </PageTransition>
  );
}
