'use client'

import SigninForm from "@/components/ui/forms/signin-form"
import { Modal } from "@/components/ui/modal"


export default function SigninPage() {
    return (
        <Modal>
            <div className="relative top-0 left-0 w-full h-full">
                <SigninForm/>
            </div>
        </Modal>
    )
}