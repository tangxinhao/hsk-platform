<template>
  <div class="exam-page">
    <!-- 顶部banner -->
    <div class="page-banner">
      <div class="banner-content">
        <div class="banner-icon">
          <el-icon :size="48"><Document /></el-icon>
        </div>
        <h1 class="banner-title">模拟考试</h1>
        <p class="banner-subtitle">选择HSK等级开始模拟考试</p>
      </div>
    </div>
    
    <div class="container">
      <!-- HSK等级选择器 -->
      <div class="level-selector-wrapper">
        <div class="level-selector">
          <div 
            v-for="level in levelOptions" 
            :key="level.value"
            class="level-card"
            :class="{ 'is-active': selectedLevel === level.value }"
            @click="selectLevel(level.value)"
          >
            <div class="level-icon">
              <el-icon :size="28">
                <component :is="level.icon" />
              </el-icon>
            </div>
            <div class="level-text">{{ level.label }}</div>
            <div class="level-count" v-if="level.value === 0">
              {{ examSets.length }} 套
            </div>
            <div class="level-count" v-else>
              {{ getLevelCount(level.value) }} 套
            </div>
          </div>
        </div>
      </div>
      
      <div class="exam-grid" v-loading="loading">
        <el-empty v-if="!loading && filteredExamSets.length === 0" description="暂无考试套卷" />
        
        <el-card
          v-for="examSet in filteredExamSets"
          :key="examSet.id"
          class="exam-card"
          shadow="hover"
        >
          <div class="exam-card-header">
            <el-tag 
              :type="getLevelTagType(examSet.level)" 
              size="large"
              effect="dark"
            >
              HSK {{ examSet.level }}
            </el-tag>
          </div>
          
          <div class="exam-card-body">
            <h3 class="exam-title">{{ examSet.title || examSet.name }}</h3>
            
            <div class="exam-meta">
              <div class="meta-item">
                <el-icon color="#409eff"><Clock /></el-icon>
                <span>{{ examSet.time_limit || examSet.duration }} 分钟</span>
              </div>
              <div class="meta-item">
                <el-icon color="#67c23a"><DocumentCopy /></el-icon>
                <span>{{ examSet.question_count || 0 }} 题</span>
              </div>
            </div>
            
            <div class="exam-description" v-if="examSet.description">
              {{ examSet.description }}
            </div>
          </div>
          
          <div class="exam-card-footer">
            <el-button 
              type="primary" 
              size="large"
              @click="startExam(examSet)"
              style="width: 100%"
            >
              <el-icon style="margin-right: 5px;"><CaretRight /></el-icon>
              开始考试
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  Clock, 
  DocumentCopy, 
  Document,
  Grid,
  Trophy,
  Star,
  Medal,
  Present,
  Orange,
  CaretRight
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()

const loading = ref(false)
const examSets = ref([])
const selectedLevel = ref(0) // 0表示全部等级

// 等级选项配置
const levelOptions = [
  { value: 0, label: '全部等级', icon: Grid },
  { value: 1, label: 'HSK 1', icon: Star },
  { value: 2, label: 'HSK 2', icon: Medal },
  { value: 3, label: 'HSK 3', icon: Trophy },
  { value: 4, label: 'HSK 4', icon: Present },
  { value: 5, label: 'HSK 5', icon: Orange },
  { value: 6, label: 'HSK 6', icon: Trophy }
]

// 根据选择的等级过滤考试套卷
const filteredExamSets = computed(() => {
  if (selectedLevel.value === 0) {
    return examSets.value
  }
  return examSets.value.filter(exam => exam.level === selectedLevel.value)
})

// 获取等级数量
const getLevelCount = (level) => {
  return examSets.value.filter(exam => exam.level === level).length
}

// 选择等级
const selectLevel = (level) => {
  selectedLevel.value = level
}

// 获取等级标签颜色
const getLevelTagType = (level) => {
  const types = ['', 'success', 'info', 'warning', 'danger', '', 'danger']
  return types[level] || 'primary'
}

const loadExamSets = async () => {
  loading.value = true
  try {
    const response = await axios.get('/question/sets/')
    examSets.value = response.data.results || response.data
  } catch (error) {
    console.error('加载考试套卷失败:', error)
    ElMessage.error('加载考试套卷失败')
  } finally {
    loading.value = false
  }
}

const startExam = async (examSet) => {
  try {
    console.log('开始考试:', examSet)
    
    // 确认是否开始考试
    const confirmed = await ElMessageBox.confirm(
      `确定开始【${examSet.title}】考试吗？考试时长 ${examSet.time_limit} 分钟。`,
      '开始考试',
      {
        confirmButtonText: '开始',
        cancelButtonText: '取消',
        type: 'info'
      }
    ).catch(() => false)
    
    if (!confirmed) return
    
    // 调用后端API开始考试
    const response = await axios.post('/question/exam/start/', {
      question_set_id: examSet.id
    })
    
    console.log('考试创建成功:', response.data)
    
    const examId = response.data.exam_id || response.data.id
    
    ElMessage.success('考试开始！')
    
    // 跳转到考试页面
    router.push({
      name: 'ExamDetail',
      params: { examId: examId },
      query: { 
        setId: examSet.id,
        title: examSet.title,
        timeLimit: examSet.time_limit
      }
    })
    
  } catch (error) {
    console.error('开始考试失败:', error)
    ElMessage.error(error.response?.data?.detail || '开始考试失败，请重试')
  }
}

onMounted(() => {
  loadExamSets()
})
</script>

<style scoped>
.exam-page {
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  min-height: 100vh;
  padding-bottom: 60px;
}

/* 顶部Banner */
.page-banner {
  padding: 30px 20px 20px;
  text-align: center;
  color: white;
}

.banner-content {
  max-width: 800px;
  margin: 0 auto;
}

.banner-icon {
  margin-bottom: 10px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-5px);
  }
}

.banner-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.banner-subtitle {
  font-size: 15px;
  opacity: 0.95;
  line-height: 1.4;
}

/* 容器 */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 等级选择器包装 */
.level-selector-wrapper {
  margin: -20px 0 30px;
  position: relative;
  z-index: 10;
}

.level-selector {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 15px;
  max-width: 1200px;
  margin: 0 auto;
}

.level-card {
  background: white;
  border-radius: 12px;
  padding: 20px 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
}

.level-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  border-color: #CCFFFF;
}

.level-card.is-active {
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  color: white;
  border-color: #CCFFFF;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  transform: translateY(-5px) scale(1.05);
}

.level-icon {
  margin-bottom: 10px;
  color: #CCFFFF;
  transition: all 0.3s;
}

.level-card.is-active .level-icon {
  color: white;
  transform: scale(1.2);
}

.level-text {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.level-count {
  font-size: 13px;
  opacity: 0.7;
  margin-top: 5px;
}

/* 考试卡片网格 */
.exam-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.exam-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.exam-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.exam-card-header {
  padding: 20px;
  background: #FFFFCC;
}

.exam-card-body {
  padding: 24px;
}

.exam-title {
  font-size: 18px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 16px 0;
  line-height: 1.5;
}

.exam-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
}

.exam-description {
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #e4e7ed;
}

.exam-card-footer {
  padding: 0 24px 24px;
}

/* 空状态 */
:deep(.el-empty) {
  padding: 60px 0;
  background: white;
  border-radius: 16px;
  grid-column: 1 / -1;
}

/* 响应式 */
@media (max-width: 768px) {
  .banner-title {
    font-size: 32px;
  }
  
  .level-selector {
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 10px;
  }
  
  .level-card {
    padding: 15px 10px;
  }
  
  .exam-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .level-selector {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
