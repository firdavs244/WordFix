/**
 * TypeScript types for the Immersive Language Learning Game.
 */

export interface ImmersiveScenario {
  id: string;
  name: string;
  name_uz: string;
  description: string;
  description_uz: string;
  location: string;
  difficulty: string;
  max_turns: number;
  time_limit_seconds: number;
  xp_reward: number;
  scene_config: SceneConfig;
  npcs?: NPCCharacter[];
  target_vocabulary?: string[];
}

export interface SceneConfig {
  environment: string;
  camera_position: [number, number, number];
  ambient_light: number;
  objects: string[];
}

export interface NPCCharacter {
  id: string;
  name: string;
  role: string;
  role_uz: string;
  avatar_config: Record<string, string>;
  initial_greeting?: string;
}

export interface ConversationTurn {
  turn_number: number;
  role: 'npc' | 'user';
  content: string;
  audio_url?: string;
  input_type?: string;
  grammar_errors: GrammarError[];
  vocabulary_feedback: VocabFeedback[];
  score: number;
  hint_level_used: number;
}

export interface GrammarError {
  original: string;
  corrected: string;
  explanation: string;
  explanation_uz: string;
}

export interface VocabFeedback {
  word: string;
  feedback: string;
  feedback_uz: string;
}

export interface ImmersiveSessionStart {
  session_id: string;
  scenario: {
    id: string;
    name: string;
    name_uz: string;
    location: string;
    difficulty: string;
    scene_config: SceneConfig;
    max_turns: number;
    time_limit_seconds: number;
  };
  npc: NPCCharacter;
  first_turn: ConversationTurn;
}

export interface SubmitResponseResult {
  user_analysis: {
    grammar_errors: GrammarError[];
    vocabulary_feedback: VocabFeedback[];
    relevance_score: number;
    grammar_score: number;
    vocabulary_score: number;
    score: number;
  };
  npc_response: {
    content: string;
    audio_url: string;
  } | null;
  session_stats: {
    turn_count: number;
    max_turns: number;
    is_last_turn: boolean;
  };
  transcribed_text?: string;
}

export interface HintResponse {
  level: number;
  hint: string;
  hint_uz: string;
  score_penalty: number;
  hints_remaining: number;
}

export interface SessionCompleteResult {
  session_id: string;
  status: string;
  total_score: number;
  fluency_score: number;
  accuracy_score: number;
  vocabulary_score: number;
  task_completion_score: number;
  duration_seconds: number;
  turn_count: number;
  hints_used: number;
  xp_earned: number;
  badges_earned: { code: string; name: string; icon: string }[];
}
