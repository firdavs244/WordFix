import { create } from 'zustand';
import { authApi } from '@/features/auth/api/authApi';
import type { User, LoginCredentials, RegisterData } from '@/types';
import { toast } from 'sonner';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: User | null) => void;
  setLoading: (loading: boolean) => void;
  login: (credentials: LoginCredentials) => Promise<{ has_completed_onboarding: boolean }>;
  register: (data: RegisterData) => Promise<void>;
  googleLogin: (credential: string) => Promise<{ has_completed_onboarding: boolean; is_new_user: boolean }>;
  logout: () => Promise<void>;
  fetchProfile: () => Promise<void>;
  initialize: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  setUser: (user) =>
    set({ user, isAuthenticated: !!user, isLoading: false }),

  setLoading: (isLoading) => set({ isLoading }),

  login: async (credentials) => {
    const response = await authApi.login(credentials);
    const { user, tokens } = response.data;
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    set({ user, isAuthenticated: true, isLoading: false });
    toast.success('Welcome back!');
    return { has_completed_onboarding: user.has_completed_onboarding };
  },

  register: async (data) => {
    const response = await authApi.register(data);
    const { user, tokens } = response.data;
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    set({ user, isAuthenticated: true, isLoading: false });
    toast.success('Account created successfully!');
  },

  googleLogin: async (credential: string) => {
    const response = await authApi.googleLogin({ id_token: credential });
    const { user, tokens, is_new_user } = response.data;
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    set({ user, isAuthenticated: true, isLoading: false });
    toast.success(is_new_user ? 'Welcome to WordFix!' : 'Welcome back!');
    return { has_completed_onboarding: user.has_completed_onboarding, is_new_user };
  },

  logout: async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    try {
      if (refreshToken) {
        await authApi.logout(refreshToken);
      }
    } catch {
      // Ignore logout API errors
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({ user: null, isAuthenticated: false, isLoading: false });
      toast.success('Logged out successfully.');
    }
  },

  fetchProfile: async () => {
    try {
      const response = await authApi.getProfile();
      set({ user: response.data, isAuthenticated: true, isLoading: false });
    } catch {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  },

  initialize: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ isLoading: false });
      return;
    }
    await get().fetchProfile();
  },
}));
