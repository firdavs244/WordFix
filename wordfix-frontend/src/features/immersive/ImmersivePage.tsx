/**
 * Immersive Game — Scenario selection page.
 * Sprint 15 — framer-motion animations, skeleton loading, ARIA.
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Globe, Filter } from 'lucide-react';
import { pageTransition, staggerContainer, staggerItem, cardHover } from '@/lib/motion';
import { useScenarios } from './hooks/useScenarios';
import { useImmersiveSession } from './hooks/useImmersiveSession';
import { ImmersiveSessionPage } from './ImmersiveSessionPage';
import { ImmersiveResultPage } from './ImmersiveResultPage';
import type { ImmersiveScenario } from './types/immersive';

const LOCATIONS = [
  { value: '', label: 'All Locations' },
  { value: 'office', label: 'Office' },
  { value: 'restaurant', label: 'Restaurant' },
  { value: 'airport', label: 'Airport' },
  { value: 'hospital', label: 'Hospital' },
  { value: 'school', label: 'School' },
  { value: 'hotel', label: 'Hotel' },
  { value: 'shop', label: 'Shop' },
  { value: 'bank', label: 'Bank' },
  { value: 'park', label: 'Park' },
  { value: 'gym', label: 'Gym' },
];

const DIFFICULTIES = [
  { value: '', label: 'All Levels' },
  { value: 'A1', label: 'A1 — Beginner' },
  { value: 'A2', label: 'A2 — Elementary' },
  { value: 'B1', label: 'B1 — Intermediate' },
  { value: 'B2', label: 'B2 — Upper Intermediate' },
];

const DIFFICULTY_COLORS: Record<string, string> = {
  A1: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
  A2: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
  B1: 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300',
  B2: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300',
  C1: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300',
  C2: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300',
};

const LOCATION_ICONS: Record<string, string> = {
  office: '🏢', restaurant: '🍽️', airport: '✈️', hospital: '🏥',
  school: '🎓', hotel: '🏨', shop: '🛍️', bank: '🏦', park: '🌳', gym: '💪',
};

function ScenarioCardSkeleton() {
  return (
    <div className="animate-pulse rounded-xl border border-gray-200 bg-white p-5 dark:border-gray-700 dark:bg-gray-800">
      <div className="mb-3 h-10 w-10 rounded-lg bg-gray-200 dark:bg-gray-700" />
      <div className="mb-2 h-5 w-3/4 rounded bg-gray-200 dark:bg-gray-700" />
      <div className="mb-1 h-3 w-full rounded bg-gray-200 dark:bg-gray-700" />
      <div className="mb-4 h-3 w-2/3 rounded bg-gray-200 dark:bg-gray-700" />
      <div className="flex gap-2">
        <div className="h-5 w-12 rounded-full bg-gray-200 dark:bg-gray-700" />
        <div className="h-5 w-16 rounded-full bg-gray-200 dark:bg-gray-700" />
        <div className="h-5 w-14 rounded-full bg-gray-200 dark:bg-gray-700" />
      </div>
    </div>
  );
}

export default function ImmersivePage() {
  const [locationFilter, setLocationFilter] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState('');
  const { data: scenarios, isLoading } = useScenarios({
    difficulty: difficultyFilter || undefined,
    location: locationFilter || undefined,
  });

  const session = useImmersiveSession();

  if (session.phase === 'playing' || session.phase === 'completing') {
    return <ImmersiveSessionPage session={session} />;
  }

  if (session.phase === 'result' && session.result) {
    return <ImmersiveResultPage result={session.result} onBack={() => session.setPhase('selecting')} />;
  }

  return (
    <motion.div {...pageTransition} className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-100 dark:bg-indigo-900/30">
            <Globe className="h-5 w-5 text-indigo-600 dark:text-indigo-400" aria-hidden="true" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              Immersive Conversations
            </h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Practice English in realistic 3D scenarios with AI-powered NPCs
            </p>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-3">
        <Filter className="h-4 w-4 text-gray-400" aria-hidden="true" />
        <select
          value={locationFilter}
          onChange={(e) => setLocationFilter(e.target.value)}
          aria-label="Filter by location"
          className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
        >
          {LOCATIONS.map((l) => (
            <option key={l.value} value={l.value}>{l.label}</option>
          ))}
        </select>
        <select
          value={difficultyFilter}
          onChange={(e) => setDifficultyFilter(e.target.value)}
          aria-label="Filter by difficulty level"
          className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200"
        >
          {DIFFICULTIES.map((d) => (
            <option key={d.value} value={d.value}>{d.label}</option>
          ))}
        </select>
      </div>

      {/* Scenarios Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <ScenarioCardSkeleton key={i} />
          ))}
        </div>
      ) : (
        <motion.div
          {...staggerContainer}
          initial="initial"
          animate="animate"
          className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3"
        >
          {scenarios?.map((scenario: ImmersiveScenario) => (
            <motion.button
              key={scenario.id}
              variants={staggerItem}
              whileHover={cardHover.hover}
              whileTap={cardHover.tap}
              onClick={() => session.startSession({ scenarioId: scenario.id })}
              disabled={session.isStarting}
              role="article"
              aria-label={`${scenario.name} — ${scenario.difficulty} level, ${scenario.max_turns} turns, ${scenario.xp_reward} XP`}
              className="group relative overflow-hidden rounded-xl border border-gray-200 bg-white p-5 text-left transition-colors hover:border-indigo-300 dark:border-gray-700 dark:bg-gray-800 dark:hover:border-indigo-500"
            >
              {/* Location icon */}
              <div className="mb-3 text-4xl" aria-hidden="true">
                {LOCATION_ICONS[scenario.location] || '🌍'}
              </div>

              {/* Title */}
              <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                {scenario.name}
              </h3>
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
                {scenario.description}
              </p>

              {/* Badges */}
              <div className="mt-3 flex items-center gap-2">
                <span
                  className={`rounded-full px-2 py-0.5 text-xs font-medium ${DIFFICULTY_COLORS[scenario.difficulty] || 'bg-gray-100 text-gray-600'}`}
                  aria-label={`Difficulty: ${scenario.difficulty}`}
                >
                  {scenario.difficulty}
                </span>
                <span className="text-xs text-gray-400">{scenario.max_turns} turns</span>
                <span className="text-xs text-gray-400">+{scenario.xp_reward} XP</span>
              </div>

              {/* Hover accent */}
              <div className="absolute inset-x-0 bottom-0 h-1 bg-indigo-500 opacity-0 transition-opacity group-hover:opacity-100" />
            </motion.button>
          ))}
        </motion.div>
      )}

      {scenarios?.length === 0 && (
        <div className="py-12 text-center text-gray-500">
          No scenarios found. Try adjusting your filters.
        </div>
      )}
    </motion.div>
  );
}
