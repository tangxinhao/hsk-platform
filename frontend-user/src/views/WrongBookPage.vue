<template>
  <div class="wrong-book-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-content">
          <div class="header-left">
            <h1>
              <el-icon><Warning /></el-icon>
              我的错题本
            </h1>
            <p>复习错题，查漏补缺，提升正确率</p>
          </div>
          <div class="header-actions">
            <el-button type="danger" :icon="Delete" @click="clearMasteredQuestions">
              清除已掌握
            </el-button>
            <el-button type="primary" :icon="Refresh" @click="loadWrongQuestions">
              刷新
            </el-button>
          </div>
        </div>
      </div>

      <!-- 统计卡片 -->
      <div class="stats-section">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #fef0f0;">
                <el-icon color="#f56c6c" :size="32"><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ total }}</div>
                <div class="stat-label">错题总数</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #f0f9ff;">
                <el-icon color="#409eff" :size="32"><Edit /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ reviewedCount }}</div>
                <div class="stat-label">已复习</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #f0f9ff;">
                <el-icon color="#67c23a" :size="32"><CircleCheck /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ masteredCount }}</div>
                <div class="stat-label">已掌握</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #fdf6ec;">
                <el-icon color="#e6a23c" :size="32"><TrendCharts /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ improvementRate }}%</div>
                <div class="stat-label">提升率</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-section">
        <el-select v-model="filters.level" placeholder="HSK等级" clearable @change="loadWrongQuestions">
          <el-option label="全部等级" :value="0"></el-option>
          <el-option label="HSK 1" :value="1"></el-option>
          <el-option label="HSK 2" :value="2"></el-option>
          <el-option label="HSK 3" :value="3"></el-option>
          <el-option label="HSK 4" :value="4"></el-option>
          <el-option label="HSK 5" :value="5"></el-option>
          <el-option label="HSK 6" :value="6"></el-option>
        </el-select>

        <el-select v-model="filters.type" placeholder="题目类型" clearable @change="loadWrongQuestions">
          <el-option label="全部类型" value=""></el-option>
          <el-option label="单选题" value="single"></el-option>
          <el-option label="多选题" value="multiple"></el-option>
          <el-option label="判断题" value="judge"></el-option>
          <el-option label="填空题" value="fill"></el-option>
          <el-option label="阅读题" value="reading"></el-option>
        </el-select>

        <el-radio-group v-model="filters.status" @change="loadWrongQuestions">
          <el-radio-button :value="'all'">全部</el-radio-button>
          <el-radio-button :value="'unreviewed'">未复习</el-radio-button>
          <el-radio-button :value="'reviewed'">已复习</el-radio-button>
          <el-radio-button :value="'mastered'">已掌握</el-radio-button>
        </el-radio-group>

        <el-button type="primary" @click="startAllPractice" :disabled="wrongQuestions.length === 0">
          <el-icon><VideoPlay /></el-icon>
          开始练习全部
        </el-button>
      </div>

      <!-- 错题列表 -->
      <div class="questions-section" v-loading="loading">
        <el-empty v-if="wrongQuestions.length === 0 && !loading" description="暂无错题">
          <el-button type="primary" @click="$router.push('/practice')">去练习</el-button>
        </el-empty>

        <div v-else class="questions-grid">
          <el-card
            v-for="item in wrongQuestions"
            :key="item.id"
            class="question-card"
            :class="{
              'is-mastered': item.is_mastered,
              'is-reviewed': item.reviewed_count > 0
            }"
            shadow="hover"
          >
            <div class="question-header">
              <div class="question-meta">
                <el-tag type="danger" size="small">
                  <el-icon><Warning /></el-icon> 错题
                </el-tag>
                <el-tag :type="getTypeColor(item.question.type)" size="small">
                  {{ getTypeLabel(item.question.type) }}
                </el-tag>
                <el-tag type="info" size="small">HSK {{ item.question.level }}</el-tag>
                <el-tag v-if="item.is_mastered" type="success" size="small">
                  <el-icon><CircleCheck /></el-icon> 已掌握
                </el-tag>
              </div>
              <div class="question-actions">
                <el-button
                  :icon="item.is_mastered ? CircleCheckFilled : CircleCheck"
                  :type="item.is_mastered ? 'success' : ''"
                  circle
                  size="small"
                  @click.stop="toggleMastered(item)"
                  title="标记掌握"
                />
                <el-button
                  :icon="Delete"
                  circle
                  size="small"
                  @click.stop="removeFromWrongBook(item)"
                  title="移除"
                />
              </div>
            </div>

            <div class="question-content">
              <div class="question-text">
                {{ item.question.content.length > 100 ? item.question.content.substring(0, 100) + '...' : item.question.content }}
              </div>
            </div>

            <div class="wrong-info">
              <div class="wrong-meta">
                <span class="wrong-item">
                  <el-icon><Clock /></el-icon>
                  错误 {{ item.wrong_count || 1 }} 次
                </span>
                <span class="wrong-item" v-if="item.last_reviewed_at">
                  <el-icon><View /></el-icon>
                  {{ formatTime(item.last_reviewed_at) }}
                </span>
                <span class="wrong-item" v-if="item.reviewed_count > 0">
                  <el-icon><Refresh /></el-icon>
                  复习 {{ item.reviewed_count }} 次
                </span>
              </div>
            </div>

            <div class="question-footer">
              <el-button type="primary" size="small" @click="startPractice(item.question)">
                <el-icon><Edit /></el-icon>
                重新练习
              </el-button>
            </div>
          </el-card>
        </div>

        <!-- 分页 -->
        <el-pagination
          v-if="total > pageSize"
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 48]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadWrongQuestions"
          @current-change="loadWrongQuestions"
          class="pagination"
        />
      </div>
    </div>

    <!-- 练习对话框 -->
    <el-dialog
      v-model="practiceDialog"
      title="错题练习"
      width="800px"
      :close-on-click-modal="false"
    >
      <div v-if="currentPracticeQuestion" class="practice-content">
        <div class="question-info">
          <el-tag :type="getTypeColor(currentPracticeQuestion.type)">
            {{ getTypeLabel(currentPracticeQuestion.type) }}
          </el-tag>
          <el-tag type="info">HSK {{ currentPracticeQuestion.level }}</el-tag>
          <span class="question-progress">
            第 {{ currentQuestionIndex + 1 }} / {{ practiceQuestions.length }} 题
          </span>
        </div>

        <div class="question-title">
          <h3>{{ currentPracticeQuestion.content }}</h3>
        </div>

        <div class="answer-area">
          <!-- 单选/多选/判断/填空题的答题区域 -->
          <el-radio-group 
            v-if="currentPracticeQuestion.type === 'single' || currentPracticeQuestion.type === 'reading'"
            v-model="userAnswer"
            :disabled="showAnswer"
          >
            <div
              v-for="(option, index) in parseOptions(currentPracticeQuestion.options)"
              :key="index"
              class="custom-radio-option"
              :class="{
                'is-selected': userAnswer === getOptionValue(option, index),
                'is-disabled': showAnswer
              }"
              @click="!showAnswer && (userAnswer = getOptionValue(option, index))"
            >
              <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
              <div class="option-text">{{ getOptionText(option) }}</div>
              <div v-if="userAnswer === getOptionValue(option, index)" class="option-indicator">
                <el-icon><Check /></el-icon>
              </div>
            </div>
          </el-radio-group>

          <el-radio-group
            v-else-if="currentPracticeQuestion.type === 'judge'"
            v-model="userAnswer"
            :disabled="showAnswer"
          >
            <el-radio label="正确" size="large">正确</el-radio>
            <el-radio label="错误" size="large">错误</el-radio>
          </el-radio-group>

          <el-input
            v-else-if="currentPracticeQuestion.type === 'fill'"
            v-model="userAnswer"
            placeholder="请输入答案"
            size="large"
            :disabled="showAnswer"
          />
        </div>

        <!-- 答案解析 -->
        <div v-if="showAnswer" class="answer-section">
          <el-alert
            :type="isCorrect ? 'success' : 'error'"
            :title="isCorrect ? '✓ 回答正确！' : '✗ 回答错误'"
            :closable="false"
            show-icon
          >
            <template #default>
              <div class="answer-details">
                <p><strong>正确答案:</strong> {{ currentPracticeQuestion.answer }}</p>
                <p v-if="currentPracticeQuestion.explanation">
                  <strong>题目解析:</strong> {{ currentPracticeQuestion.explanation }}
                </p>
              </div>
            </template>
          </el-alert>
        </div>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="closePractice">退出练习</el-button>
          <el-button v-if="!showAnswer" type="primary" @click="submitAnswer">
            提交答案
          </el-button>
          <el-button v-else-if="currentQuestionIndex < practiceQuestions.length - 1" type="primary" @click="nextQuestion">
            下一题
          </el-button>
          <el-button v-else type="success" @click="completePractice">
            完成练习
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Warning, Delete, Refresh, Edit, CircleCheck, CircleCheckFilled, TrendCharts,
  Clock, View, VideoPlay, Check
} from '@element-plus/icons-vue'
import axios from 'axios'

