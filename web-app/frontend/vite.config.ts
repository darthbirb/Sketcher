import { defineConfig } from 'vite'
import path from "path"
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

const isProduction = process.env.NODE_ENV === 'production';
const API_URL = isProduction
  ? 'https://sketcher-backend-294103069034.europe-west1.run.app'
  : 'http://localhost:5000';

  export default defineConfig({
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(API_URL),
    },
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
      },
    },
    server: {
      proxy: {
        '/predict': {
          target: API_URL,
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/predict/, '/predict'),
        },
      },
    },
  });