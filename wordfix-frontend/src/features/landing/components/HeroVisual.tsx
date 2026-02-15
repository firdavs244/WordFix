export function HeroVisual() {
  return (
    <div className="relative h-[500px] w-full">
      {/* Main flashcard */}
      <div
        className="absolute left-1/4 top-1/4 z-20 h-40 w-64 animate-float rounded-2xl border border-border/30 bg-card p-6 shadow-xl"
        style={{ transform: 'perspective(800px) rotateY(-8deg) rotateX(4deg)' }}
      >
        <p className="font-heading text-xl font-bold">Serendipity</p>
        <p className="mt-2 text-sm text-muted-foreground">tasodifiy yoqimli kashfiyot</p>
        <div className="mt-4 flex items-center gap-2">
          <div className="h-1.5 w-16 rounded-full bg-primary/30" />
          <span className="text-[10px] text-muted-foreground">B2 Level</span>
        </div>
      </div>

      {/* Streak card */}
      <div
        className="absolute left-4 top-8 z-10 h-32 w-48 animate-float rounded-xl border border-border/20 bg-card p-4 opacity-80 shadow-lg"
        style={{ transform: 'rotateY(5deg) rotateZ(-3deg)', animationDelay: '-1.5s' }}
      >
        <p className="text-2xl">🔥</p>
        <p className="mt-1 font-heading text-lg font-bold">12 Day Streak</p>
        <p className="text-xs text-muted-foreground">Keep it up!</p>
      </div>

      {/* Achievement badge */}
      <div
        className="absolute bottom-16 right-4 z-10 h-28 w-44 animate-float rounded-xl border border-border/20 bg-card p-4 opacity-70 shadow-lg"
        style={{ transform: 'rotateY(-5deg) rotateZ(2deg)', animationDelay: '-3s' }}
      >
        <p className="text-2xl">🏆</p>
        <p className="mt-1 font-heading text-sm font-semibold">Word Master</p>
        <p className="text-[10px] text-muted-foreground">100 words learned</p>
      </div>

      {/* XP notification */}
      <div
        className="absolute right-16 top-16 z-30 animate-float rounded-full border border-accent/20 bg-accent/10 px-4 py-2"
        style={{ animationDuration: '2.5s' }}
      >
        <span className="text-sm font-semibold text-accent">+25 XP</span>
      </div>
    </div>
  );
}
