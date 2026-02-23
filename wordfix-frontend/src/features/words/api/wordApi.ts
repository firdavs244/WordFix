import apiClient from '@/api/client';
import type {
  ApiResponse,
  BulkWordCreateData,
  Word,
  WordCategory,
  WordCreateData,
  WordFilters,
  WordStats,
  WordUpdateData,
} from '@/types';

// ─── Words API ─────────────────────────────────────────────────────────────────

export const wordsApi = {
  list: async (filters?: WordFilters) => {
    const params = new URLSearchParams();
    if (filters) {
      if (filters.difficulty_level) params.set('difficulty_level', filters.difficulty_level);
      if (filters.category_id) params.set('category_id', filters.category_id);
      if (filters.is_mastered !== undefined) params.set('is_mastered', String(filters.is_mastered));
      if (filters.part_of_speech) params.set('part_of_speech', filters.part_of_speech);
      if (filters.search) params.set('search', filters.search);
      if (filters.ordering) params.set('ordering', filters.ordering);
      if (filters.page) params.set('page', String(filters.page));
      if (filters.page_size) params.set('page_size', String(filters.page_size));
    }
    const qs = params.toString();
    const res = await apiClient.get<ApiResponse<Word[]>>(
      qs ? `/words/?${qs}` : '/words/',
    );
    return res.data;
  },

  getById: async (id: string) => {
    const res = await apiClient.get<ApiResponse<Word>>(`/words/${id}/`);
    return res.data;
  },

  create: async (data: WordCreateData) => {
    const res = await apiClient.post<ApiResponse<Word>>('/words/', data);
    return res.data;
  },

  update: async (id: string, data: WordUpdateData) => {
    const res = await apiClient.patch<ApiResponse<Word>>(
      `/words/${id}/`,
      data,
    );
    return res.data;
  },

  delete: async (id: string) => {
    await apiClient.delete(`/words/${id}/`);
  },

  bulkCreate: async (data: BulkWordCreateData) => {
    const res = await apiClient.post<
      ApiResponse<{ created: number; skipped: number; errors: unknown[] }>
    >('/words/bulk/', data);
    return res.data;
  },

  getStats: async () => {
    const res = await apiClient.get<ApiResponse<WordStats>>('/words/stats/');
    return res.data;
  },

  getReviewWords: async () => {
    const res = await apiClient.get<ApiResponse<Word[]>>('/words/review/');
    return res.data;
  },

  // ─── Categories ────────────────────────────────────────────────────────────

  listCategories: async () => {
    const res = await apiClient.get<ApiResponse<WordCategory[]>>(
      '/words/categories/',
    );
    return res.data;
  },

  createCategory: async (data: { name: string; color?: string; icon?: string }) => {
    const res = await apiClient.post<ApiResponse<WordCategory>>(
      '/words/categories/',
      data,
    );
    return res.data;
  },

  deleteCategory: async (id: string) => {
    await apiClient.delete(`/words/categories/${id}/`);
  },

  // ─── Archive ─────────────────────────────────────────────────────────────

  archiveWord: async (id: string) => {
    const res = await apiClient.post<ApiResponse<{ id: string; is_archived: boolean }>>(
      `/words/${id}/archive/`,
    );
    return res.data;
  },

  unarchiveWord: async (id: string) => {
    const res = await apiClient.post<ApiResponse<{ id: string; is_archived: boolean }>>(
      `/words/${id}/unarchive/`,
    );
    return res.data;
  },

  getArchivedWords: async (params?: { page?: number; page_size?: number }) => {
    const qs = new URLSearchParams();
    if (params?.page) qs.set('page', String(params.page));
    if (params?.page_size) qs.set('page_size', String(params.page_size));
    const query = qs.toString();
    const res = await apiClient.get<ApiResponse<Word[]>>(
      query ? `/words/archived/?${query}` : '/words/archived/',
    );
    return res.data;
  },

  bulkArchiveWords: async (wordIds: string[]) => {
    const res = await apiClient.post<ApiResponse<{ archived_count: number }>>(
      '/words/archive/bulk/',
      { word_ids: wordIds },
    );
    return res.data;
  },

  // ─── Enrichment ──────────────────────────────────────────────────────────

  enrichWord: async (id: string) => {
    const res = await apiClient.post<ApiResponse<unknown>>(`/words/${id}/enrich/`);
    return res.data;
  },

  enrichAll: async () => {
    const res = await apiClient.post<ApiResponse<unknown>>('/words/enrich-all/');
    return res.data;
  },
};
