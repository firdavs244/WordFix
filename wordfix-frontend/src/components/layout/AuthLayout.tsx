import { Outlet } from 'react-router-dom';
import { Logo } from '@/components/shared';
import { APP_DESCRIPTION } from '@/lib/constants';
import { useMediaQuery } from '@/hooks/useMediaQuery';
import { FloatingShapes } from '@/features/auth/components/FloatingShapes';

export function AuthLayout() {
  const isDesktop = useMediaQuery('(min-width: 1024px)');

  return (
    <div className="flex min-h-screen bg-background">
      {/* Decorative left panel — desktop only */}
      {isDesktop && (
        <div className="relative hidden flex-1 flex-col items-center justify-center overflow-hidden bg-gradient-to-br from-primary/5 to-secondary/5 lg:flex">
          <FloatingShapes />
          <div className="relative z-10">
            <Logo size="lg" />
            <p className="mt-4 max-w-xs text-center text-sm font-medium text-gradient">
              {APP_DESCRIPTION}
            </p>
          </div>
        </div>
      )}

      {/* Form panel */}
      <div className="flex flex-1 flex-col items-center justify-center p-8">
        {!isDesktop && (
          <div className="mb-8">
            <Logo size="md" />
          </div>
        )}
        <div className="w-full max-w-md">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
