import { useEffect, useRef, useState } from 'react';
import { Loader2 } from 'lucide-react';

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || '';

function GoogleIcon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none">
      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1Z" fill="#4285F4" />
      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23Z" fill="#34A853" />
      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18A10.96 10.96 0 0 0 1 12c0 1.77.42 3.45 1.18 4.93l3.66-2.84Z" fill="#FBBC05" />
      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53Z" fill="#EA4335" />
    </svg>
  );
}

interface GoogleLoginButtonProps {
  onSuccess: (credential: string) => void;
  onError?: () => void;
  text?: string;
  disabled?: boolean;
}

declare global {
  interface Window {
    google?: {
      accounts: {
        id: {
          initialize: (config: { client_id: string; callback: (r: { credential: string }) => void; auto_select?: boolean }) => void;
          prompt: () => void;
        };
      };
    };
  }
}

export function GoogleLoginButton({ onSuccess, onError, text = 'Continue with Google', disabled = false }: GoogleLoginButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [gsiReady, setGsiReady] = useState(false);
  const initializedRef = useRef(false);

  useEffect(() => {
    if (!GOOGLE_CLIENT_ID || initializedRef.current) return;
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.async = true;
    script.defer = true;
    script.onload = () => {
      if (window.google) {
        window.google.accounts.id.initialize({
          client_id: GOOGLE_CLIENT_ID,
          callback: (response) => { if (response.credential) onSuccess(response.credential); },
        });
        setGsiReady(true);
        initializedRef.current = true;
      }
    };
    document.head.appendChild(script);
  }, [onSuccess]);

  const handleClick = () => {
    if (!gsiReady || !window.google) { onError?.(); return; }
    setIsLoading(true);
    try { window.google.accounts.id.prompt(); } catch { onError?.(); }
    setTimeout(() => setIsLoading(false), 3000);
  };

  if (!GOOGLE_CLIENT_ID) return null;

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={disabled || isLoading || (!gsiReady && !!GOOGLE_CLIENT_ID)}
      className="flex h-12 w-full items-center justify-center gap-2.5 rounded-xl border border-border/50 bg-card text-sm font-medium transition-all hover:border-border hover:bg-muted/50 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {isLoading ? <Loader2 className="h-[18px] w-[18px] animate-spin" /> : <GoogleIcon className="h-[18px] w-[18px]" />}
      {isLoading ? 'Connecting...' : text}
    </button>
  );
}
