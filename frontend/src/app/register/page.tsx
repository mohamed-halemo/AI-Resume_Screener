'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

export default function Register() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [role, setRole] = useState('applicant') // Default to applicant
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  // On mount, get role from URL if passed from previous screen
  useEffect(() => {
    const selectedRole = searchParams.get('role')
    if (selectedRole === 'hr' || selectedRole === 'applicant') {
      setRole(selectedRole)
    }
  }, [searchParams])

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()

    // Send POST request to your FastAPI backend to create user
    const res = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        password,
        role, // the selected role: 'hr' or 'applicant'
      }),
    })

    if (res.ok) {
      router.push(role === 'hr' ? '/upload-job-description' : '/upload-resume')
    } else {
      const data = await res.json()
      setError(data.detail || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Register as {role === 'hr' ? 'HR' : 'Applicant'}</h2>

        {/* Registration Form */}
        <form onSubmit={handleRegister} className="space-y-4">
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />

          {/* Error message display */}
          {error && <p className="text-red-600 text-sm">{error}</p>}

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
          >
            Register
          </button>
        </form>

        {/* Go back link */}
        <p className="mt-4 text-sm text-center">
          Already have an account? <a href="/login" className="text-blue-600 underline">Login</a>
        </p>
      </div>
    </div>
  )
}
