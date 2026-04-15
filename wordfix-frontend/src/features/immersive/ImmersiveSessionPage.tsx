/**
 * Immersive Game — Main 3D session page with conversation.
 * Sprint 15 — Enterprise-grade: animations, ErrorBoundary, ARIA, AudioPlayer, ErrorHighlight, HintPanel.
 */

import { useState, useRef, useEffect, Suspense, lazy } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Send, ChevronUp, ChevronDown, Loader2 } from 'lucide-react';
import ErrorBoundary from '@/components/shared/ErrorBoundary';
import { pageTransition, slideInLeft, slideInRight, fadeInUp, staggerContainer, bounceIn, floatUp } from '@/lib/motion';
import type { ConversationTurn } from './types/immersive';
import { useVoiceRecorder } from './hooks/useVoiceRecorder';
import AudioPlayer from './components/conversation/AudioPlayer';
import ErrorHighlight from './components/feedback/ErrorHighlight';
import HintPanel from './components/feedback/HintPanel';

const ImmersiveScene = lazy(() => import('./components/scene/ImmersiveScene'));

interface Props {
  session: ReturnType<typeof import('./hooks/useImmersiveSession').useImmersiveSession>;
}

/** Skeleton for the 3D scene while Three.js loads */
function SceneSkeleton() {
  return (
    <div className="flex h-full items-center justify-center bg-gradient-to-b from-gray-100 to-gray-200 dark:from-gray-900 dark:to-gray-800">
      <div className="text-center">
        <div className="mx-auto mb-3 h-10 w-10 animate-spin rounded-full border-4 border-indigo-500 border-t-transparent" />
        <p className="text-sm font-medium text-gray-500">Loading 3D scene...</p>
      </div>
    </div>
  );
}

/** Skeleton for conversation panel before session data loads */
function ConversationSkeleton() {
  return (
    <div className="flex flex-1 flex-col p-4 space-y-3 animate-pulse">
      <div className="flex items-center gap-2 pb-3 border-b border-gray-200 dark:border-gray-700">
        <div className="h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-700" />
        <div className="space-y-1">
          <div className="h-3 w-24 rounded bg-gray-200 dark:bg-gray-700" />
          <div className="h-2 w-16 rounded bg-gray-200 dark:bg-gray-700" />
        </div>
      </div>
      <div className="flex justify-start">
        <div className="h-12 w-64 rounded-2xl bg-gray-200 dark:bg-gray-700" />
      </div>
      <div className="flex justify-start">
        <div className="h-8 w-48 rounded-2xl bg-gray-200 dark:bg-gray-700" />
      </div>
    </div>
  );
}