// 数据定义
const loading = ref(false)
const wrongQuestions = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const reviewedCount = ref(0)
const masteredCount = ref(0)
const improvementRate = ref(0)

// 筛选条件
const filters = reactive({
  level: 0,
  type: '',
  status: 'all'
})

// 练习相关
const practiceDialog = ref(false)
const practiceQuestions = ref([])
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const showAnswer = ref(false)
const isCorrect = ref(false)

const currentPracticeQuestion = computed(() => practiceQuestions.value[currentQuestionIndex.value])

// 加载错题列表
const loadWrongQuestions = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (filters.level) params.level = filters.level
    if (filters.type) params.type = filters.type

    const res = await axios.get('/question/wrong-book/', { params })
    
    // 假设后端返回的是WrongBook对象数组，包含question字段
    wrongQuestions.value = res.data.results || res.data || []
    total.value = res.data.count || wrongQuestions.value.length

    // 根据筛选条件过滤
    if (filters.status !== 'all') {
      wrongQuestions.value = wrongQuestions.value.filter(item => {
        if (filters.status === 'unreviewed') return !item.reviewed_count || item.reviewed_count === 0
        if (filters.status === 'reviewed') return item.reviewed_count > 0 && !item.is_mastered
        if (filters.status === 'mastered') return item.is_mastered
        return true
      })
    }

    // 计算统计数据
    reviewedCount.value = wrongQuestions.value.filter(item => item.reviewed_count > 0).length
    masteredCount.value = wrongQuestions.value.filter(item => item.is_mastered).length
    improvementRate.value = total.value > 0 ? Math.round((masteredCount.value / total.value) * 100) : 0
  } catch (error) {
    console.error('加载错题失败:', error)
    ElMessage.error('加载错题失败')
  } finally {
    loading.value = false
  }
}

