import { useState, useCallback } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { importApi } from '../api/importApi';
import { toast } from 'sonner';
import type { CSVValidateResult, CSVImportResult } from '@/types';

export function useCSVImport() {
  const queryClient = useQueryClient();
  const [file, setFile] = useState<File | null>(null);
  const [previewData, setPreviewData] = useState<CSVValidateResult | null>(null);
  const [result, setResult] = useState<CSVImportResult | null>(null);

  const validateMutation = useMutation({
    mutationFn: (f: File) => importApi.validateCSV(f),
    onSuccess: (res) => setPreviewData(res.data),
    onError: () => toast.error('Failed to validate CSV'),
  });

  const importMutation = useMutation({
    mutationFn: () => importApi.importCSV(file!),
    onSuccess: (res) => {
      setResult(res.data);
      queryClient.invalidateQueries({ queryKey: ['words'] });
      toast.success(`Imported ${res.data.imported} words!`);
    },
    onError: () => toast.error('Failed to import CSV'),
  });

  const validate = useCallback(async (f: File) => {
    setFile(f);
    await validateMutation.mutateAsync(f);
  }, [validateMutation]);

  const importFile = useCallback(() => importMutation.mutateAsync(), [importMutation]);

  const reset = useCallback(() => {
    setFile(null);
    setPreviewData(null);
    setResult(null);
  }, []);

  return {
    file, previewData, result,
    isValidating: validateMutation.isPending,
    isImporting: importMutation.isPending,
    validate, importFile, reset,
  };
}
