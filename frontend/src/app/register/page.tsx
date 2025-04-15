'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

export default function Register() {
  const router = useRouter()

  // searchParams allows us to access query string params like ?role=hr
  const searchParams = useSearchParams()

  // Form state variables
  const [role, setRole] = useState('applicant') // Default to 'applicant'
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')

  // On component mount, get the 'role' from the URL (e.g., ?role=hr)
  useEffect(() => {
    const selectedRole = searchParams.get('role') // searchParams.get() fetches the value of a query param
    if (selectedRole === 'hr' || selectedRole === 'applicant') {
      setRole(selectedRole)
    }
  }, [searchParams])

  // Handles form submission
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validate password match before sending to backend
    if (password !== confirmPassword) {
      setError("Passwords do not match")
      return
    }

    // Send data to FastAPI backend
    const res = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        password,
        role, // 'hr' or 'applicant'
      }),
    })

    if (res.ok) {
      // Redirect based on role
      router.push(role === 'hr' ? '/upload-job-description' : '/upload-resume')
    } else {
      const data = await res.json()
      setError(data.detail || 'Registration failed')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">
          Register as {role === 'hr' ? 'HR' : 'Applicant'}
        </h2>

        <form onSubmit={handleRegister} className="space-y-4">
          <input
            type="text"
            placeholder="Full Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />
          <input
            type="email"
            placeholder="Email Address"
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
          <input
            type="password"
            placeholder="Confirm Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded-md"
            required
          />

          {error && <p className="text-red-600 text-sm">{error}</p>}

          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
          >
            Register
          </button>
        </form>

        <p className="mt-4 text-sm text-center">
          Already have an account?{' '}
          <a href="/login" className="text-blue-600 underline">Login</a>
        </p>
      </div>
    </div>
  )
}
