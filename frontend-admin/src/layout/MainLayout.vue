<template>
  <el-container class="main-layout">
    <el-header class="header">
      <div class="header-left">
        <h1 class="logo">HSK学习平台</h1>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        class="header-menu"
        mode="horizontal"
        :ellipsis="false"
        @select="handleMenuSelect"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>数据统计</span>
        </el-menu-item>
        
        <el-sub-menu index="content">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>内容管理</span>
          </template>
          <el-menu-item index="/questions">题目管理</el-menu-item>
          <el-menu-item index="/exam-sets">套卷管理</el-menu-item>
          <el-menu-item index="/culture">文化管理</el-menu-item>
        </el-sub-menu>
        
        <el-menu-item index="/universities">
          <el-icon><School /></el-icon>
          <span>院校管理</span>
        </el-menu-item>
      </el-menu>
      
      <div class="header-right">
        <el-dropdown @command="handleUserCommand">
          <span class="user-dropdown">
            <el-icon><User /></el-icon>
            <span>{{ username }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-main class="main-content">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { 
  HomeFilled, 
  DataAnalysis, 
  Document,
  School,
  User 
} from '@element-plus/icons-vue';

const router = useRouter();
const route = useRoute();

const username = ref(localStorage.getItem('username') || '游客');

const activeMenu = computed(() => route.path);

const handleMenuSelect = (index) => {
  if (index !== 'content') {
    router.push(index);
  }
};

const handleUserCommand = async (command) => {
  if (command === 'logout') {
    try {
      await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      });
      
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      ElMessage.success('已退出登录');
      router.push('/login');
    } catch {
      // 用户取消
    }
  } else if (command === 'profile') {
    ElMessage.info('个人资料功能开发中');
  }
};
</script>

<style scoped>
.main-layout {
  height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  box-shadow: 0 2px 12px 0 rgba(204, 255, 255, 0.3);
  padding: 0 20px;
}

.header-left {
  flex-shrink: 0;
  margin-right: 50px;
}

.logo {
  color: #333333;
  font-size: 22px;
  font-weight: bold;
  margin: 0;
  white-space: nowrap;
}

.header-menu {
  flex: 1;
  border-bottom: none;
  background: transparent;
}

:deep(.el-menu--horizontal > .el-menu-item),
:deep(.el-menu--horizontal > .el-sub-menu .el-sub-menu__title) {
  color: #333333;
  border-bottom: 2px solid transparent;
}

:deep(.el-menu--horizontal > .el-menu-item:hover),
:deep(.el-menu--horizontal > .el-sub-menu .el-sub-menu__title:hover) {
  background-color: rgba(255, 255, 255, 0.5);
  color: #333333;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  border-bottom-color: #CCFFFF;
  color: #333333;
  background-color: rgba(255, 255, 255, 0.5);
}

.header-right {
  flex-shrink: 0;
  margin-left: 20px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #333333;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: all 0.3s;
}

.user-dropdown:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

.main-content {
  background: #FFFFCC;
  padding: 0;
  overflow-y: auto;
}

@media (max-width: 1200px) {
  .header-left {
    margin-right: 20px;
  }
  
  .logo {
    font-size: 18px;
  }
}

@media (max-width: 768px) {
  .header {
    flex-wrap: wrap;
    height: auto;
    padding: 10px;
  }
  
  .header-menu {
    width: 100%;
    margin-top: 10px;
  }
}
</style>
