import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    VitePWA({
      registerType: 'prompt',
      injectRegister: 'script',
      workbox: {
        cleanupOutdatedCaches: true,
        // skipWaiting removed: registerType 'prompt' shows the user a dialog before
        // activating a new SW. Setting skipWaiting:true would override that dialog
        // and update immediately, making the prompt meaningless.
        clientsClaim: true,
        globPatterns: ['**/*.{js,css,html,svg,png,jpg}'],
        globIgnores: [
          '**/sw.js',
          '**/workbox-*.js',
          '**/registerSW.js'
        ],
        runtimeCaching: [
          {
            urlPattern: ({ url }) => url.pathname.startsWith('/api/'),
            handler: 'NetworkFirst',
            options: {
              cacheName: 'api-cache',
              expiration: { maxEntries: 100, maxAgeSeconds: 86400 }
            }
          }
        ]
      },
      manifest: {
        name: 'TechnoPath SEAIT Guide',
        short_name: 'TechnoPath',
        description: 'SEAIT Campus Guide Map and Navigation System',
        theme_color: '#FF9800',
        background_color: '#ffffff',
        display: 'standalone',
        start_url: './',
        icons: [
          { src: 'icons/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icons/icon-512.png', sizes: '512x512', type: 'image/png' }
        ]
      }
    })
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
