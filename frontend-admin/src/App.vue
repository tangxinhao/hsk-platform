<template>
  <div class="app-container">
    <!-- 登录页面 -->
    <template v-if="!isLoggedIn">
      <router-view />
    </template>
    
    <!-- 管理系统主界面 -->
    <template v-else>
      <!-- 侧边栏 -->
      <div class="sidebar">
        <div class="logo-container">
          <h1>HSK管理系统</h1>
        </div>
        <el-menu 
          :default-active="activeMenu"
          router
          background-color="#001529"
          text-color="#fff"
          active-text-color="#ffd04b">
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="/questions">
            <el-icon><Document /></el-icon>
            <span>题目管理</span>
          </el-menu-item>
          <el-menu-item index="/mock-exam-questions">
            <el-icon><Edit /></el-icon>
            <span>模拟考试题目</span>
          </el-menu-item>
          <el-menu-item index="/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
          <el-menu-item index="/universities">
            <el-icon><School /></el-icon>
            <span>院校管理</span>
          </el-menu-item>
          <el-menu-item index="/culture">
            <el-icon><Collection /></el-icon>
            <span>文化管理</span>
          </el-menu-item>
        </el-menu>
      </div>
      
      <!-- 主内容区 -->
      <div class="main-content">
        <!-- 顶部导航条 -->
        <div class="top-navbar">
          <div class="breadcrumb">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="currentRoute">{{ currentRoute }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="user-info">
            <el-dropdown @command="handleCommand">
              <span class="el-dropdown-link">
                {{ username || '管理员' }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
        
        <!-- 主要内容区域 -->
        <div class="content-wrapper">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
        
        <!-- 页脚 -->
        <div class="footer">
          <p>© {{ new Date().getFullYear() }} HSK学习平台 - 管理系统</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { HomeFilled, Document, School, Collection, DataAnalysis, Edit } from '@element-plus/icons-vue'

export default {
  components: {
    HomeFilled,
    Document,
    School,
    Collection,
    DataAnalysis,
    Edit
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const isLoggedIn = ref(!!localStorage.getItem('token'))
    const username = ref(localStorage.getItem('username') || '')
    
    // 监听路由变化，更新登录状态
    watch(() => route.path, () => {
      isLoggedIn.value = !!localStorage.getItem('token')
      username.value = localStorage.getItem('username') || ''
    })
    
    // 计算当前活动菜单项
    const activeMenu = computed(() => {
      return route.path
    })
    
    // 计算当前路由名称
    const currentRoute = computed(() => {
      const meta = route.meta || {}
      return meta.title || ''
    })
    
    // 处理下拉菜单命令
    const handleCommand = (command) => {
      if (command === 'logout') {
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        localStorage.removeItem('refresh_token')
        isLoggedIn.value = false
        ElMessage.success('退出成功')
        router.push('/login')
      }
    }
    
    return {
      activeMenu,
      currentRoute,
      isLoggedIn,
      username,
      handleCommand
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f0f2f5;
}

.app-container {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background-color: #001529;
  color: white;
  flex-shrink: 0;
}

.logo-container {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid #002140;
}

.logo-container h1 {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-navbar {
  height: 64px;
  background-color: white;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
}

.breadcrumb {
  font-size: 14px;
}

.user-info {
  display: flex;
  align-items: center;
}

.content-wrapper {
  padding: 24px;
  flex: 1;
}

.footer {
  text-align: center;
  color: #999;
  padding: 16px 0;
  background-color: #f7f7f7;
  border-top: 1px solid #e8e8e8;
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Element Plus 样式覆盖 */
.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
}

.el-menu {
  border-right: none;
}

.el-menu-item [class^="el-icon-"] {
  margin-right: 5px;
  width: 24px;
  text-align: center;
  font-size: 18px;
}

.highlight-menu {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
  border-left: 3px solid #ffd04b;
}

.highlight-menu:hover {
  background: linear-gradient(90deg, #764ba2 0%, #667eea 100%) !important;
}
</style> 