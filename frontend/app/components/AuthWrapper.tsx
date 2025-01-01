'use client'

import { useAuth } from '@/components/ui/lib/useAuth';
import { ReactNode } from 'react';

export default function AuthWrapper({ children }: { children: ReactNode }) {
  useAuth();
  return <>{children}</>;
}
