interface CustomTopicInputProps {
  value: string;
  onChange: (value: string) => void;
}

export default function CustomTopicInput({ value, onChange }: CustomTopicInputProps) {
  return (
    <div>
      <label className="mb-1 block text-[10px] uppercase tracking-wide text-muted-foreground/50">
        Custom
      </label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Or type a custom topic..."
        className="h-10 w-full rounded-xl border border-border/50 bg-background px-4 text-sm transition-all focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/10"
      />
    </div>
  );
}
