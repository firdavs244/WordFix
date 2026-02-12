import { useState, useRef, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Upload, FileSpreadsheet, X, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface CSVDropZoneProps {
  onFileSelect: (file: File) => void;
  isLoading?: boolean;
}

const MAX_SIZE = 5 * 1024 * 1024; // 5MB

export function CSVDropZone({ onFileSelect, isLoading = false }: CSVDropZoneProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateFile = useCallback((f: File): string | null => {
    if (!f.name.endsWith('.csv')) {
      return 'Only .csv files are allowed.';
    }
    if (f.size > MAX_SIZE) {
      return 'File must be under 5 MB.';
    }
    return null;
  }, []);

  const handleFile = useCallback(
    (f: File) => {
      const err = validateFile(f);
      if (err) {
        setError(err);
        setFile(null);
        return;
      }
      setError(null);
      setFile(f);
    },
    [validateFile],
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      const f = e.dataTransfer.files[0];
      if (f) handleFile(f);
    },
    [handleFile],
  );

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) handleFile(f);
    // Reset input so re-selecting same file triggers change
    e.target.value = '';
  };

  const clearFile = () => {
    setFile(null);
    setError(null);
  };

  return (
    <div className="space-y-4">
      <motion.div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => !file && inputRef.current?.click()}
        className={cn(
          'relative flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed p-8 transition-all',
          isDragging
            ? 'border-primary bg-primary/5 scale-[1.02]'
            : file
              ? 'border-green-500 bg-green-50 dark:bg-green-950/20'
              : 'border-border hover:border-primary/50 hover:bg-muted/50',
          isLoading && 'pointer-events-none opacity-60',
        )}
        animate={isDragging ? { scale: 1.02 } : { scale: 1 }}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={handleInputChange}
          className="hidden"
        />

        {file ? (
          <div className="flex items-center gap-3">
            <FileSpreadsheet className="h-8 w-8 text-green-600 dark:text-green-400" />
            <div>
              <p className="text-sm font-medium text-foreground">{file.name}</p>
              <p className="text-xs text-muted-foreground">
                {(file.size / 1024).toFixed(1)} KB
              </p>
            </div>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={(e) => {
                e.stopPropagation();
                clearFile();
              }}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        ) : (
          <>
            <Upload className="mb-3 h-10 w-10 text-muted-foreground" />
            <p className="text-sm font-medium text-foreground">
              Drop a CSV file here or <span className="text-primary">browse</span>
            </p>
            <p className="mt-1 text-xs text-muted-foreground">
              .csv files up to 5 MB
            </p>
          </>
        )}
      </motion.div>

      {error && (
        <div className="flex items-center gap-2 text-sm text-destructive">
          <AlertCircle className="h-4 w-4" />
          {error}
        </div>
      )}

      {file && !error && (
        <Button
          className="w-full"
          onClick={() => onFileSelect(file)}
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Validating...
            </>
          ) : (
            <>
              <Upload className="mr-2 h-4 w-4" />
              Upload & Validate
            </>
          )}
        </Button>
      )}
    </div>
  );
}
