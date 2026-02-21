interface BadgeIconProps {
  earned: boolean;
}

export default function BadgeIcon({ earned }: BadgeIconProps) {
  return (
    <div className="flex h-11 w-11 items-center justify-center">
      {earned ? (
        <span className="text-3xl" role="img" aria-label="trophy">🏆</span>
      ) : (
        <span className="text-2xl grayscale" role="img" aria-label="locked">🔒</span>
      )}
    </div>
  );
}
