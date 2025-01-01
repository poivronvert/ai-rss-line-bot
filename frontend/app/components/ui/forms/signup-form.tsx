import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { X as CloseIcon} from 'lucide-react'
import { useRouter } from "next/navigation"
import Link from "next/link"
import Form from "next/form"

export default function SignupForm() {
  const [message, setMessage] = useState(null)
  async function handleSubmit(formData: FormData) {
    const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}/signup`
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: formData.get('name'),
        email: formData.get('email'),
        password: formData.get('password'),
      })
    })

    const msg = await response.json()
    if (msg.message){
      setMessage(msg.message)
    }else{
      setMessage(msg.error)
    }
  }
  const router = useRouter()

  return (
    <div className="mx-auto max-w-md space-y-4 bg-background px-6 py-8 shadow-sm sm:rounded-lg">
      <div className="flex justify-end h-6">
        <Button variant="ghost" className="h-6 w-6 p-0" aria-label="Close" title="Close" onClick={() => router.back()}>
          <CloseIcon className="h-4 w-4" />
        </Button>
      </div>
      <div className="space-y-2 text-center">
        <h1 className="text-3xl font-bold">Sign Up</h1>
        <p className="text-muted-foreground">Create a new account by filling the form below.</p>
      </div>
      <div>
        <div className="space-y-4">
        </div>
        <Separator className="my-8" />
        <Form className="space-y-4" action={handleSubmit}>
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input name="name" type="text" placeholder="Enter your name" required/>
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input name="email" type="email" placeholder="Enter your email" required/>
            {message && <p className="text-sm text-red-500 pl-4">{message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input name="password" type="password" placeholder="Enter your password" required/>
          </div>
          <Button type="submit" className="w-full">
            Sign Up
          </Button>
        </Form>
        <div className="mt-4 text-center text-sm text-muted-foreground">
            <Link href="/signin" className="underline underline-offset-4" prefetch={false}>
              Already have an account? Sign In here!
            </Link>
        </div>
      </div>
    </div>
  )
}




