// ─── Confusing Pairs Types ─────────────────────────────────────────────────────

export interface ConfusingPairWord {
  id: string;
  original_word: string;
  translation: string;
}

export interface ConfusingPair {
  id: string;
  word_1: ConfusingPairWord;
  word_2: ConfusingPairWord;
  confusion_count: number;
  last_confused_at: string;
  is_resolved: boolean;
}

export interface DrillExample {
  sentence: string;
  translation: string;
}

export interface DrillQuestion {
  sentence: string;
  correct_answer: string;
  wrong_answer: string;
  explanation: string;
}

export interface DrillData {
  explanation: string;
  word_1_examples: DrillExample[];
  word_2_examples: DrillExample[];
  mnemonic: string;
  test_questions: DrillQuestion[];
}

export interface ConfusingPairsCountResponse {
  count: number;
}
