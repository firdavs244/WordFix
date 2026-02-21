import { Loader2 } from 'lucide-react';
import CSVPreviewTable from './CSVPreviewTable';
import type { CSVValidateResult } from '@/types';

interface CSVPreviewProps {
  data: CSVValidateResult;
  onImport: () => void;
  isImporting: boolean;
}

export default function CSVPreview({ data, onImport, isImporting }: CSVPreviewProps) {
  return (
    <div className="overflow-hidden rounded-2xl border border-border/50 shadow-card">
      <div className="flex items-center justify-between border-b border-border/30 bg-muted/20 px-5 py-4">
        <span className="font-heading text-sm font-semibold">Preview</span>
        <span className="rounded-full bg-primary/10 px-2.5 py-1 text-xs text-primary">{data.total_rows} rows detected</span>
      </div>
      <CSVPreviewTable headers={data.headers} rows={data.preview} />
      {data.total_rows > data.preview.length && (
        <p className="px-5 py-2 text-center text-xs text-muted-foreground">...and {data.total_rows - data.preview.length} more rows</p>
      )}
      {data.errors.length > 0 && (
        <div className="border-t border-border/20 px-5 py-3">
          {data.errors.map((e, i) => (
            <p key={i} className="text-xs text-warning">{e}</p>
          ))}
        </div>
      )}
      <div className="border-t border-border/30 px-5 py-4">
        <button
          onClick={onImport}
          disabled={isImporting}
          className="flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-primary text-sm font-semibold text-white disabled:opacity-50"
        >
          {isImporting ? <><Loader2 className="h-4 w-4 animate-spin" /> Importing...</> : `Import ${data.valid_rows} Words`}
        </button>
      </div>
    </div>
  );
}
