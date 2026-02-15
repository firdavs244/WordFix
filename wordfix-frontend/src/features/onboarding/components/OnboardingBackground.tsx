export function OnboardingBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 z-0 overflow-hidden">
      <div className="absolute left-10 top-10 h-[400px] w-[400px] animate-float rounded-full bg-primary/[0.08] blur-[100px]" />
      <div
        className="absolute bottom-20 right-10 h-[350px] w-[350px] animate-float rounded-full bg-secondary/[0.06] blur-[80px]"
        style={{ animationDelay: '-2s', animationDuration: '8s' }}
      />
      <div
        className="absolute left-1/2 top-1/2 h-[250px] w-[250px] animate-float rounded-full bg-accent/[0.05] blur-[80px]"
        style={{ animationDelay: '-4s', animationDuration: '10s' }}
      />
      <div
        className="absolute inset-0 opacity-[0.02]"
        style={{ backgroundImage: 'radial-gradient(circle, currentColor 1px, transparent 1px)', backgroundSize: '30px 30px' }}
      />
    </div>
  );
}
