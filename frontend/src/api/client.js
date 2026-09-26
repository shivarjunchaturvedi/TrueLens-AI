import axios from 'axios'

// In dev, Vite proxies /api -> http://localhost:8000 (see vite.config.js).
// In production, set VITE_API_BASE_URL to the deployed backend URL.
const baseURL = import.meta.env.VITE_API_BASE_URL || '/api'

const client = axios.create({ baseURL })

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('truelens_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('truelens_token')
      localStorage.removeItem('truelens_user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default client
