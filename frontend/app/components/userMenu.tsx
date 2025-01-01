// app/components/userMenu.tsx
'use client'

import { useAppSelector, useAppDispatch } from '../../lib/hook'
import { UserRound } from 'lucide-react'
import Link from 'next/link'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem
} from "@/components/ui/dropdown-menu"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { logout } from '../../lib/features/user/userSlice'
import { AppDispatch } from '../../lib/store'

function useLogout(dispatch: AppDispatch) {
  return () => {
    localStorage.clear()
    dispatch(logout())
  }
}


export default function UserMenu(): JSX.Element {
  const dispatch = useAppDispatch()
  const isLoggedIn = useAppSelector((state) => state.user.isLoggedIn)
  const userInfo = useAppSelector((state) => state.user.userInfo)
  const handleLogout = useLogout(dispatch)

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Avatar className="cursor-pointer">
          {isLoggedIn ? (
            <>
              <AvatarImage src={userInfo.picture} alt={userInfo.name} />
              <AvatarFallback>{userInfo.name?.[0]?.toUpperCase()}</AvatarFallback>
            </>
          ) : (
            <AvatarFallback>
              <UserRound className="h-5 w-5" />
            </AvatarFallback>
          )}
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        {isLoggedIn ? (
          <DropdownMenuItem onClick={handleLogout}>
            Logout
          </DropdownMenuItem>
        ) : (
          <DropdownMenuItem asChild>
            <Link href="/signin" className="w-full">Login</Link>
          </DropdownMenuItem>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}