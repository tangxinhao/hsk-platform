<template>
  <div class="login-page">
    <div class="login-box">
      <div class="login-header">
        <h1>HSK管理系统</h1>
        <p>欢迎登录后台管理</p>
      </div>
      
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
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
      
      <div class="login-tip">
        <p>默认账号：admin / admin123456</p>
        <p>测试账号：test / test123456</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

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
  
  try {
    await loginFormRef.value.validate()
    
    loading.value = true
    
    console.log('发送登录请求:', loginForm)
    
    const response = await axios.post('/user/login/', loginForm)
    
    console.log('登录响应完整数据:', response)
    console.log('登录响应data:', response.data)
    
    // 保存token
    const token = response.data.access || response.data.token
    const username = response.data.user?.username || loginForm.username
    
    console.log('提取的token:', token)
    console.log('提取的username:', username)
    
    if (!token) {
      throw new Error('未收到认证令牌')
    }
    
    localStorage.setItem('token', token)
    localStorage.setItem('refresh_token', response.data.refresh || '')
    localStorage.setItem('username', username)
    
    console.log('Token已保存到localStorage')
    
    ElMessage.success('登录成功！')
    
    // 跳转到首页
    setTimeout(() => {
      console.log('准备跳转到首页')
      router.push('/')
    }, 500)
    
  } catch (error) {
    console.error('登录失败完整错误:', error)
    console.error('错误响应:', error.response)
    console.error('错误数据:', error.response?.data)
    
    const errorMsg = error.response?.data?.detail || 
                    error.response?.data?.message ||
                    error.response?.data?.error ||
                    error.message ||
                    '登录失败，请检查用户名和密码'
    ElMessage.error(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, #3b82f6 0%, #2563eb 100%);
  padding: 40px 20px;
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
  animation: wave 10s linear infinite;
}

@keyframes wave {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.login-box {
  width: 100%;
  max-width: 450px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 50px 45px;
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.3), 
              0 10px 25px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
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
  font-weight: 700;
  color: #0f172a;
  -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
  letter-spacing: -1px;
}

.login-header p {
  color: #64748b;
  font-size: 16px;
  font-weight: 400;
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
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  border-color: #3b82f6;
}

.login-button {
  width: 100%;
  background: #3b82f6;
  border: none;
  height: 54px;
  font-size: 17px;
  font-weight: 600;
  margin-top: 15px;
  border-radius: 8px;
  letter-spacing: 0.3px;
  transition: all 0.2s ease;
}

.login-button:hover {
  background: #2563eb;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
  transform: translateY(-1px);
}

.login-button:active {
  transform: translateY(0);
}

.login-tip {
  text-align: center;
  padding-top: 25px;
  border-top: 1px solid #e2e8f0;
  margin-top: 25px;
  background: rgba(59, 130, 246, 0.05);
  padding: 20px;
  border-radius: 8px;
}

.login-tip p {
  margin: 8px 0;
  font-size: 14px;
  color: #64748b;
  line-height: 1.8;
  font-weight: 400;
}

.login-tip p:first-child {
  color: #0f172a;
  font-weight: 600;
}
</style>
