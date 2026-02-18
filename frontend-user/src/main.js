import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

// 配置axios - 生产环境统一使用相对路径，通过 Nginx 代理到后端
// 这里不再依赖环境变量，避免打包环境里误配为 localhost
axios.defaults.baseURL = '/api'
axios.defaults.timeout = 60000 // 增加到60秒，避免复杂操作超时

// 请求拦截器
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 统一处理错误，避免重复提示
let isShowingError = false
axios.interceptors.response.use(
  response => response,
  error => {
    // 避免同时显示多个错误提示
    if (!isShowingError) {
      isShowingError = true
      
      if (error.response) {
        switch (error.response.status) {
          case 401:
            ElMessage.error('请先登录')
            localStorage.removeItem('token')
            if (router.currentRoute.value.path !== '/login') {
              router.push('/login')
            }
            break
          case 404:
            console.error('接口不存在:', error.config.url)
            // 不显示404错误给用户，只在控制台记录
            break
          default:
            // 其他错误也只在控制台记录
            console.error('请求错误:', error.response.status, error.config.url)
        }
      }
      
      setTimeout(() => {
        isShowingError = false
      }, 1000)
    }
    
    return Promise.reject(error)
  }
)

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
app.mount('#app')
