<template>
  <div class="exam-result-page">
    <div class="result-container" v-loading="loading">
      <!-- 顶部成绩卡片 -->
      <div class="score-card">
        <div class="score-header">
          <div class="score-icon" :class="scoreLevel">
            <el-icon :size="80">
              <component :is="scoreIcon" />
            </el-icon>
          </div>
          <h1 class="exam-title">{{ report.question_set_title }}</h1>
          <div class="score-label">{{ scoreText }}</div>
        </div>
        
        <div class="score-body">
          <div class="score-circle">
            <el-progress
              type="circle"
              :percentage="report.score"
              :width="180"
              :stroke-width="12"
              :color="scoreColor"
            >
              <template #default="{ percentage }">
                <span class="percentage-value">{{ percentage }}</span>
                <span class="percentage-label">分</span>
              </template>
            </el-progress>
          </div>
          
          <div class="score-stats">
            <div class="stat-row">
              <div class="stat-item">
                <div class="stat-icon correct">
                  <el-icon><CircleCheck /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ report.correct_count }}</div>
                  <div class="stat-label">正确</div>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon wrong">
                  <el-icon><CircleClose /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ report.total_questions - report.correct_count }}</div>
                  <div class="stat-label">错误</div>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon time">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ formatTime(report.time_spent) }}</div>
                  <div class="stat-label">用时</div>
                </div>
              </div>
              
              <div class="stat-item">
                <div class="stat-icon rate">
                  <el-icon><TrendCharts /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ report.accuracy_rate }}%</div>
                  <div class="stat-label">正确率</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分类表现 -->
      <el-card class="performance-card" v-if="categoryPerformanceList.length > 0">
        <template #header>
          <div class="card-header">
            <el-icon><DataAnalysis /></el-icon>
            <span>分类表现</span>
          </div>
        </template>
        
        <div class="category-list">
          <div 
            v-for="category in categoryPerformanceList" 
            :key="category.name"
            class="category-item"
          >
            <div class="category-info">
              <span class="category-name">{{ category.name }}</span>
              <span class="category-stats">{{ category.correct }}/{{ category.total }}</span>
            </div>
            <div class="category-progress">
              <el-progress
                :percentage="category.accuracy"
                :color="getCategoryColor(category.accuracy)"
                :show-text="true"
                :format="() => `${category.accuracy}%`"
              />
            </div>
          </div>
        </div>
      </el-card>

      <!-- 学习建议 -->
      <el-card class="suggestions-card" v-if="report.suggestions">
        <template #header>
          <div class="card-header">
            <el-icon><Reading /></el-icon>
            <span>学习建议</span>
          </div>
        </template>
        
        <div class="suggestions-content">
          <el-alert
            :title="report.suggestions"
            type="info"
            :closable="false"
            show-icon
          />
          
          <div class="weak-points" v-if="weakPointsList.length > 0">
            <h4>薄弱知识点</h4>
            <div class="weak-points-grid">
              <div 
                v-for="(point, index) in weakPointsList" 
                :key="index"
                class="weak-point-card"
              >
                <div class="weak-point-header">
                  <el-icon color="#e6a23c"><Warning /></el-icon>
                  <span class="question-id">题目 {{ point.question_id }}</span>
                  <el-tag size="small" :type="getDifficultyType(point.difficulty)">
                    {{ getDifficultyText(point.difficulty) }}
                  </el-tag>
                </div>
                <div class="weak-point-content">{{ point.content }}</div>
                <div class="weak-point-footer" v-if="point.category && point.category !== '未分类'">
                  <el-tag size="small" type="info" effect="plain">{{ point.category }}</el-tag>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 排行榜 -->
      <el-card class="ranking-card" v-if="rankings.length > 0">
        <template #header>
          <div class="card-header">
            <el-icon><TrophyBase /></el-icon>
            <span>排行榜 TOP 10</span>
          </div>
        </template>
        
        <div class="ranking-list">
          <div 
            v-for="(ranking, index) in rankings.slice(0, 10)" 
            :key="ranking.rank"
            class="ranking-item"
            :class="{ 'is-current': ranking.is_current_user, 'is-top': index < 3 }"
          >
            <div class="ranking-rank">
              <el-icon v-if="index === 0" color="#FFD700" :size="24"><Trophy /></el-icon>
              <el-icon v-else-if="index === 1" color="#C0C0C0" :size="24"><Trophy /></el-icon>
              <el-icon v-else-if="index === 2" color="#CD7F32" :size="24"><Trophy /></el-icon>
              <span v-else class="rank-number">{{ ranking.rank }}</span>
            </div>
            <div class="ranking-user">
              <el-avatar :size="36">{{ ranking.username.charAt(0) }}</el-avatar>
              <span class="username">{{ ranking.username }}</span>
              <el-tag v-if="ranking.is_current_user" type="success" size="small">我</el-tag>
            </div>
            <div class="ranking-score">{{ ranking.score }}分</div>
            <div class="ranking-time">{{ ranking.time_spent }}分钟</div>
          </div>
        </div>
      </el-card>

      <!-- 操作按钮 -->
      <div class="actions-section">
        <el-button size="large" @click="backToList">
          <el-icon><ArrowLeft /></el-icon>
          返回列表
        </el-button>
        <el-button type="info" size="large" plain @click="viewWrongBook">
          <el-icon><Failed /></el-icon>
          查看错题
        </el-button>
        <el-button type="primary" size="large" @click="retryExam">
          <el-icon><RefreshRight /></el-icon>
          再考一次
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  CircleCheck,
  CircleClose,
  Clock,
  TrendCharts,
  DataAnalysis,
  Reading,
  TrophyBase,
  Trophy,
  ArrowLeft,
  Failed,
  RefreshRight,
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled,
  Warning
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const report = ref({
  exam_id: null,
  question_set_title: '',
  score: 0,
  total_questions: 0,
  correct_count: 0,
  accuracy_rate: 0,
  time_spent: 0,
  category_performance: {},
  weak_points: [],
  suggestions: ''
})
const rankings = ref([])

