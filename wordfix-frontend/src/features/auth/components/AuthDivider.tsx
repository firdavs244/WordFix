export function AuthDivider() {
  return (
    <div className="my-6 flex items-center gap-3">
      <div className="h-px flex-1 bg-border/40" />
      <span className="text-xs text-muted-foreground/50">or</span>
      <div className="h-px flex-1 bg-border/40" />
    </div>
  );
}
