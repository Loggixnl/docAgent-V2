import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// Preview (Railway) runs `vite preview` against the built SPA. The preview
// server does not inherit `server.proxy` by default, so /api would hit the
// static dist and 500. Point preview proxy at the backend explicitly:
// VITE_PROXY_TARGET (preferred) or VITE_API_BASE_URL (baked at build time),
// falling back to local uvicorn for local `npm run preview`.
const proxyTarget =
  process.env.VITE_PROXY_TARGET ||
  process.env.VITE_API_BASE_URL ||
  'http://127.0.0.1:8000'

const apiProxy = {
  '/api': { target: proxyTarget, changeOrigin: true },
  '/widget.js': { target: proxyTarget, changeOrigin: true }
}

// Vite answers CORS preflights itself (before the proxy) and its default
// origin allowlist only covers localhost, which broke the embeddable widget
// on every other domain. Reflect the requesting origin so preflights pass
// for any website; the backend additionally reflects origins on /api/chat
// and /api/widget/* for the actual responses.
const corsPermissive = { origin: true }

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },

  server: {
    port: 5173,
    cors: corsPermissive,
    proxy: apiProxy
  },

  preview: {
    host: '0.0.0.0',
    allowedHosts: true,
    cors: corsPermissive,
    proxy: apiProxy
  },

  build: {
    outDir: 'dist'
  }
})