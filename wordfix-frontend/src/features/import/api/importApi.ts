import apiClient from '@/api/client';
import API_ENDPOINTS from '@/api/endpoints';
import type {
  AnalyzeTextRequest,
  AnalyzeTextResponse,
  ApiResponse,
  CSVImportResult,
  CSVValidateResult,
  ImportWordsRequest,
  ImportWordsResponse,
} from '@/types';

export const importApi = {
  analyzeText: async (data: AnalyzeTextRequest) => {
    const res = await apiClient.post<ApiResponse<AnalyzeTextResponse>>(
      API_ENDPOINTS.IMPORT.ANALYZE,
      data,
    );
    return res.data;
  },

  addWords: async (data: ImportWordsRequest) => {
    const res = await apiClient.post<ApiResponse<ImportWordsResponse>>(
      API_ENDPOINTS.IMPORT.ADD,
      data,
    );
    return res.data;
  },

  validateCSV: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<ApiResponse<CSVValidateResult>>(
      API_ENDPOINTS.IMPORT.CSV_VALIDATE,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data;
  },

  importCSV: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<ApiResponse<CSVImportResult>>(
      API_ENDPOINTS.IMPORT.CSV_IMPORT,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } },
    );
    return res.data;
  },
};
