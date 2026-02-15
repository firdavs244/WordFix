import type { ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

export default function FlashCardContainer({ children }: Props) {
  return (
    <div style={{ perspective: '1200px', transformStyle: 'preserve-3d' }} className="flex items-center justify-center">
      {children}
    </div>
  );
}
