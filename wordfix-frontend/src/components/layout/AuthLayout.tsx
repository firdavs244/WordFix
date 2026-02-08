import { Outlet } from 'react-router-dom';
import { Logo } from '@/components/common/Logo';

/**
 * Auth layout for login/register pages.
 *
 * Clean, centered layout with logo.
 * To be used in future sprint when auth is implemented.
 */
export function AuthLayout() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4">
      <div className="mb-8">
        <Logo />
      </div>
      <div className="w-full max-w-md">
        <Outlet />
      </div>
    </div>
  );
}
