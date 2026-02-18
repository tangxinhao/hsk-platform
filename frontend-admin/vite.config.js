import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // 部署在 Nginx 的 /admin-panel/ 路径下，必须设置 base，否则打包后静态资源会指向 /assets 导致 404
  base: '/admin-panel/',
  plugins: [vue()],
  server: {
    port: 8080,
    host: '0.0.0.0',
    strictPort: false,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path
      },
      '/media': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
