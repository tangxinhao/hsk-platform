<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">
        <span class="logo-icon">🎓</span>
        <span class="logo-text">HSK学习平台</span>
      </router-link>
      
      <div class="nav-links">
        <router-link to="/" class="nav-link">首页</router-link>
        <router-link to="/about-hsk" class="nav-link">HSK介绍</router-link>
        <router-link to="/practice" v-if="isLoggedIn" class="nav-link">题目练习</router-link>
        <router-link to="/exam" v-if="isLoggedIn" class="nav-link">模拟考试</router-link>
        <router-link to="/universities" class="nav-link">院校推荐</router-link>
        <router-link to="/culture" class="nav-link">文化学习</router-link>
        <router-link to="/progress" v-if="isLoggedIn" class="nav-link">个人中心</router-link>
      </div>
      
      <div class="nav-actions">
        <template v-if="!isLoggedIn">
          <router-link to="/login" class="btn-login">登录</router-link>
          <router-link to="/register" class="btn-register">注册</router-link>
        </template>
        <template v-else>
          <span class="username-display">{{ username }}</span>
          <button @click="handleLogout" class="btn-logout">退出</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const isLoggedIn = ref(false)
const username = ref('')

const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  isLoggedIn.value = !!token
  username.value = localStorage.getItem('username') || ''
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('refresh_token')
  isLoggedIn.value = false
  username.value = ''
  ElMessage.success('退出成功')
  router.push('/')
}

onMounted(() => {
  checkLoginStatus()
})

// 监听路由变化，更新登录状态
watch(() => route.path, () => {
  checkLoginStatus()
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  font-weight: 700;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  color: #0f172a;
  font-weight: 600;
}

.nav-links {
  display: flex;
  gap: 32px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  color: #64748b;
  text-decoration: none;
  font-weight: 500;
  font-size: 15px;
  transition: all 0.2s ease;
  padding: 8px 12px;
  border-radius: 6px;
}

.nav-link:hover {
  color: #0f172a;
  background: #f1f5f9;
}

.nav-link.router-link-active {
  color: #3b82f6;
  background: #eff6ff;
}

.nav-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.btn-login,
.btn-register,
.btn-logout {
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-block;
}

.btn-login {
  color: #64748b;
  background: white;
  border: 1px solid #e2e8f0;
}

.btn-login:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  color: #0f172a;
}

.btn-register {
  background: #3b82f6;
  color: white;
  border: none;
}

.btn-register:hover {
  background: #2563eb;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.btn-logout {
  background: #f56c6c;
  color: white;
}

.btn-logout:hover {
  background: #f45454;
}

.username-display {
  color: #303133;
  font-weight: 600;
  font-size: 14px;
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }
}
</style>
