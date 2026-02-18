import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import { apiService } from './api/index.js';
import axios from 'axios';

// 配置axios全局设置
axios.defaults.baseURL = '/api';
axios.defaults.timeout = 60000; // 增加到60秒，避免复杂操作超时

// axios请求拦截器
axios.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

// 创建Vue应用
const app = createApp(App);

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('全局错误:', err);
  console.error('错误组件:', vm);
  console.error('错误信息:', info);
};

// 捕获未处理的Promise错误
window.addEventListener('unhandledrejection', event => {
  console.error('未处理的Promise错误:', event.reason);
});

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 使用插件
app.use(router);
app.use(ElementPlus);

// 挂载API服务到全局
app.config.globalProperties.$api = apiService;

// 挂载应用
app.mount('#app'); 