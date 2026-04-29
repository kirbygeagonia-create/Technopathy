import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  base: '/seait-technopath/',
  plugins: [
    vue()
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      },
      '/chatbot-api': {
        target: 'http://localhost:5187',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/chatbot-api/, '')
      }
    }
  }
})