// 开始练习单个题目
const startPractice = (question) => {
  practiceQuestions.value = [question]
  currentQuestionIndex.value = 0
  userAnswer.value = ''
  showAnswer.value = false
  practiceDialog.value = true
}

// 开始练习全部错题
const startAllPractice = () => {
  if (wrongQuestions.value.length === 0) {
    ElMessage.warning('没有可练习的错题')
    return
  }
  
  practiceQuestions.value = wrongQuestions.value.map(item => item.question)
  currentQuestionIndex.value = 0
  userAnswer.value = ''
  showAnswer.value = false
  practiceDialog.value = true
}

// 提交答案
const submitAnswer = async () => {
  if (!userAnswer.value) {
    ElMessage.warning('请先选择答案')
    return
  }

  try {
    const res = await axios.post('/question/answer/', {
      question_id: currentPracticeQuestion.value.id,
      user_answer: userAnswer.value.trim()
    })

    isCorrect.value = res.data.is_correct
    showAnswer.value = true

    if (isCorrect.value) {
      ElMessage.success('回答正确！')
    } else {
      ElMessage.error('回答错误，请查看解析')
    }
  } catch (error) {
    console.error('提交答案失败:', error)
    ElMessage.error('提交答案失败')
  }
}

// 下一题
const nextQuestion = () => {
  currentQuestionIndex.value++
  userAnswer.value = ''
  showAnswer.value = false
}

// 完成练习
const completePractice = () => {
  ElMessage.success('练习完成！')
  closePractice()
  loadWrongQuestions() // 刷新列表
}

// 关闭练习
const closePractice = () => {
  practiceDialog.value = false
  practiceQuestions.value = []
  currentQuestionIndex.value = 0
  userAnswer.value = ''
  showAnswer.value = false
}

// 标记掌握
const toggleMastered = (item) => {
  item.is_mastered = !item.is_mastered
  ElMessage.success(item.is_mastered ? '已标记为掌握' : '已取消掌握标记')
  // TODO: 调用后端API保存状态
}