export function ImmersiveSessionPage({ session }: Props) {
  const [inputText, setInputText] = useState('');
  const [showScene, setShowScene] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const voiceRecorder = useVoiceRecorder();
  const [, setTurnStartTime] = useState<number>(Date.now());

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [session.turns]);

  // Focus input after NPC responds
  useEffect(() => {
    if (!session.isResponding) {
      inputRef.current?.focus();
      setTurnStartTime(Date.now());
    }
  }, [session.isResponding]);

  const handleSendText = () => {
    if (!inputText.trim() || session.isResponding) return;
    session.addUserMessage(inputText);
    session.respond(inputText);
    setInputText('');
  };

  const handleVoiceStop = async () => {
    try {
      const blob = await voiceRecorder.stopRecording();
      session.respondVoice(blob);
    } catch {
      voiceRecorder.reset();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendText();
    }
  };

  const scenarioData = session.sessionData?.scenario;
  const npcData = session.sessionData?.npc;

  return (
    <motion.div {...pageTransition} className="flex h-[calc(100vh-4rem)] flex-col">
      {/* Top Bar */}
      <div
        role="status"
        aria-live="polite"
        aria-label="Session progress"
        className="flex items-center justify-between border-b border-gray-200 bg-white px-4 py-2 dark:border-gray-700 dark:bg-gray-800"
      >
        <div className="flex items-center gap-4">
          <motion.span
            key={session.totalScore}
            {...bounceIn}
            className="text-sm font-medium text-gray-700 dark:text-gray-300"
            aria-label={`Score: ${session.totalScore}`}
          >
            Score: {session.totalScore}
          </motion.span>
          <span className="text-sm text-gray-500" aria-label={`Turn ${session.turnCount} of ${session.maxTurns}`}>
            Turn {session.turnCount}/{session.maxTurns}
          </span>
          <span className="text-sm text-gray-500" aria-label={`${session.hintsUsed} of 3 hints used`}>
            Hints: {session.hintsUsed}/3
          </span>
        </div>
        <div className="flex items-center gap-2">
          <span className="rounded-full bg-indigo-100 px-2 py-0.5 text-xs font-medium text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300">
            {scenarioData?.difficulty}
          </span>
          <span className="hidden text-sm text-gray-500 sm:inline">{scenarioData?.name}</span>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* 3D Scene — Desktop: always visible, Mobile: toggle */}
        <div className={`border-r border-gray-200 dark:border-gray-700 ${showScene ? 'block' : 'hidden'} w-full lg:block lg:w-1/2`}>
          <ErrorBoundary>
            <Suspense fallback={<SceneSkeleton />}>
              <ImmersiveScene
                environment={scenarioData?.location || 'office'}
                sceneConfig={scenarioData?.scene_config}
                npcName={npcData?.name || 'NPC'}
              />
            </Suspense>
          </ErrorBoundary>
        </div>

        {/* Conversation Panel */}
        <ErrorBoundary>
          <div className={`flex flex-1 flex-col ${showScene ? 'hidden lg:flex' : 'flex'}`}>
            {/* Mobile 3D toggle */}
            <button
              onClick={() => setShowScene(!showScene)}
              className="flex items-center justify-center gap-1 border-b border-gray-200 py-1.5 text-xs text-gray-500 hover:bg-gray-50 lg:hidden dark:border-gray-700 dark:hover:bg-gray-800"
              aria-label={showScene ? 'Hide 3D scene' : 'Show 3D scene'}
            >
              {showScene ? <ChevronUp className="h-3 w-3" /> : <ChevronDown className="h-3 w-3" />}
              {showScene ? 'Hide Scene' : 'Show 3D Scene'}
            </button>

            {/* NPC Info */}
            <div className="border-b border-gray-200 bg-gray-50 px-4 py-2 dark:border-gray-700 dark:bg-gray-800/50">
              <div className="flex items-center gap-2">
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-indigo-500 text-sm font-medium text-white" aria-hidden="true">
                  {npcData?.name?.[0] || 'N'}
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-900 dark:text-gray-100">{npcData?.name}</p>
                  <p className="text-xs text-gray-500">{npcData?.role}</p>
                </div>
              </div>
            </div>

            {/* Chat Messages */}
            {!session.sessionData ? (
              <ConversationSkeleton />
            ) : (
              <motion.div
                {...staggerContainer}
                role="log"
                aria-live="polite"
                aria-label="Conversation"
                className="flex-1 overflow-y-auto px-4 py-3 space-y-3"
              >
                <AnimatePresence mode="popLayout">
                  {session.turns.map((turn: ConversationTurn, idx: number) => (
                    <motion.div
                      key={idx}
                      {...(turn.role === 'user' ? slideInRight : slideInLeft)}
                      className={`flex ${turn.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`max-w-[85%] space-y-1 ${turn.role === 'user' ? 'items-end' : 'items-start'}`}>
                        <div className={`rounded-2xl px-4 py-2 ${
                          turn.role === 'npc'
                            ? 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-gray-100'
                            : 'bg-indigo-500 text-white'
                        }`}>
                          <p className="text-sm leading-relaxed">{turn.content}</p>

                          {/* Score badge */}
                          {turn.role === 'user' && turn.score > 0 && (
                            <motion.span {...floatUp} className="ml-2 inline-block rounded-full bg-white/20 px-1.5 py-0.5 text-xs">
                              +{turn.score}
                            </motion.span>
                          )}
                        </div>

                        {/* NPC audio */}
                        {turn.role === 'npc' && turn.audio_url && (
                          <AudioPlayer audioUrl={turn.audio_url} autoPlay={idx === session.turns.length - 1} />
                        )}

                        {/* Grammar/vocabulary feedback for user messages */}
                        {turn.role === 'user' && (turn.grammar_errors?.length > 0 || turn.vocabulary_feedback?.length > 0) && (
                          <ErrorHighlight
                            grammarErrors={turn.grammar_errors || []}
                            vocabularyFeedback={turn.vocabulary_feedback || []}
                          />
                        )}
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>

                {/* Typing indicator */}
                <AnimatePresence>
                  {(session.isResponding || session.isRespondingVoice) && (
                    <motion.div {...fadeInUp} exit={{ opacity: 0 }} className="flex justify-start">
                      <div className="rounded-2xl bg-gray-100 px-4 py-3 dark:bg-gray-700" aria-label="NPC is typing">
                        <div className="flex gap-1">
                          <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '0ms' }} />
                          <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '150ms' }} />
                          <span className="h-2 w-2 animate-bounce rounded-full bg-gray-400" style={{ animationDelay: '300ms' }} />
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>

                {/* Hint panel */}
                <HintPanel
                  hint={session.lastHint}
                  hintsRemaining={3 - session.hintsUsed}
                  onRequestHint={() => session.requestHint()}
                  isLoading={session.isRequestingHint}
                />

                <div ref={chatEndRef} />
              </motion.div>
            )}

            {/* Input Bar */}
            {session.phase === 'playing' && (
              <motion.div
                {...fadeInUp}
                className="border-t border-gray-200 bg-white px-4 py-3 dark:border-gray-700 dark:bg-gray-800"
              >
                <div className="flex items-center gap-2">
                  {/* Voice record button */}
                  <button
                    onClick={voiceRecorder.isRecording ? handleVoiceStop : voiceRecorder.startRecording}
                    disabled={session.isResponding || session.isRespondingVoice}
                    aria-label={voiceRecorder.isRecording ? 'Stop recording' : 'Start voice recording'}
                    className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full transition-colors ${
                      voiceRecorder.isRecording
                        ? 'animate-pulse bg-red-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-400'
                    }`}
                  >
                    {voiceRecorder.isRecording ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
                  </button>

                  {/* Text input */}
                  <input
                    ref={inputRef}
                    type="text"
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={session.isResponding || session.isRespondingVoice || voiceRecorder.isRecording}
                    placeholder="Type your response..."
                    aria-label="Type your response"
                    className="flex-1 rounded-full border border-gray-300 bg-gray-50 px-4 py-2 text-sm focus:border-indigo-500 focus:outline-none dark:border-gray-600 dark:bg-gray-700 dark:text-gray-100"
                  />

                  {/* Send button */}
                  <button
                    onClick={handleSendText}
                    disabled={!inputText.trim() || session.isResponding}
                    aria-label="Send message"
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-indigo-500 text-white hover:bg-indigo-600 disabled:opacity-50"
                  >
                    <Send className="h-5 w-5" />
                  </button>
                </div>
              </motion.div>
            )}

            {/* Complete button */}
            {session.phase === 'completing' && (
              <motion.div
                {...fadeInUp}
                className="border-t border-gray-200 bg-white px-4 py-4 dark:border-gray-700 dark:bg-gray-800"
              >
                <button
                  onClick={() => session.completeSession()}
                  disabled={session.isCompleting}
                  aria-label="Complete session"
                  className="flex w-full items-center justify-center gap-2 rounded-lg bg-indigo-500 px-4 py-3 font-medium text-white hover:bg-indigo-600 disabled:opacity-50"
                >
                  {session.isCompleting ? (
                    <>
                      <Loader2 className="h-5 w-5 animate-spin" />
                      Completing...
                    </>
                  ) : (
                    'Complete Session'
                  )}
                </button>
              </motion.div>
            )}
          </div>
        </ErrorBoundary>
      </div>
    </motion.div>
  );
}
