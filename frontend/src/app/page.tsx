'use client'

import { useRouter } from 'next/navigation'
import { useState } from 'react'

export default function Home() {
  const router = useRouter()
  const [role, setRole] = useState<'HR' | 'applicant' | null>(null)

  const handleContinue = () => {
    if (role) {
      // Navigate to registration page with role in URL
      router.push(`/register?role=${role}`)
    }
  }

  return (
    <main className="flex flex-col items-center justify-center h-screen px-4">
      <h1 className="text-4xl font-bold mb-8">AI Resume Screener</h1>

      {/* Role buttons */}
      <div className="flex gap-6 mb-6">
        <button
          onClick={() => setRole('HR')}
          className={`px-6 py-3 rounded-xl border ${
            role === 'HR'
              ? 'bg-blue-600 text-white'
              : 'bg-white text-blue-600 border-blue-600'
          }`}
        >
          I'm an HR
        </button>

        <button
          onClick={() => setRole('applicant')}
          className={`px-6 py-3 rounded-xl border ${
            role === 'applicant'
              ? 'bg-green-600 text-white'
              : 'bg-white text-green-600 border-green-600'
          }`}
        >
          I'm an Applicant
        </button>
      </div>

      {/* Continue */}
      <button
        disabled={!role}
        onClick={handleContinue}
        className={`px-6 py-2 rounded-lg ${
          role
            ? 'bg-black text-white hover:bg-gray-800'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        Continue
      </button>

      {/* Login */}
      <div className="mt-6 text-sm">
        <p>
          Do you already have an account?
          <a href="/login" className="text-blue-600 hover:underline ml-2">
            Login
          </a>
        </p>
      </div>
    </main>
  )
}