// 从错题本移除
const removeFromWrongBook = async (item) => {
  try {
    await ElMessageBox.confirm(
      '确定要从错题本中移除这道题吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // TODO: 调用后端API删除
    wrongQuestions.value = wrongQuestions.value.filter(q => q.id !== item.id)
    total.value--
    ElMessage.success('已移除')
  } catch {
    // 取消操作
  }
}

// 清除已掌握的题目
const clearMasteredQuestions = async () => {
  const masteredItems = wrongQuestions.value.filter(item => item.is_mastered)
  
  if (masteredItems.length === 0) {
    ElMessage.info('没有已掌握的题目')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要清除 ${masteredItems.length} 道已掌握的题目吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    // TODO: 调用后端API批量删除
    wrongQuestions.value = wrongQuestions.value.filter(item => !item.is_mastered)
    total.value -= masteredItems.length
    masteredCount.value = 0
    ElMessage.success(`已清除 ${masteredItems.length} 道题目`)
  } catch {
    // 取消操作
  }
}

// 格式化时间
const formatTime = (timeStr) => {
  if (!timeStr) return ''
  
  const time = new Date(timeStr)
  const now = new Date()
  const diff = now - time
  
  const seconds = Math.floor(diff / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

// 解析选项
const parseOptions = (options) => {
  try {
    let parsed = options
    if (typeof options === 'string') {
      parsed = JSON.parse(options)
    }
    
    if (parsed && typeof parsed === 'object' && parsed.options && Array.isArray(parsed.options)) {
      return parsed.options
    }
    
    if (Array.isArray(parsed)) {
      return parsed.map((opt, idx) => {
        if (typeof opt === 'string') {
          return {
            label: String.fromCharCode(65 + idx),
            text: opt,
            value: opt
          }
        }
        return opt
      })
    }
    
    return []
  } catch (e) {
    console.error('解析选项失败:', e, options)
    return []
  }
}

const getOptionValue = (option, index) => {
  if (typeof option === 'string') return option
  return option.value || option.label || String.fromCharCode(65 + index)
}

const getOptionText = (option) => {
  if (typeof option === 'string') return option
  return option.text || option.label || option.value || ''
}

const getTypeColor = (type) => {
  const colorMap = {
    'single': 'primary',
    'multiple': 'success',
    'judge': 'warning',
    'fill': 'info',
    'reading': 'info'
  }
  return colorMap[type] || 'info'
}

const getTypeLabel = (type) => {
  const labelMap = {
    'single': '单选题',
    'multiple': '多选题',
    'judge': '判断题',
    'fill': '填空题',
    'reading': '阅读题'
  }
  return labelMap[type] || type
}

onMounted(() => {
  loadWrongQuestions()
})
</script>

<style scoped>
.wrong-book-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #F8F9FA 0%, #FFFFFF 100%);
  padding: 20px 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  background: white;
  padding: 30px;
  border-radius: 16px;
  margin-bottom: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h1 {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 28px;
  color: #303133;
  margin: 0 0 8px 0;
}

.header-left p {
  color: #909399;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-section {
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.filter-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.questions-section {
  min-height: 400px;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.question-card {
  transition: all 0.3s;
}

.question-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}

.question-card.is-mastered {
  opacity: 0.7;
  background: #f0f9ff;
}

.question-card.is-reviewed {
  border-left: 3px solid #409eff;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.question-actions {
  display: flex;
  gap: 8px;
}

.question-content {
  margin-bottom: 15px;
}

.question-text {
  font-size: 15px;
  line-height: 1.6;
  color: #303133;
}

.wrong-info {
  background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.wrong-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.wrong-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #606266;
}

.question-footer {
  display: flex;
  justify-content: flex-end;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 练习对话框样式 */
.practice-content {
  padding: 20px;
}

.question-info {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 20px;
}

.question-progress {
  margin-left: auto;
  color: #909399;
  font-size: 14px;
}

.question-title {
  margin-bottom: 30px;
}

.question-title h3 {
  font-size: 18px;
  line-height: 1.6;
  color: #303133;
}

.answer-area {
  margin-bottom: 20px;
}

.custom-radio-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 2px solid #e8eaed;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 10px;
  min-height: 40px;
}

.custom-radio-option:hover {
  border-color: #667eea;
  background: #f8f9ff;
}

.custom-radio-option.is-selected {
  border-color: #667eea;
  background: #ecf2ff;
}

.custom-radio-option.is-disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.option-label {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #606266;
  flex-shrink: 0;
}

.option-text {
  flex: 1;
  font-size: 13px;
  line-height: 1.3;
  color: #303133;
}

.option-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #667eea;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.answer-section {
  margin-top: 20px;
}

.answer-details p {
  margin: 8px 0;
  line-height: 1.6;
}
</style>
