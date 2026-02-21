interface Props {
  label: string;
  isActive: boolean;
}

export function OptimalDayIndicator({ label, isActive }: Props) {
  return (
    <div
      className={`flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium transition-colors ${
        isActive
          ? 'bg-primary text-primary-foreground'
          : 'bg-muted text-muted-foreground'
      }`}
    >
      {label}
    </div>
  );
}
