export function FloatingShapes() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute -left-16 -top-16 h-72 w-72 animate-float rounded-full bg-gradient-to-br from-primary/10 to-primary/5 blur-3xl" />
      <div
        className="absolute -bottom-20 -right-12 h-64 w-64 animate-float rounded-3xl bg-gradient-to-br from-secondary/10 to-secondary/5 blur-3xl"
        style={{ animationDelay: '-2s', animationDuration: '8s' }}
      />
      <div
        className="absolute left-1/3 top-1/4 h-48 w-48 animate-float rounded-full bg-gradient-to-br from-accent/8 to-accent/3 blur-2xl"
        style={{ animationDelay: '-4s', animationDuration: '10s' }}
      />
      <div
        className="absolute bottom-1/3 right-1/4 h-32 w-32 animate-float rounded-full bg-gradient-to-br from-primary/6 to-secondary/4 blur-2xl"
        style={{ animationDelay: '-1s', animationDuration: '7s' }}
      />
      <div
        className="absolute right-1/3 top-2/3 h-24 w-24 animate-float rounded-3xl bg-gradient-to-br from-accent/6 to-primary/4 blur-xl"
        style={{ animationDelay: '-3s', animationDuration: '9s' }}
      />
    </div>
  );
}
