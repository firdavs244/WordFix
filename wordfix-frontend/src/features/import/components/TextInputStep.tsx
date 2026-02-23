import { useState, useCallback, useRef } from 'react';
import { Upload, FileText, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { toast } from 'sonner';

interface TextInputStepProps {
  text: string;
  onChange: (text: string) => void;
}

export default function TextInputStep({ text, onChange }: TextInputStepProps) {
  const count = text.length;
  const [isDragOver, setIsDragOver] = useState(false);
  const [fileName, setFileName] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback((file: File) => {
    if (!file.name.endsWith('.txt') && file.type !== 'text/plain') {
      toast.error('Only .txt files are supported');
      return;
    }
    if (file.size > 50000) {
      toast.error('File too large (max 50KB)');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      const content = (e.target?.result as string) ?? '';
      onChange(content.slice(0, 5000));
      setFileName(file.name);
      toast.success(`Loaded "${file.name}"`);
    };
    reader.onerror = () => toast.error('Failed to read file');
    reader.readAsText(file);
  }, [onChange]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  }, [handleFile]);

  const clearFile = () => {
    setFileName(null);
    onChange('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="rounded-2xl border border-border/50 p-6 shadow-card space-y-4">
      {/* Drop zone / file picker */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={cn(
          'flex cursor-pointer flex-col items-center gap-2 rounded-xl border-2 border-dashed py-6 transition-all',
          isDragOver
            ? 'border-primary bg-primary/5 scale-[1.01]'
            : 'border-border/40 bg-muted/10 hover:border-primary/30 hover:bg-muted/20'
        )}
      >
        <Upload className={cn('h-6 w-6', isDragOver ? 'text-primary' : 'text-muted-foreground')} />
        <div className="text-center">
          <p className="text-sm font-medium">
            {isDragOver ? 'Drop file here' : 'Drag & drop a .txt file'}
          </p>
          <p className="text-xs text-muted-foreground">or click to browse</p>
        </div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt,text/plain"
          className="hidden"
          onChange={handleFileInput}
        />
      </div>

      {/* File indicator */}
      {fileName && (
        <div className="flex items-center gap-2 rounded-lg bg-primary/5 px-3 py-2">
          <FileText className="h-4 w-4 text-primary" />
          <span className="flex-1 truncate text-xs font-medium">{fileName}</span>
          <button onClick={clearFile} className="text-muted-foreground hover:text-foreground">
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      )}

      {/* Divider */}
      <div className="flex items-center gap-2">
        <div className="flex-1 border-t border-border/30" />
        <span className="text-[10px] text-muted-foreground">or paste text</span>
        <div className="flex-1 border-t border-border/30" />
      </div>

      {/* Textarea */}
      <textarea
        value={text}
        onChange={(e) => { onChange(e.target.value.slice(0, 5000)); setFileName(null); }}
        placeholder="Paste your English text here... Articles, stories, or any content with words you want to learn."
        className="h-48 w-full resize-none rounded-xl border border-border/50 bg-background px-4 py-3 text-sm leading-relaxed transition-all placeholder:text-muted-foreground/40 focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10"
      />
      <div className="flex items-center justify-between">
        <span
          className={cn(
            'text-xs',
            count >= 5000 ? 'text-destructive' : count >= 4500 ? 'text-warning' : 'text-muted-foreground',
          )}
        >
          {count}/5000
        </span>
      </div>
    </div>
  );
}
