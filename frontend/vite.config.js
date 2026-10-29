import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },

  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/widget.js': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  },

  preview: {
    host: '0.0.0.0',
    allowedHosts: true
  },

  build: {
    outDir: 'dist'
  }
})