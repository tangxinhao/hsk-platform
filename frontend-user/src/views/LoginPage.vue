<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <h1>欢迎回来</h1>
          <p>登录以继续您的HSK学习之旅</p>
        </div>
        
        <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="用户名或邮箱"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="密码"
              size="large"
              prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item>
            <div class="form-options">
              <el-checkbox v-model="remember">记住我</el-checkbox>
              <a href="#" class="forgot-link">忘记密码？</a>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="login-button"
              :loading="loading"
              @click="handleLogin"
            >
              登录
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="register-tip">
          还没有账号？
          <router-link to="/register" class="register-link">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import apiClient from '@/api'

const router = useRouter()
const route = useRoute()
const loginFormRef = ref(null)
const loading = ref(false)
const remember = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    try {
      loading.value = true

      // 通过统一封装的 apiClient 调用后端登录接口
      // 实际请求路径为 POST /api/user/login/
      const response = await apiClient.post('/user/login/', loginForm)
      
      console.log('登录响应:', response.data)
      
      // 保存token (后端返回的是access和refresh)
      const token = response.data.access || response.data.token
      const username = response.data.user?.username || loginForm.username
      
      if (!token) {
        throw new Error('未收到认证令牌')
      }
      
      localStorage.setItem('token', token)
      localStorage.setItem('refresh_token', response.data.refresh || '')
      localStorage.setItem('username', username)
      
      ElMessage.success('登录成功！')
      
      // 跳转
      const redirect = route.query.redirect || '/practice'
      setTimeout(() => {
        router.push(redirect)
      }, 500)
      
    } catch (error) {
      console.error('登录失败:', error)
      const errorMsg = error.response?.data?.detail || 
                      error.response?.data?.message || 
                      error.message ||
                      '登录失败，请检查用户名和密码'
      ElMessage.error(errorMsg)
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 60px);
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
  padding: 60px 20px;
  position: relative;
  overflow-x: hidden;
  overflow-y: auto;
}

.login-page::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1440 320'%3E%3Cpath fill='%23ffffff' fill-opacity='0.1' d='M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z'%3E%3C/path%3E%3C/svg%3E") no-repeat bottom;
  background-size: cover;
}

.login-container {
  width: 100%;
  max-width: 480px;
  position: relative;
  z-index: 1;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 50px 40px;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.3), 
              0 10px 25px rgba(0, 0, 0, 0.2);
  animation: slideUp 0.6s ease-out;
  margin: 20px auto;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 45px;
}

.login-header h1 {
  font-size: 36px;
  font-weight: 800;
  background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
  letter-spacing: -1px;
}

.login-header p {
  color: #666;
  font-size: 17px;
  font-weight: 500;
}

.login-form {
  margin-bottom: 25px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 12px;
  padding: 12px 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.25);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-top: -10px;
}

.forgot-link {
  color: #1a1f2e;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.3s;
}

.forgot-link:hover {
  color: #2d3748;
  text-decoration: underline;
}

.login-button {
  width: 100%;
  background: linear-gradient(135deg, #1a1f2e 0%, #2d3748 100%);
  border: none;
  height: 54px;
  font-size: 17px;
  font-weight: 700;
  border-radius: 12px;
  letter-spacing: 0.5px;
  transition: all 0.3s;
  margin-top: 10px;
}

.login-button:hover {
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
  transform: translateY(-2px);
}

.login-button:active {
  transform: translateY(0);
}

.register-tip {
  text-align: center;
  color: #666;
  font-size: 15px;
  padding-top: 25px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
  margin-top: 25px;
}

.register-link {
  color: #1a1f2e;
  text-decoration: none;
  font-weight: 700;
  margin-left: 5px;
  transition: color 0.3s;
}

.register-link:hover {
  color: #2d3748;
  text-decoration: underline;
}
</style>
