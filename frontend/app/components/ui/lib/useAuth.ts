import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAppSelector, useAppDispatch } from '../../../../lib/hook';


export function useAuth() {
  const router = useRouter();
  const pathname = usePathname();
  const dispatch = useAppDispatch();
  const isLoggedIn = useAppSelector((state) => state.user.isLoggedIn);

  useEffect(() => {
    if (!isLoggedIn && pathname !== '/signin' && pathname !== '/signup') {
      const currentUrl = pathname

      // Using optional chaining on the global object to access the window object.
      if (global?.window !== undefined) {
        localStorage.setItem('redirectUrl', currentUrl);
      }
      
      router.push('/signin');
    }
  }, [isLoggedIn, router, pathname, dispatch]);

  return isLoggedIn;
}