// 成绩等级
const scoreLevel = computed(() => {
  const score = report.value.score
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 60) return 'pass'
  return 'fail'
})

// 成绩图标
const scoreIcon = computed(() => {
  const score = report.value.score
  if (score >= 80) return SuccessFilled
  if (score >= 60) return WarningFilled
  return CircleCloseFilled
})

// 成绩文本
const scoreText = computed(() => {
  const score = report.value.score
  if (score >= 90) return '优秀！'
  if (score >= 80) return '良好！'
  if (score >= 60) return '及格'
  return '不及格'
})

// 成绩颜色
const scoreColor = computed(() => {
  const score = report.value.score
  if (score >= 90) return '#67c23a'
  if (score >= 80) return '#409eff'
  if (score >= 60) return '#e6a23c'
  return '#f56c6c'
})

// 分类表现列表
const categoryPerformanceList = computed(() => {
  const performance = report.value.category_performance
  if (!performance || typeof performance !== 'object') return []
  
  return Object.entries(performance).map(([name, data]) => ({
    name,
    correct: data.correct || 0,
    total: data.total || 0,
    accuracy: Math.round((data.correct / data.total) * 100) || 0
  }))
})

// 薄弱知识点列表（解析JSON）
const weakPointsList = computed(() => {
  const weakPoints = report.value.weak_points
  if (!weakPoints || !Array.isArray(weakPoints)) return []
  
  return weakPoints.map(point => {
    // 如果是字符串，尝试解析为JSON
    if (typeof point === 'string') {
      try {
        return JSON.parse(point)
      } catch (e) {
        // 解析失败，返回原字符串作为content
        return { content: point, question_id: null, category: null, difficulty: 2 }
      }
    }
    // 如果已经是对象，直接返回
    return point
  }).filter(point => point && point.content) // 过滤掉无效数据
})

