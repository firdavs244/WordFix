import { useState } from 'react';
import { MessageCircle } from 'lucide-react';
import TopicChip from './TopicChip';
import CustomTopicInput from './CustomTopicInput';
import StartChatButton from './StartChatButton';

const TOPICS = [
  { emoji: '✈️', label: 'Travel' },
  { emoji: '🍕', label: 'Food' },
  { emoji: '💻', label: 'Technology' },
  { emoji: '🎬', label: 'Movies' },
  { emoji: '☀️', label: 'Daily Life' },
  { emoji: '💼', label: 'Work' },
];

interface ChatTopicSelectorProps {
  onStart: (topic: string) => void;
  isLoading: boolean;
}

export default function ChatTopicSelector({ onStart, isLoading }: ChatTopicSelectorProps) {
  const [selected, setSelected] = useState('');
  const [custom, setCustom] = useState('');

  const handleSelect = (label: string) => {
    setSelected(label === selected ? '' : label);
    if (label !== selected) setCustom('');
  };

  const handleCustom = (val: string) => {
    setCustom(val);
    if (val) setSelected('');
  };

  const topic = selected || custom;

  return (
    <div className="relative overflow-hidden rounded-2xl border border-border/50 p-6 shadow-card lg:p-8">
      <div className="absolute right-4 top-4 opacity-[0.03]">
        <MessageCircle className="h-[100px] w-[100px] rotate-12" />
      </div>
      <h2 className="font-heading text-base font-semibold">Start a Conversation</h2>
      <p className="mt-1 text-sm text-muted-foreground">Choose a topic or write your own</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {TOPICS.map((t) => (
          <TopicChip key={t.label} {...t} isSelected={selected === t.label} onClick={() => handleSelect(t.label)} />
        ))}
      </div>
      <div className="mt-4">
        <CustomTopicInput value={custom} onChange={handleCustom} />
      </div>
      <div className="mt-4">
        <StartChatButton onClick={() => onStart(topic)} isLoading={isLoading} disabled={!topic} />
      </div>
    </div>
  );
}
