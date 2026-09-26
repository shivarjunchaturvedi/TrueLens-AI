import { createContext, useContext, useState } from 'react'
import client from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('truelens_user')
    return stored ? JSON.parse(stored) : null
  })

  const login = async (username, password) => {
    const res = await client.post('/auth/login', { username, password })
    localStorage.setItem('truelens_token', res.data.access_token)
    localStorage.setItem('truelens_user', JSON.stringify(res.data.user))
    setUser(res.data.user)
    return res.data.user
  }

  const register = async (username, email, password) => {
    await client.post('/auth/register', { username, email, password })
  }

  const logout = () => {
    localStorage.removeItem('truelens_token')
    localStorage.removeItem('truelens_user')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
