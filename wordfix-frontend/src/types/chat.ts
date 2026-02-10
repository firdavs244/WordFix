// ─── AI Chat Types ─────────────────────────────────────────────────────────────

export interface ChatSession {
  id: string;
  topic: string;
  started_at: string;
  ended_at: string | null;
  message_count: number;
  target_words: string[];
  words_practiced: string[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: string;
  session_id: string;
  role: 'user' | 'assistant';
  content: string;
  corrections: ChatCorrection[];
  words_used: string[];
  order: number;
  created_at: string;
}

export interface ChatCorrection {
  original: string;
  corrected: string;
  explanation: string;
}

export interface StartChatRequest {
  topic?: string;
}

export interface StartChatResponse {
  session_id: string;
  topic: string;
  target_words: string[];
  first_message: {
    role: string;
    content: string;
    corrections: ChatCorrection[];
    words_used: string[];
  };
}

export interface SendMessageRequest {
  message: string;
}

export interface SendMessageResponse {
  ai_message: string;
  corrections: ChatCorrection[];
  words_used: string[];
  encouragement: string;
  xp_earned: number;
}

export interface ChatSessionListResponse {
  sessions: ChatSession[];
}

export interface ChatSessionDetailResponse {
  session: ChatSession;
  messages: ChatMessage[];
}
