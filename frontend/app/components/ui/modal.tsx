'use client';

export function Modal({ children }: { children: React.ReactNode }) {

    return (
        <div className="w-full h-full fixed top-0 left-0 bg-gray-900/70 flex justify-center items-center z-10">
            <div>{children}</div>
        </div>
    );
}