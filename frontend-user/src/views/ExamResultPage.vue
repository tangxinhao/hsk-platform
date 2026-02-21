<template>
  <div class="exam-result-page">
    <div class="result-container">
      <el-card class="result-card">
        <!-- 成绩展示 -->
        <div class="score-section">
          <div class="score-icon">
            <el-icon v-if="score >= 60" color="#67c23a" :size="80"><CircleCheck /></el-icon>
            <el-icon v-else color="#f56c6c" :size="80"><CircleClose /></el-icon>
          </div>
          
          <h1 class="exam-title">{{ examTitle }}</h1>
          
          <div class="score-display">
            <div class="score-number">{{ score }}</div>
            <div class="score-label">分</div>
          </div>
          
          <div class="score-status">
            <el-tag :type="score >= 60 ? 'success' : 'danger'" size="large">
              {{ score >= 60 ? '考试通过' : '未通过' }}
            </el-tag>
          </div>
        </div>

        <!-- 统计信息 -->
        <div class="stats-section">
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="stat-item">
                <div class="stat-icon correct">
                  <el-icon><Select /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ correctCount }}</div>
                  <div class="stat-label">答对题数</div>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-item">
                <div class="stat-icon wrong">
                  <el-icon><Close /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ totalCount - correctCount }}</div>
                  <div class="stat-label">答错题数</div>
                </div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="stat-item">
                <div class="stat-icon total">
                  <el-icon><Document /></el-icon>
                </div>
                <div class="stat-content">
                  <div class="stat-value">{{ totalCount }}</div>
                  <div class="stat-label">总题目数</div>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>

        <!-- 操作按钮 -->
        <div class="actions-section">
          <el-button size="large" @click="backToList">返回列表</el-button>
          <el-button type="primary" size="large" @click="retryExam">再考一次</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { CircleCheck, CircleClose, Select, Close, Document } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const score = ref(0)
const correctCount = ref(0)
const totalCount = ref(0)
const examTitle = ref('')

onMounted(() => {
  score.value = parseInt(route.query.score) || 0
  correctCount.value = parseInt(route.query.correct) || 0
  totalCount.value = parseInt(route.query.total) || 0
  examTitle.value = route.query.title || '考试完成'
})

const backToList = () => {
  router.push('/exam')
}

const retryExam = () => {
  router.push('/exam')
}
</script>

<style scoped>
.exam-result-page {
  min-height: calc(100vh - 64px);
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  color: #333333;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.result-container {
  max-width: 800px;
  width: 100%;
}

.result-card {
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.score-section {
  text-align: center;
  padding: 60px 40px 40px;
  background: #FFFFCC;
}

.score-icon {
  margin-bottom: 20px;
  animation: scaleIn 0.5s ease-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.exam-title {
  font-size: 24px;
  color: #333333;
  margin-bottom: 30px;
  font-weight: 600;
}

.score-display {
  display: flex;
  align-items: baseline;
  justify-content: center;
  margin-bottom: 20px;
}

.score-number {
  font-size: 96px;
  font-weight: 800;
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  color: #333333;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
  animation: countUp 1s ease-out;
}

@keyframes countUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.score-label {
  font-size: 24px;
  color: #666;
  margin-left: 10px;
}

.score-status {
  margin-top: 20px;
}

.stats-section {
  padding: 40px;
  background: white;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: #FFFFCC;
  border-radius: 12px;
  transition: all 0.3s;
}

.stat-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.stat-icon.correct {
  background: #FFFFFF;
  border: 1px solid #CCFFFF;
  color: #67c23a;
}

.stat-icon.wrong {
  background: #fef0f0;
  color: #f56c6c;
}

.stat-icon.total {
  background: #f4f4f5;
  color: #909399;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #333333;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.actions-section {
  padding: 30px 40px;
  text-align: center;
  display: flex;
  gap: 15px;
  justify-content: center;
  background: white;
  border-top: 1px solid #eee;
}

.actions-section .el-button {
  min-width: 150px;
}
</style>
