"use client"
import Link from "next/link"
import { Settings as SettingsIcon, ArrowRightFromLine, ArrowLeftFromLine, Bot, Rss, LibraryBig } from 'lucide-react';
import { Badge } from "@/components/ui/badge"
import { useState } from 'react';
import { Button } from "@/components/ui/button";

export default function Sidebar() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className={`transition-all ${isOpen ? "w-64" : "w-16"} border-r bg-muted/40 hidden lg:block`}>
            <div className="flex flex-col gap-2">
                <div className="flex h-[60px] items-center px-6 ">

                    <Link href="/" className="flex items-center gap-2 font-semibold" prefetch={false}>
                        {isOpen &&
                            <>
                                <Bot className="h-6 w-6" />
                                <span className="">Assistant</span>
                            </>
                        }
                    </Link>
                    <Button
                        variant="ghost"
                        className="p-0 ml-auto"
                        onClick={() => setIsOpen(!isOpen)}
                    >
                        {isOpen ? <ArrowLeftFromLine className="h-4 w-4" /> : <ArrowRightFromLine className="h-4 w-4" />}
                    </Button>
                </div>

                <div className="flex-1">
                    <nav className="grid items-start px-4 text-sm font-medium">
                        <Link
                            href="/lims"
                            className="flex items-center gap-3 rounded-lg bg-muted px-3 py-2 text-primary  transition-all hover:text-primary"
                            prefetch={false}
                        >
                            <Rss className="h-4 w-4" />
                            {isOpen && "LIMS Rss"}
                            {isOpen && <Badge className="ml-auto flex h-6 w-6 shrink-0 items-center justify-center rounded-full">12</Badge>}
                        </Link>
                        <Link
                            href="#"
                            className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
                            prefetch={false}
                        >
                            <LibraryBig className="h-4 w-4" />
                            {isOpen && "Collections"}
                        </Link>
                        <Link
                            href="#"
                            className="flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary"
                            prefetch={false}
                        >
                            <SettingsIcon className="h-4 w-4" />
                            {isOpen && "Settings"}
                        </Link>
                    </nav>
                </div>
            </div>
        </div>
    )
}