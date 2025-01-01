'use client'

import { useEffect, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import jwt , { JwtPayload }from 'jsonwebtoken';
import { useAppDispatch } from '../../lib/hook'
import { loginSuccess } from '../../lib/features/user/userSlice'

function CallbackContent(): JSX.Element {
  const searchParams = useSearchParams()
  const router = useRouter()
  const dispatch = useAppDispatch()

  useEffect(() => {
    const code = searchParams.get('code') 
    const state = searchParams.get('state')

    if (!code || !state) {
      console.error('Missing code or state in URL parameters')
      router.push('/')
      return
    }

    const getUserInfo = async () => {
      const redirectUrl = localStorage.getItem('redirectUrl');
      
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/auth`, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({ code, state }),
        })

        if (!response.ok) {
          console.error("/auth 連線失敗")
        }

        const jwtData = await response.json()

        const jwtToken = jwtData.token as string        
        const decoded = jwt.decode(jwtToken) as JwtPayload

        if (!decoded) {
          throw new Error ('Invalid JWT payload') 
        }

        if (global?.window !== undefined) {
          localStorage.setItem('jwtToken', jwtToken);
        }

        dispatch(loginSuccess({
          id: decoded.id,
          name: decoded.name,
          picture: decoded.picture,
        }))
        
        // Redirect to the previous page or home if not set
        router.push(redirectUrl || '/')
      } catch (error) {
        console.error('Authentication error:', error)
      }
    }

    getUserInfo()
  })

  return <div>Processing your login...</div>
}

export default function CallbackPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <CallbackContent />
    </Suspense>
  )
}