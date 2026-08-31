// src/app/layout.tsx

import './globals.css'
import { Inter } from 'next/font/google'

// Import a clean, readable font
const inter = Inter({ subsets: ['latin'] })

// Metadata is used for SEO and browser info
export const metadata = {
  title: 'CV Wizard',
  description: 'Screen and rank resumes using AI',
}

// Root layout wraps around all pages (like a template)
export default function RootLayout({
  children, // children = content of the page currently being viewed
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
            {/* 💡 applying google fonts*/}
      <body className={`${inter.className} bg-gray-50 text-gray-900`}> 
        <div className="min-h-screen flex flex-col">

          {/* 💡 Header (Sticky on top, stylish shadow and padding) top-0 means it remains while scrolling and z-50 mean above all*/}
          <header className="bg-white shadow-md sticky top-0 z-50">
            <div className="container mx-auto px-4 py-4 flex items-center justify-between">
              <h1 className="text-2xl font-bold text-blue-700">CV Wizard</h1>
              <p className="text-sm text-gray-500 hidden sm:block">
                Smart AI-Powered Resume Screening
              </p>
            </div>
          </header>

          {/* 📄 Main content area */}
          <main className="flex-1 container mx-auto px-4 py-8">
            {children}
          </main>

          {/* 📌 Footer (at the bottom with soft border and spacing) */}
          <footer className="bg-white border-t py-4 text-center text-sm text-gray-500">
            © {new Date().getFullYear()} CV Wizard — Built by Lemo and Hesham 
          </footer>
        </div>
      </body>
    </html>
  )
}
