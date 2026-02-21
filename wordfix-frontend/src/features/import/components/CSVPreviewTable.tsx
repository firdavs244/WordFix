interface CSVPreviewTableProps {
  headers: string[];
  rows: Array<Record<string, string>>;
}

export default function CSVPreviewTable({ headers, rows }: CSVPreviewTableProps) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="bg-muted/30">
            {headers.map((h) => (
              <th key={h} className="px-4 py-2 text-left text-[10px] font-medium uppercase tracking-wide text-muted-foreground">
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className={i % 2 === 1 ? 'bg-muted/10' : ''}>
              {headers.map((h) => (
                <td key={h} className="px-4 py-2 text-sm">{row[h] || ''}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
