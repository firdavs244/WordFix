import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  ApiResponse,
  AuthTokens,
  ChangePasswordData,
  LoginCredentials,
  RegisterData,
  UpdateProfileData,
  User,
} from '@/types';

// ─── Auth API ──────────────────────────────────────────────────────────────────

export const authApi = {
  register: async (data: RegisterData) => {
    const res = await apiClient.post<ApiResponse<{ user: User; tokens: AuthTokens }>>(
      API_ENDPOINTS.AUTH.REGISTER,
      data,
    );
    return res.data;
  },

  login: async (credentials: LoginCredentials) => {
    const res = await apiClient.post<ApiResponse<{ user: User; tokens: AuthTokens }>>(
      API_ENDPOINTS.AUTH.LOGIN,
      credentials,
    );
    return res.data;
  },

  logout: async (refreshToken: string) => {
    const res = await apiClient.post<ApiResponse>(API_ENDPOINTS.AUTH.LOGOUT, {
      refresh: refreshToken,
    });
    return res.data;
  },

  refreshToken: async (refreshToken: string) => {
    const res = await apiClient.post<ApiResponse<{ access: string }>>(
      API_ENDPOINTS.AUTH.REFRESH,
      { refresh: refreshToken },
    );
    return res.data;
  },

  getProfile: async () => {
    const res = await apiClient.get<ApiResponse<User>>(API_ENDPOINTS.AUTH.PROFILE);
    return res.data;
  },

  updateProfile: async (data: UpdateProfileData) => {
    const res = await apiClient.patch<ApiResponse<User>>(
      API_ENDPOINTS.AUTH.PROFILE,
      data,
    );
    return res.data;
  },

  changePassword: async (data: ChangePasswordData) => {
    const res = await apiClient.post<ApiResponse>(
      API_ENDPOINTS.AUTH.CHANGE_PASSWORD,
      data,
    );
    return res.data;
  },
};
