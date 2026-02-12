import { motion } from 'framer-motion';
import { AlertCircle, Check, FileSpreadsheet } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import type { CSVValidateResult } from '@/types/smart-import';

interface CSVPreviewProps {
  result: CSVValidateResult;
  file: File;
  onImport: () => void;
  onCancel: () => void;
  isImporting: boolean;
}

export function CSVPreview({ result, file, onImport, onCancel, isImporting }: CSVPreviewProps) {
  const hasErrors = result.errors && result.errors.length > 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-4"
    >
      {/* File info */}
      <div className="flex items-center gap-3 rounded-lg border bg-muted/30 p-3">
        <FileSpreadsheet className="h-5 w-5 text-primary" />
        <div className="flex-1">
          <p className="text-sm font-medium">{file.name}</p>
          <p className="text-xs text-muted-foreground">
            {result.total_rows} rows &middot; {result.valid_rows} valid &middot;{' '}
            {result.headers.length} columns
          </p>
        </div>
        <div className="flex gap-1">
          {result.has_translation && <Badge variant="outline">Translation</Badge>}
          {result.has_difficulty && <Badge variant="outline">Difficulty</Badge>}
          {result.has_category && <Badge variant="outline">Category</Badge>}
        </div>
      </div>

      {/* Preview table */}
      <div className="overflow-hidden rounded-lg border">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b bg-muted/50">
                {result.headers.map((header) => (
                  <th key={header} className="px-4 py-2 text-left font-medium text-muted-foreground">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.preview.map((row, i) => (
                <tr key={i} className="border-b last:border-b-0 hover:bg-muted/20">
                  {result.headers.map((header) => (
                    <td key={header} className="max-w-[200px] truncate px-4 py-2 text-foreground">
                      {row[header] || '—'}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {result.total_rows > result.preview.length && (
          <div className="border-t bg-muted/20 px-4 py-2 text-center text-xs text-muted-foreground">
            Showing {result.preview.length} of {result.total_rows} rows
          </div>
        )}
      </div>

      {/* Errors */}
      {hasErrors && (
        <div className="rounded-lg border border-destructive/30 bg-destructive/5 p-3 space-y-1">
          <div className="flex items-center gap-2 text-sm font-medium text-destructive">
            <AlertCircle className="h-4 w-4" />
            {result.errors!.length} validation issue{result.errors!.length > 1 ? 's' : ''}
          </div>
          <ul className="space-y-0.5">
            {result.errors!.slice(0, 5).map((err, i) => (
              <li key={i} className="text-xs text-destructive/80">
                &bull; {err}
              </li>
            ))}
            {result.errors!.length > 5 && (
              <li className="text-xs text-muted-foreground">
                &hellip; and {result.errors!.length - 5} more
              </li>
            )}
          </ul>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center justify-between pt-2">
        <Button variant="outline" onClick={onCancel}>
          Cancel
        </Button>
        <Button onClick={onImport} disabled={isImporting || result.valid_rows === 0}>
          {isImporting ? (
            <>
              <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Importing...
            </>
          ) : (
            <>
              <Check className="mr-2 h-4 w-4" />
              Import {result.valid_rows} Words
            </>
          )}
        </Button>
      </div>
    </motion.div>
  );
}
