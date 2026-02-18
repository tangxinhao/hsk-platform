<template>
  <div class="user-center-page">
    <!-- 顶部横幅 -->
    <div class="hero-banner">
      <div class="banner-content">
        <div class="user-avatar">
          <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" />
          <div v-else class="default-avatar">{{ userInfo.username ? userInfo.username[0].toUpperCase() : 'U' }}</div>
        </div>
        <div class="user-basic-info">
          <h1 class="username">{{ userInfo.username || '学习者' }}</h1>
          <div class="user-tags">
            <el-tag type="primary" size="large">HSK {{ userInfo.hsk_level || 1 }} 级</el-tag>
            <el-tag type="success" size="large">学习第 {{ studyDays }} 天</el-tag>
            <el-tag v-if="userInfo.nationality" type="info" size="large">{{ userInfo.nationality }}</el-tag>
          </div>
        </div>
      </div>
      <svg class="wave" viewBox="0 0 1200 120" preserveAspectRatio="none">
        <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" class="wave-fill"></path>
      </svg>
    </div>

    <div class="container" v-loading="loading">
      <!-- 核心统计卡片 -->
      <section class="core-stats">
        <div class="stats-grid">
          <div class="stat-card primary">
            <div class="stat-icon">📝</div>
            <div class="stat-content">
              <div class="stat-number">{{ totalPractices }}</div>
              <div class="stat-label">练习总数</div>
              <div class="stat-trend">+{{ recentPractices }} 最近7天</div>
            </div>
          </div>
          <div class="stat-card success">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-number">{{ correctRate }}%</div>
              <div class="stat-label">正确率</div>
              <div class="stat-progress">
                <el-progress :percentage="correctRate" :show-text="false" :stroke-width="6" />
              </div>
            </div>
          </div>
          <div class="stat-card warning">
            <div class="stat-icon">❌</div>
            <div class="stat-content">
              <div class="stat-number">{{ wrongCount }}</div>
              <div class="stat-label">错题数量</div>
              <el-button type="warning" size="small" text @click="goToWrongBook">查看错题本</el-button>
            </div>
          </div>
          <div class="stat-card info">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <div class="stat-number">{{ totalScore }}</div>
              <div class="stat-label">学习积分</div>
              <div class="stat-trend">继续加油！</div>
            </div>
          </div>
        </div>
      </section>

      <div class="main-content">
        <!-- 左侧内容 -->
        <div class="left-content">
          <!-- HSK等级进度 -->
          <section class="section level-section">
            <div class="section-header">
              <div>
                <h2><el-icon><Trophy /></el-icon> HSK等级进度</h2>
                <p>您在各个等级的学习情况</p>
              </div>
            </div>
            <div class="level-list">
              <div 
                v-for="level in levelProgress" 
                :key="level.level"
                class="level-item"
                :class="`level-${level.level}`"
              >
                <div class="level-header">
                  <div class="level-badge">HSK {{ level.level }}</div>
                  <div class="level-percentage">{{ level.progress }}%</div>
                </div>
                <el-progress 
                  :percentage="level.progress" 
                  :color="getLevelColor(level.level)"
                  :stroke-width="12"
                />
                <div class="level-stats">
                  <span>已练: {{ level.practiced }}题</span>
                  <span>正确率: {{ level.accuracy }}%</span>
                </div>
              </div>
            </div>
          </section>

        </div>

        <!-- 右侧内容 -->
        <div class="right-content">
          <!-- 最近练习 -->
          <section class="section recent-section">
            <div class="section-header">
              <h2><el-icon><Clock /></el-icon> 最近练习</h2>
              <el-button type="primary" text @click="goToPractice">开始练习</el-button>
            </div>
            <div class="recent-list">
              <div 
                v-for="record in recentRecords" 
                :key="record.id"
                class="recent-item"
              >
                <div class="recent-icon" :class="record.is_correct ? 'correct' : 'wrong'">
                  <el-icon v-if="record.is_correct"><CircleCheck /></el-icon>
                  <el-icon v-else><CircleClose /></el-icon>
                </div>
                <div class="recent-content">
                  <div class="recent-question">{{ record.question_content }}</div>
                  <div class="recent-time">{{ formatTime(record.created_at) }}</div>
                </div>
              </div>
              <div v-if="recentRecords.length === 0" class="empty-recent">
                <el-empty description="暂无练习记录" :image-size="80" />
              </div>
            </div>
          </section>

          <!-- 快速入口 -->
          <section class="section quick-actions">
            <div class="section-header">
              <h2><el-icon><Compass /></el-icon> 快速入口</h2>
            </div>
            <div class="actions-grid">
              <div class="action-card" @click="goToPractice">
                <el-icon class="action-icon"><Edit /></el-icon>
                <span>题目练习</span>
              </div>
              <div class="action-card" @click="goToExam">
                <el-icon class="action-icon"><Document /></el-icon>
                <span>模拟考试</span>
              </div>
              <div class="action-card" @click="goToWrongBook">
                <el-icon class="action-icon"><Warning /></el-icon>
                <span>错题本</span>
              </div>
              <div class="action-card" @click="goToCulture">
                <el-icon class="action-icon"><Reading /></el-icon>
                <span>文化学习</span>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Trophy, TrendCharts, Clock, Compass, Edit, Document, Warning, Reading,
  CircleCheck, CircleClose
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)

