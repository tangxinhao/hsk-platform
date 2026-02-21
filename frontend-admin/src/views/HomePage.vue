<template>
  <div class="home-container">
    <!-- 顶部欢迎区域 -->
    <div class="welcome-section">
      <h1>HSK学习平台管理系统</h1>
      <p>欢迎回来，{{ username || '管理员' }}</p>
    </div>

    <!-- 数据统计概览 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon primary"><Document /></el-icon>
            <div class="stat-text">
              <h3>{{ stats.totalQuestions }}</h3>
              <p>题目总数</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon success"><Notebook /></el-icon>
            <div class="stat-text">
              <h3>{{ stats.totalExamSets }}</h3>
              <p>考试套卷</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon warning"><School /></el-icon>
            <div class="stat-text">
              <h3>{{ stats.totalUniversities }}</h3>
              <p>院校信息</p>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <el-icon class="stat-icon danger"><Collection /></el-icon>
            <div class="stat-text">
              <h3>{{ stats.totalCulture }}</h3>
              <p>文化内容</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快捷管理入口 -->
    <el-row :gutter="20" class="management-section">
      <el-col :span="12">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>内容管理</span>
            </div>
          </template>
          <div class="management-grid">
            <div class="management-item" @click="navigateTo('/questions')">
              <el-icon size="24"><Document /></el-icon>
              <span>题目管理</span>
            </div>
            <div class="management-item" @click="navigateTo('/exam-sets')">
              <el-icon size="24"><Notebook /></el-icon>
              <span>套卷管理</span>
            </div>
            <div class="management-item" @click="navigateTo('/universities')">
              <el-icon size="24"><School /></el-icon>
              <span>院校管理</span>
            </div>
            <div class="management-item" @click="navigateTo('/culture')">
              <el-icon size="24"><Collection /></el-icon>
              <span>文化管理</span>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="section-card">
          <template #header>
            <div class="card-header">
              <span>系统信息</span>
            </div>
          </template>
          <div class="system-info">
            <div class="info-item">
              <el-icon><Connection /></el-icon>
              <span>后端服务状态：</span>
              <el-tag :type="backendStatus === 'online' ? 'success' : 'danger'">
                {{ backendStatus === 'online' ? '在线' : '离线' }}
              </el-tag>
            </div>
            <div class="info-item">
              <el-icon><Clock /></el-icon>
              <span>最后更新：</span>
              <span>{{ lastUpdate }}</span>
            </div>
            <el-button type="primary" size="small" @click="refreshStats" :loading="loading">
              刷新数据
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 快速操作 -->
    <el-card class="quick-actions-card">
      <template #header>
        <div class="card-header">
          <span>快速操作</span>
        </div>
      </template>
      <div class="quick-actions">
        <el-button type="primary" icon="Plus" @click="navigateTo('/questions?action=create')">
          添加新题目
        </el-button>
        <el-button type="success" icon="Plus" @click="navigateTo('/exam-sets?action=create')">
          创建考试套卷
        </el-button>
        <el-button type="warning" icon="Plus" @click="navigateTo('/universities?action=create')">
          添加院校信息
        </el-button>
        <el-button type="info" icon="Plus" @click="navigateTo('/culture?action=create')">
          发布文化内容
        </el-button>
        <el-button icon="DataAnalysis" @click="navigateTo('/dashboard')">
          查看数据统计
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Document, School, Collection, Notebook, DataAnalysis, Connection, Clock, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { apiService } from '../api/index.js'

const router = useRouter()
const loading = ref(false)
const username = ref(localStorage.getItem('username') || '管理员')
const backendStatus = ref('online')
const lastUpdate = ref(new Date().toLocaleString('zh-CN'))

const stats = ref({
  totalQuestions: 0,
  totalExamSets: 0,
  totalUniversities: 0,
  totalCulture: 0
})

const navigateTo = (path) => {
  router.push(path)
}

const loadStats = async () => {
  loading.value = true
  try {
    // 获取题目数量
    try {
      const questionsRes = await apiService.getQuestions({ page_size: 1 })
      stats.value.totalQuestions = questionsRes.data.count || questionsRes.data.length || 0
    } catch (e) {
      console.error('获取题目数量失败:', e)
    }

    // 获取套卷数量
    try {
      const setsRes = await apiService.getExamSets()
      stats.value.totalExamSets = setsRes.data.length || 0
    } catch (e) {
      console.error('获取套卷数量失败:', e)
    }

    // 获取院校数量
    try {
      const univRes = await apiService.getUniversities({ page_size: 1 })
      stats.value.totalUniversities = univRes.data.count || univRes.data.length || 0
    } catch (e) {
      console.error('获取院校数量失败:', e)
    }

    // 获取文化内容数量  
    try {
      const cultureRes = await apiService.getCultureContent({ page_size: 1 })
      stats.value.totalCulture = cultureRes.data.count || cultureRes.data.length || 0
    } catch (e) {
      console.error('获取文化内容数量失败:', e)
    }

    backendStatus.value = 'online'
    lastUpdate.value = new Date().toLocaleString('zh-CN')
  } catch (error) {
    console.error('加载统计数据失败:', error)
    backendStatus.value = 'offline'
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

const refreshStats = () => {
  loadStats()
  ElMessage.success('数据已刷新')
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.home-container {
  padding: 24px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.welcome-section {
  margin-bottom: 24px;
  padding: 32px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: white;
}

.welcome-section h1 {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 8px 0;
}

.welcome-section p {
  font-size: 18px;
  opacity: 0.9;
  margin: 0;
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border-radius: 8px;
  transition: all 0.3s;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 48px;
}

.stat-icon.primary {
  color: #1a1f2e;
}

.stat-icon.success {
  color: #67C23A;
}

.stat-icon.warning {
  color: #E6A23C;
}

.stat-icon.danger {
  color: #F56C6C;
}

.stat-text h3 {
  font-size: 32px;
  font-weight: 700;
  margin: 0 0 4px 0;
  color: #303133;
}

.stat-text p {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.management-section {
  margin-bottom: 24px;
}

.section-card {
  border-radius: 8px;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
}

.management-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 8px;
}

.management-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px;
  border: 2px solid #EBEEF5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  gap: 12px;
}

.management-item:hover {
  border-color: #1a1f2e;
  background: #ecf5ff;
  transform: translateY(-2px);
}

.management-item .el-icon {
  color: #1a1f2e;
}

.management-item span {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.system-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 8px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.info-item .el-icon {
  color: #909399;
}

.quick-actions-card {
  border-radius: 8px;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
}

.quick-actions .el-button {
  flex: 1;
  min-width: 160px;
}
</style> 