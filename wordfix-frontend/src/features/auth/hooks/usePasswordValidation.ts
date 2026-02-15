import { useMemo } from 'react';

export function usePasswordValidation(password: string, confirmPassword: string) {
  return useMemo(() => {
    const hasMinLength = password.length >= 8;
    const hasNumber = /\d/.test(password);
    const hasUppercase = /[A-Z]/.test(password);
    const hasSpecialChar = /[^a-zA-Z0-9]/.test(password);
    const passwordsMatch = password.length > 0 && password === confirmPassword;

    let strength = 0;
    if (hasMinLength) strength++;
    if (hasNumber) strength++;
    if (hasUppercase) strength++;
    if (hasSpecialChar) strength++;

    const isValid = hasMinLength && hasNumber && passwordsMatch;

    return { hasMinLength, hasNumber, hasUppercase, hasSpecialChar, passwordsMatch, strength, isValid };
  }, [password, confirmPassword]);
}
