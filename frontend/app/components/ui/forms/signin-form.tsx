'use client'
import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { X as CloseIcon } from 'lucide-react'
import { FaLine } from "react-icons/fa6"
import Link from "next/link"
import { useRouter } from "next/navigation"
import Form from "next/form"
import jwt, { JwtPayload } from 'jsonwebtoken';
import { useAppDispatch } from '../../../../lib/hook'
import { loginSuccess } from '../../../../lib/features/user/userSlice'

const handleLineLogin = async () => {
  const url = process.env.NEXT_PUBLIC_BACKEND_URL;

  try {
    const response = await fetch(`${url}/uri`, {mode:'cors'});
    const data = await response.json();

    if (response.ok) {
      window.location.href = data.result;
    }
    
  } catch (error) {
    console.error(error);
  }
};

export default function SigninForm() {
  const [message, setMessage] = useState(null)
  const [redirectUrl, setRedirectUrl] = useState<string | null>(null)
  const dispatch = useAppDispatch()

  useEffect(() => {
    if (typeof window !== 'undefined') {
      setRedirectUrl(localStorage.getItem('redirectUrl') ?? '')
    }
  }, []);
  async function handleSubmit(formData: FormData) {
    const url = process.env.NEXT_PUBLIC_BACKEND_URL
    const response = await fetch(`${url}/signin`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: formData.get("email"),
        password: formData.get("password"),
      }),
    });
    const data = await response.json();
    if (response.ok) {
      const jwtToken = data.token
      localStorage.setItem('jwtToken', jwtToken)
      
      const decoded = jwt.decode(jwtToken) as JwtPayload
      if (!decoded) {
        throw new Error ('Invalid JWT payload') 
      }
      dispatch(loginSuccess({
        id: decoded.id,
        name: decoded.name
      }))
      setTimeout(() => {
        router.push(redirectUrl || '/')
      }, 1000)
    } else{
      setMessage(data.error)
    }
  }
  const router = useRouter()

  return (
    <div className="mx-auto max-w-md space-y-4 bg-background px-6 py-8 shadow-sm sm:rounded-lg">
      <div className="flex justify-end h-6">
        <Button variant="ghost" className="h-6 w-6 p-0" aria-label="Close" title="Close" onClick={() => router.push("/")}>
          <CloseIcon className="h-4 w-4" />
        </Button>
      </div>
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-bold">Login</h1>
        <p className="text-muted-foreground">Sign in to your account using your email or social media.</p>
      </div>
      <div>
        <Form className="space-y-4" action={handleSubmit}>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input name="email" type="text" placeholder="Enter your email" required />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input name="password" type="password" required />
          </div>
          {message && <p className="text-sm text-red-500 pl-4">{message}</p>}
          <Button type="submit" className="w-full">
            Sign In
          </Button>
        </Form>
        <Separator className="my-8" />
        <div className="space-y-4">
          <Button variant="outline" className="w-full" onClick={() => handleLineLogin()}>
            <FaLine className="mr-2 h-4 w-4" />
              Sign in with LINE
          </Button>
        </div>
        <div className="mt-4 text-center text-sm text-muted-foreground">
          <Link href="/signup" className="underline underline-offset-4" prefetch={false}>
            No account? Sign Up here!
          </Link>
        </div>
      </div>
    </div>
  )
}