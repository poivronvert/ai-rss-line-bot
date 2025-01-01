'use client'

import SignupForm from "@/components/ui/forms/signup-form"
import { Modal } from "@/components/ui/modal"


export default function SigninPage() {
    return (
        <Modal>
            <div className="relative top-0 left-0 w-full h-full">
                <SignupForm/>
            </div>
        </Modal>
    )
}