export default function CalendarLegend() {
  const levels = ['bg-muted/50', 'bg-emerald-200/60', 'bg-emerald-300/70', 'bg-emerald-400/80', 'bg-emerald-500'];
  return (
    <div className="mt-3 flex items-center justify-end gap-1.5">
      <span className="text-[8px] text-muted-foreground/40">Less</span>
      {levels.map((c, i) => (
        <div key={i} className={`h-2.5 w-2.5 rounded-sm ${c}`} />
      ))}
      <span className="text-[8px] text-muted-foreground/40">More</span>
    </div>
  );
}
