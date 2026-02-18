import axios from 'axios';
import { ElMessage } from 'element-plus';

// API基础路径
// 生产环境通过 Nginx 将 /api 代理到后端，因此这里强制使用相对路径，避免被打包进 http://localhost:8000 之类的开发地址
const API_BASE_URL = '/api'

// 创建axios实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 60000 // 请求超时时间（60秒）- 听力题组保存需要更长时间
})

// 请求拦截器
apiClient.interceptors.request.use(config => {
  // 从localStorage获取token
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  console.log('API请求:', config.url, config.data || config.params)
  return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器
apiClient.interceptors.response.use(response => {
  console.log('API响应:', response.config.url, response.data)
  return response
}, error => {
  console.error('API错误:', error.response?.data || error.message)
  return Promise.reject(error)
})

// API服务
export const apiService = {
  // 通用方法
  get(url, params) {
    return apiClient.get(url, { params })
  },

  post(url, data) {
    return apiClient.post(url, data)
  },

  put(url, data) {
    return apiClient.put(url, data)
  },

  delete(url) {
    return apiClient.delete(url)
  },

  // 认证相关
  login(credentials) {
    return apiClient.post('/auth/login/', credentials)
  },

  refreshToken(refreshToken) {
    return apiClient.post('/auth/refresh/', { refresh: refreshToken })
  },

  // 用户相关
  getCurrentUser() {
    return apiClient.get('/user/')
  },

  getCsrfToken() {
    return apiClient.get('/user/csrf-token/')
  },

  // 分类管理
  getCategories() {
    return apiClient.get('/categories/')
  },

  getCategoryById(id) {
    return apiClient.get(`/categories/${id}/`)
  },

  createCategory(data) {
    console.log('创建分类数据:', data)

    // 验证level字段
    if (data.level && !['初级', '中级', '高级'].includes(data.level)) {
      console.error('创建分类错误: level值无效', data.level)
      return Promise.reject(new Error(`无效的level值: ${data.level}，必须为 "初级", "中级" 或 "高级"`))
    }

    return apiClient.post('/categories/', data)
  },

  updateCategory(id, data) {
    console.log('更新分类数据:', data)

    // 验证level字段
    if (data.level && !['初级', '中级', '高级'].includes(data.level)) {
      console.error('更新分类错误: level值无效', data.level)
      return Promise.reject(new Error(`无效的level值: ${data.level}，必须为 "初级", "中级" 或 "高级"`))
    }

    return apiClient.put(`/categories/${id}/`, data)
  },

  deleteCategory(id) {
    return apiClient.delete(`/categories/${id}/`)
  },

  // 问题管理 - 使用正确的API路径
  getQuestions(params) {
    return apiClient.get('/question/questions/', { params })
  },

  getQuestionById(id) {
    return apiClient.get(`/question/questions/${id}/`)
  },

  createQuestion(data) {
    console.log('创建题目API调用:', data)
    return apiClient.post('/question/questions/', data)
  },

  updateQuestion(id, data) {
    console.log('更新题目API调用:', id, data)
    return apiClient.put(`/question/questions/${id}/`, data)
  },

  deleteQuestion(id) {
    return apiClient.delete(`/question/questions/${id}/`)
  },

  // 大学管理 - 使用正确的API路径
  getUniversities(params) {
    return apiClient.get('/university/', { params })
  },

  getUniversityById(id) {
    return apiClient.get(`/university/${id}/`)
  },

  createUniversity(data) {
    console.log('创建大学数据:', data)

    // 确保website字段格式正确
    if (data.website && !data.website.startsWith('http')) {
      data.website = 'https://' + data.website.replace(/^[\/\\]+/, '')
    }

    return apiClient.post('/university/', data)
  },

  updateUniversity(id, data) {
    console.log('更新大学数据:', data)

    // 确保website字段格式正确
    if (data.website && !data.website.startsWith('http')) {
      data.website = 'https://' + data.website.replace(/^[\/\\]+/, '')
    }

    return apiClient.put(`/university/${id}/`, data)
  },

  deleteUniversity(id) {
    return apiClient.delete(`/university/${id}/`)
  },

  // 文化内容管理 - 根据Django日志添加正确的API路径
  getCultureContent(params) {
    // 根据日志，正确的API路径是/api/culture/category/
    if (params && params.type === 'category') {
      return apiClient.get('/culture/category/', params)
    }
    return apiClient.get('/culture/', { params })
  },

  getCultureContentById(id, type = '') {
    if (type === 'category') {
      return apiClient.get(`/culture/category/${id}/`)
    }
    return apiClient.get(`/culture/${id}/`)
  },

  createCultureContent(formData) {
    // 检查是否是文化类别创建
    if (formData.type === 'category') {
      return apiClient.post('/culture/category/', formData)
    }

    // 为文化内容创建使用multipart/form-data
    const isFormData = formData instanceof FormData
    const headers = isFormData ? {
      'Content-Type': 'multipart/form-data'
    } : {}

    return apiClient.post('/culture/', formData, { headers })
  },

  updateCultureContent(id, formData) {
    // 检查是否是文化类别更新
    if (formData.type === 'category') {
      return apiClient.put(`/culture/category/${id}/`, formData)
    }

    // 为文化内容更新使用multipart/form-data
    const isFormData = formData instanceof FormData
    const headers = isFormData ? {
      'Content-Type': 'multipart/form-data'
    } : {}

    return apiClient.put(`/culture/${id}/`, formData, { headers })
  },

  deleteCultureContent(id) {
    return apiClient.delete(`/culture/${id}/`)
  },

  // 考试套卷管理
  getExamSets(params) {
    return apiClient.get('/question/sets/', { params })
  },

  getExamSetById(id) {
    return apiClient.get(`/question/sets/${id}/`)
  },

  getExamSetDetail(id) {
    return apiClient.get(`/question/sets/${id}/`)
  },

  createExamSet(data) {
    console.log('创建套卷数据:', data)
    return apiClient.post('/question/sets/', data)
  },

  updateExamSet(id, data) {
    console.log('更新套卷数据:', data)
    return apiClient.patch(`/question/sets/${id}/`, data)
  },

  deleteExamSet(id) {
    return apiClient.delete(`/question/sets/${id}/`)
  }
}

// 测试后端连接
function testConnection() {
  return apiClient.get('/') // 测试根路径连接
}

// 默认导出，方便直接import api from '../api/index.js'
export default {
  apiService,
  testConnection
}
