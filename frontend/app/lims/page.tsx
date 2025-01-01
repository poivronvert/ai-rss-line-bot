'use client'

import { useAuth } from '@/components/ui/lib/useAuth'

export default function Page () {
    const isLoggednIn = useAuth()

    if (!isLoggednIn) return null
    
    return <div>Hello</div>
}