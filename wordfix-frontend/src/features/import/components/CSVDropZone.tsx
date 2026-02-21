import { useRef, useState } from 'react';
import { Upload, FileSpreadsheet } from 'lucide-react';
import { cn } from '@/lib/utils';

interface CSVDropZoneProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
}

export default function CSVDropZone({ onFileSelect, selectedFile }: CSVDropZoneProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.name.endsWith('.csv')) onFileSelect(file);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) onFileSelect(file);
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={cn(
        'flex h-48 cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed bg-muted/20 transition-all duration-200',
        dragOver ? 'scale-[1.01] border-primary bg-primary/[0.05]' : 'border-border/50 hover:border-primary/30 hover:bg-primary/[0.02]',
      )}
    >
      <input ref={inputRef} type="file" accept=".csv" onChange={handleChange} className="hidden" />
      {selectedFile ? (
        <>
          <FileSpreadsheet className="h-8 w-8 text-primary" />
          <p className="mt-2 text-sm font-medium">{selectedFile.name}</p>
          <p className="text-xs text-muted-foreground">{(selectedFile.size / 1024).toFixed(1)} KB</p>
          <span className="mt-1 text-xs text-primary">Change file</span>
        </>
      ) : (
        <>
          <Upload className="h-10 w-10 text-muted-foreground/30" />
          <p className="mt-3 text-sm font-medium">Drag & drop your CSV file here</p>
          <p className="mt-1 text-xs text-muted-foreground/40">or</p>
          <span className="text-sm font-medium text-primary underline underline-offset-4">Browse Files</span>
          <p className="mt-2 text-[10px] text-muted-foreground/30">.csv format</p>
        </>
      )}
    </div>
  );
}
