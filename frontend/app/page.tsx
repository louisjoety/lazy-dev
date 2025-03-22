'use client';

import { useRouter } from 'next/navigation'
import Link from 'next/link'

export default function Page() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-3xl font-bold mb-8">Lazy Dev</h1>
      <nav className="flex flex-col gap-4">
        <Link 
          href="/login" 
          className="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-center"
        >
          Login
        </Link>
        <Link 
          href="/dashboard" 
          className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600 text-center"
        >
          Dashboard
        </Link>
        <Link 
          href="/chatbot" 
          className="px-6 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 text-center"
        >
          Chatbot
        </Link>
        <Link 
          href="/upload" 
          className="px-6 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 text-center"
        >
          Upload Project
        </Link>
      </nav>
    </div>
  )
} 
