import { logout } from '../../../../lib/features/user/userSlice'
import { useAppDispatch } from '../../../../lib/hook'
import { useCallback } from 'react';

export function useFetchWithHeaders() {
  const dispatch = useAppDispatch();

  return useCallback(async function fetchWithHeaders(url: string, options?: RequestInit) {
    const token = localStorage.getItem('jwtToken');
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options?.headers
      }
    };

    let response;
    let data;

    try {
      response = await fetch(url, config);
      data = await response.json();
    } catch (error) {
      console.error(`Network or JSON parsing error: ${error}`);
      throw error;
    }

    if (!response.ok) {
      console.error(`HTTP error ${response.status}:`, data?.error || response.statusText);

      // 如果是 401 錯誤，處理登出
      if (response.status === 401) {
        localStorage.clear();
        dispatch(logout());
      }
      throw new Error(data?.error || 'Request failed');
    }

    return data;
  }, [dispatch]);
}