// 用户信息
const userInfo = ref({
  username: localStorage.getItem('username') || '',
  avatar: '',
  hsk_level: 1,
  nationality: ''
})

// 统计数据
const totalPractices = ref(0)
const correctRate = ref(0)
const wrongCount = ref(0)
const totalScore = ref(0)
const studyDays = ref(0)
const recentPractices = ref(0)

// HSK等级进度
const levelProgress = ref([
  { level: 1, progress: 0, practiced: 0, accuracy: 0 },
  { level: 2, progress: 0, practiced: 0, accuracy: 0 },
  { level: 3, progress: 0, practiced: 0, accuracy: 0 },
  { level: 4, progress: 0, practiced: 0, accuracy: 0 },
  { level: 5, progress: 0, practiced: 0, accuracy: 0 },
  { level: 6, progress: 0, practiced: 0, accuracy: 0 }
])

// 学习趋势
const trendDays = ref(7)
const trendData = ref([])

// 最近练习记录
const recentRecords = ref([])

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    // 加载学习进度概览
    try {
      const overviewRes = await axios.get('/user/progress/overview/')
      if (overviewRes.data) {
        totalPractices.value = overviewRes.data.total_practices || 0
        correctRate.value = Math.round(overviewRes.data.correct_rate || 0)
        studyDays.value = overviewRes.data.study_days || 0
        totalScore.value = overviewRes.data.total_score || 0
        wrongCount.value = overviewRes.data.wrong_count || 0
        
        // 计算最近7天的练习数（如果后端没有提供）
        recentPractices.value = overviewRes.data.recent_practices || Math.floor((overviewRes.data.total_practices || 0) * 0.1)
      }
    } catch (err) {
      console.error('获取进度概览失败:', err)
      // 使用默认值
      totalPractices.value = 0
      correctRate.value = 0
      studyDays.value = 0
      totalScore.value = 0
      wrongCount.value = 0
      recentPractices.value = 0
    }

    // 加载HSK等级进度
    try {
      const levelRes = await axios.get('/user/progress/level/')
      if (levelRes.data && Array.isArray(levelRes.data)) {
        // 创建一个包含所有6个等级的数组
        const allLevels = [1, 2, 3, 4, 5, 6].map(level => {
          const levelData = levelRes.data.find(l => l.level === level)
          return {
            level: level,
            progress: Math.round(levelData?.progress || 0),
            practiced: levelData?.practiced || 0,
            accuracy: Math.round(levelData?.accuracy || 0)
          }
        })
        levelProgress.value = allLevels
      }
    } catch (err) {
      console.error('获取等级进度失败:', err)
      // 保持默认值
    }

    // 加载最近练习记录（从答题记录API获取）
    try {
      // 使用答题记录查询API
      const recordsRes = await axios.get('/question/answer-records/', { 
        params: { 
          page: 1,
          page_size: 5
        } 
      })
      
      if (recordsRes.data && recordsRes.data.results) {
        recentRecords.value = recordsRes.data.results.map((record, index) => ({
          id: record.id || index,
          is_correct: record.is_correct || false,
          question_content: record.question?.content || record.question_content || '题目内容',
          created_at: record.created_at || new Date().toISOString()
        }))
      }
    } catch (err) {
      console.error('获取练习记录失败:', err)
      // 保持空数组
      recentRecords.value = []
    }

  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 获取等级颜色
const getLevelColor = (level) => {
  const colors = {
    1: '#67c23a',
    2: '#409eff',
    3: '#e6a23c',
    4: '#f56c6c',
    5: '#9c27b0',
    6: '#ff5722'
  }
  return colors[level] || '#409eff'
}

