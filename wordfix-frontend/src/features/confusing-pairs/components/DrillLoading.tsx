export default function DrillLoading() {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12">
      <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      <p className="text-muted-foreground">Generating drill...</p>
    </div>
  );
}
