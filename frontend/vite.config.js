import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],

  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: true,

    proxy: {
      // Forward API calls to the FastAPI backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },

      // Uploaded images
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },

      // Generated Grad-CAM heatmaps
      '/heatmaps': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})