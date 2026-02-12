import type { ProficiencyLevel } from './core';

// ─── User Types ────────────────────────────────────────────────────────────────

export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  avatar: string;
  native_language: string;
  learning_language: string;
  proficiency_level: ProficiencyLevel;
  daily_goal: number;
  timezone: string;
  is_premium: boolean;
  premium_until: string | null;
  is_premium_active: boolean;
  is_active: boolean;
  date_joined: string;
  last_login: string | null;
  has_completed_onboarding: boolean;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  full_name?: string;
}

export interface ChangePasswordData {
  old_password: string;
  new_password: string;
  new_password_confirm: string;
}

export interface UpdateProfileData {
  full_name?: string;
  native_language?: string;
  learning_language?: string;
  proficiency_level?: ProficiencyLevel;
  daily_goal?: number;
  timezone?: string;
}