// 加载考试报告
const loadReport = async () => {
  loading.value = true
  try {
    const examId = route.query.examId
    if (!examId) {
      throw new Error('缺少考试ID')
    }
    
    const token = localStorage.getItem('token')
    
    // 获取考试报告
    const reportResponse = await axios.get(
      `/question/exam/${examId}/report/`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    
    report.value = reportResponse.data
    
    // 获取排行榜
    try {
      const rankingResponse = await axios.get(
        `/question/exam/${examId}/ranking/`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      rankings.value = rankingResponse.data
    } catch (e) {
      console.log('获取排行榜失败:', e)
    }
  } catch (error) {
    console.error('加载报告失败:', error)
    ElMessage.error('加载报告失败: ' + (error.response?.data?.error || error.message))
    // 使用URL中的基本数据作为备选
    report.value.score = parseFloat(route.query.score) || 0
  } finally {
    loading.value = false
  }
}

// 格式化时间
const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${minutes}'${secs}"`
}

// 获取分类颜色
const getCategoryColor = (accuracy) => {
  if (accuracy >= 80) return '#67c23a'
  if (accuracy >= 60) return '#e6a23c'
  return '#f56c6c'
}

// 获取难度类型
const getDifficultyType = (difficulty) => {
  if (difficulty === 1) return 'success'
  if (difficulty === 2) return ''
  if (difficulty === 3) return 'warning'
  return 'danger'
}

// 获取难度文本
const getDifficultyText = (difficulty) => {
  const texts = {
    1: '简单',
    2: '中等',
    3: '困难',
    4: '极难'
  }
  return texts[difficulty] || '中等'
}

// 返回列表
const backToList = () => {
  router.push('/exam')
}

// 查看错题本
const viewWrongBook = () => {
  router.push('/wrong-book')
}

// 再考一次
const retryExam = () => {
  router.push('/exam')
}

onMounted(() => {
  loadReport()
})
</script>

<style scoped>
.exam-result-page {
  min-height: calc(100vh - 64px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.result-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* 成绩卡片 */
.score-card {
  background: white;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  margin-bottom: 24px;
}

.score-header {
  text-align: center;
  padding: 40px 40px 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
}

.score-icon {
  margin-bottom: 16px;
  animation: scaleIn 0.5s ease-out;
}

.score-icon.excellent {
  color: #67c23a;
}

.score-icon.good {
  color: #409eff;
}

.score-icon.pass {
  color: #e6a23c;
}

.score-icon.fail {
  color: #f56c6c;
}

@keyframes scaleIn {
  from {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  to {
    transform: scale(1) rotate(0);
    opacity: 1;
  }
}

.exam-title {
  font-size: 28px;
  color: #2c3e50;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.score-label {
  font-size: 20px;
  color: #666;
  font-weight: 600;
}

.score-body {
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 40px;
  gap: 40px;
}

.score-circle {
  flex-shrink: 0;
}

.percentage-value {
  font-size: 48px;
  font-weight: 700;
  color: #2c3e50;
}

.percentage-label {
  font-size: 18px;
  color: #666;
  margin-left: 4px;
}

.score-stats {
  flex: 1;
}

.stat-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 12px;
  transition: all 0.3s;
}

.stat-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.stat-icon.correct {
  background: #f0f9ff;
  color: #67c23a;
}

.stat-icon.wrong {
  background: #fef0f0;
  color: #f56c6c;
}

.stat-icon.time {
  background: #fdf6ec;
  color: #e6a23c;
}

.stat-icon.rate {
  background: #f4f4f5;
  color: #409eff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

/* 分类表现卡片 */
.performance-card,
.suggestions-card,
.ranking-card {
  margin-bottom: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.category-item {
  padding: 16px 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.category-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.category-name {
  font-size: 15px;
  font-weight: 600;
  color: #2c3e50;
}

.category-stats {
  font-size: 14px;
  color: #909399;
}

/* 学习建议 */
.suggestions-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.weak-points h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #606266;
  font-weight: 600;
}

.weak-points-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.weak-point-card {
  background: #fffbf0;
  border: 1px solid #faecd8;
  border-radius: 8px;
  padding: 16px;
  transition: all 0.3s;
}

.weak-point-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(230, 162, 60, 0.15);
  border-color: #e6a23c;
}

.weak-point-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.question-id {
  font-size: 13px;
  color: #909399;
  flex: 1;
}

.weak-point-content {
  font-size: 14px;
  line-height: 1.6;
  color: #303133;
  margin-bottom: 12px;
  word-break: break-word;
}

.weak-point-footer {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 排行榜 */
.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 16px;
  background: #f5f7fa;
  border-radius: 8px;
  transition: all 0.3s;
}

.ranking-item:hover {
  background: #ecf5ff;
}

.ranking-item.is-current {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.ranking-item.is-current .username,
.ranking-item.is-current .ranking-score,
.ranking-item.is-current .ranking-time {
  color: white;
}

.ranking-item.is-top {
  background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
  color: white;
}

.ranking-item.is-top .username,
.ranking-item.is-top .ranking-score,
.ranking-item.is-top .ranking-time,
.ranking-item.is-top .rank-number {
  color: white;
}

.ranking-rank {
  width: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.rank-number {
  font-size: 18px;
  font-weight: 700;
  color: #909399;
}

.ranking-user {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-size: 15px;
  font-weight: 600;
  color: #2c3e50;
}

.ranking-score {
  font-size: 18px;
  font-weight: 700;
  color: #409eff;
  min-width: 80px;
  text-align: right;
}

.ranking-time {
  font-size: 14px;
  color: #909399;
  min-width: 80px;
  text-align: right;
}

/* 操作按钮 */
.actions-section {
  display: flex;
  gap: 16px;
  justify-content: center;
  padding: 20px;
}

.actions-section .el-button {
  min-width: 140px;
  height: 48px;
  font-size: 16px;
}

/* 响应式 */
@media (max-width: 768px) {
  .score-body {
    flex-direction: column;
  }
  
  .stat-row {
    grid-template-columns: 1fr;
  }
  
  .actions-section {
    flex-direction: column;
  }
  
  .actions-section .el-button {
    width: 100%;
  }
  
  .weak-points-grid {
    grid-template-columns: 1fr;
  }
}
</style>