// 格式化时间
const formatTime = (timeStr) => {
  try {
    const date = new Date(timeStr)
    const now = new Date()
    const diff = now - date
    
    if (diff < 60000) return '刚刚'
    if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
    return `${Math.floor(diff / 86400000)}天前`
  } catch {
    return '最近'
  }
}

// 导航方法
const goToPractice = () => router.push('/practice')
const goToExam = () => router.push('/exam')
const goToWrongBook = () => {
  router.push('/wrong-book')
}
const goToCulture = () => router.push('/culture')

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.user-center-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 40px;
}

/* 顶部横幅 */
.hero-banner {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 20px 100px;
  color: white;
  overflow: hidden;
}

.banner-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 30px;
  position: relative;
  z-index: 1;
}

.user-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 4px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  flex-shrink: 0;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-avatar {
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: bold;
  color: white;
}

.user-basic-info {
  flex: 1;
}

.username {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.user-tags {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.wave {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 60px;
}

.wave-fill {
  fill: #f5f7fa;
}

/* 容器 */
.container {
  max-width: 1200px;
  margin: -60px auto 0;
  padding: 0 20px;
  position: relative;
  z-index: 2;
}

/* 核心统计 */
.core-stats {
  margin-bottom: 30px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  border-left: 4px solid;
}

.stat-card.primary { border-left-color: #409eff; }
.stat-card.success { border-left-color: #67c23a; }
.stat-card.warning { border-left-color: #e6a23c; }
.stat-card.info { border-left-color: #9c27b0; }

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  font-size: 48px;
  line-height: 1;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-trend {
  font-size: 13px;
  color: #67c23a;
}

.stat-progress {
  margin-top: 8px;
}

/* 主内容区 */
.main-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.section-header h2 {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
}

.section-header p {
  font-size: 14px;
  color: #909399;
  margin: 4px 0 0 0;
}

/* HSK等级进度 */
.level-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.level-item {
  padding: 16px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border: 2px solid #e8eaed;
  transition: all 0.3s;
}

.level-item:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.level-badge {
  font-size: 16px;
  font-weight: 700;
  padding: 6px 16px;
  border-radius: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.level-percentage {
  font-size: 20px;
  font-weight: 700;
  color: #667eea;
}

.level-stats {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  font-size: 13px;
  color: #606266;
}

/* 学习趋势图表 */
.chart-container {
  min-height: 200px;
}

.trend-chart {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  height: 200px;
  padding: 20px 0;
}

.chart-bar {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  min-width: 15px;
  max-width: 40px;
}

.bar-fill {
  width: 100%;
  min-height: 20px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px 8px 0 0;
  position: relative;
  transition: all 0.3s;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 8px;
}

.bar-fill:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.bar-value {
  font-size: 11px;
  font-weight: 700;
  color: white;
}

.bar-label {
  font-size: 10px;
  color: #909399;
  white-space: nowrap;
  transform: rotate(-45deg);
  transform-origin: center center;
  margin-top: 15px;
}

/* 最近练习 */
.recent-list {
  max-height: 400px;
  overflow-y: auto;
}

.recent-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  transition: all 0.3s;
}

.recent-item:hover {
  background: #f8f9fa;
}

.recent-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}

.recent-icon.correct {
  background: #f0f9ff;
  color: #67c23a;
}

.recent-icon.wrong {
  background: #fff5f5;
  color: #f56c6c;
}

.recent-content {
  flex: 1;
  min-width: 0;
}

.recent-question {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recent-time {
  font-size: 12px;
  color: #909399;
}

/* 快速入口 */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.action-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border: 2px solid #e8eaed;
  cursor: pointer;
  transition: all 0.3s;
}

.action-card:hover {
  border-color: #667eea;
  background: linear-gradient(135deg, #f5f7ff 0%, #ffffff 100%);
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
}

.action-icon {
  font-size: 32px;
  color: #667eea;
}

.action-card span {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.empty-chart {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
}

.empty-recent {
  padding: 20px 0;
}

/* 响应式 */
@media (max-width: 968px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .banner-content {
    flex-direction: column;
    text-align: center;
  }
  
  .username {
    font-size: 28px;
  }
  
  .user-tags {
    justify-content: center;
  }
  
  .trend-chart {
    gap: 4px;
  }
  
  .bar-label {
    font-size: 10px;
  }
}
</style>
