<template>
  <div class="listening-practice-page">
    <div class="container">
      <div class="page-header">
        <div class="header-left">
          <h1 class="page-title">
            <el-icon :size="32" color="#fff"><Headset /></el-icon>
            听力题组练习
          </h1>
          <p class="page-subtitle">一段音频，多道题目</p>
        </div>
        <div class="header-filters">
          <el-select v-model="selectedLevel" placeholder="选择HSK等级" clearable style="width: 200px;" @change="filterByLevel">
            <el-option label="全部等级" :value="null" />
            <el-option label="HSK 1" :value="1" />
            <el-option label="HSK 2" :value="2" />
            <el-option label="HSK 3" :value="3" />
            <el-option label="HSK 4" :value="4" />
            <el-option label="HSK 5" :value="5" />
            <el-option label="HSK 6" :value="6" />
          </el-select>
        </div>
      </div>

      <!-- 题组列表 -->
      <div class="groups-container">
        <div v-if="filteredGroups.length === 0 && !loading" class="empty-state">
          <el-empty description="该等级暂无听力题组">
            <el-button @click="selectedLevel = null">查看全部</el-button>
          </el-empty>
        </div>
        <el-row v-else :gutter="24" v-loading="loading">
          <el-col
            v-for="group in filteredGroups"
            :key="group.material_group"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
          >
            <el-card class="group-card" shadow="hover" @click="startPractice(group)">
              <div class="group-header">
                <el-tag type="success" size="small">听力题组</el-tag>
                <el-tag type="info" size="small">HSK {{ group.level }}</el-tag>
              </div>

              <div class="group-content">
                <h3 class="group-title">{{ group.title }}</h3>
                <div class="group-meta">
                  <div class="meta-item">
                    <el-icon><Document /></el-icon>
                    <span>{{ group.question_count }} 题</span>
                  </div>
                  <div class="meta-item">
                    <el-icon><Clock /></el-icon>
                    <span>{{ formatDuration(group.audio_duration) }}</span>
                  </div>
                  <div class="meta-item">
                    <el-icon><CaretRight /></el-icon>
                    <span>{{ group.play_times }} 次</span>
                  </div>
                </div>
              </div>

              <div class="group-footer">
                <el-button type="primary" size="small" plain>
                  <el-icon><CaretRight /></el-icon>
                  开始练习
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- 练习对话框 -->
    <el-dialog
      v-model="practiceDialogVisible"
      :title="currentGroup.title"
      fullscreen
      :close-on-click-modal="false"
      class="practice-dialog"
    >
      <div v-if="currentGroup" class="listening-practice-container">
        <!-- 左侧：音频播放区 -->
        <div class="audio-panel">
          <div class="audio-header">
            <h3>
              <el-icon><Headset /></el-icon>
              听力材料
            </h3>
            <el-tag type="info">HSK {{ currentGroup.level }}</el-tag>
          </div>

          <div class="audio-player-box">
            <audio 
              v-if="currentGroup.audio_url"
              :src="currentGroup.audio_url" 
              controls 
              style="width: 100%;"
              @error="handleAudioError"
            >
              您的浏览器不支持音频播放
            </audio>
            <div class="play-info">
              <div class="info-row">
                <el-icon><Clock /></el-icon>
                <span>音频时长: {{ formatDuration(currentGroup.audio_duration) }}</span>
              </div>
              <div class="info-row">
                <el-icon><RefreshRight /></el-icon>
                <span>剩余播放次数: {{ remainingPlays }}</span>
              </div>
            </div>
          </div>

          <div class="tips-box">
            <h4>答题提示</h4>
            <ul>
              <li>请先仔细听音频</li>
              <li>每道题目可以单独提交</li>
              <li>切换题目不影响已答题目</li>
              <li>所有题目完成后点击"完成练习"</li>
            </ul>
          </div>
        </div>

        <!-- 右侧：题目区（滚动显示） -->
        <div class="questions-panel">
          <div class="questions-header">
            <h3>题目列表</h3>
            <div class="progress-text">
              已完成：{{ completedCount }} / {{ groupQuestions.length }}
            </div>
          </div>
          
          <div class="questions-scroll-container">
            <div 
              v-for="(question, index) in groupQuestions" 
              :key="question.id"
              class="question-item"
              :class="{ 'completed': submitted && questionStatus[question.id] }"
            >
              <!-- 题目信息 -->
              <div class="question-header-bar">
                <div class="question-number-badge">第{{ index + 1 }}题</div>
                <div class="question-meta">
                  <el-tag size="small">{{ getTypeLabel(question.type) }}</el-tag>
                  <el-tag type="warning" size="small" v-if="question.difficulty">
                    {{ '★'.repeat(question.difficulty) }}
                  </el-tag>
                </div>
                <div class="question-status">
                  <el-icon v-if="questionStatus[question.id] === 'correct'" class="status-icon correct" :size="20">
                    <CircleCheck />
                  </el-icon>
                  <el-icon v-else-if="questionStatus[question.id] === 'wrong'" class="status-icon wrong" :size="20">
                    <CircleClose />
                  </el-icon>
                </div>
              </div>
              
              <!-- 题目内容 -->
              <div class="question-text">
                <p>{{ question.content }}</p>
              </div>
                
              <!-- 选项 -->
              <div class="options-container">
                <div
                  v-for="(option, optIndex) in parseOptions(question.options)"
                  :key="optIndex"
                  class="option-card"
                  :class="{ 
                    'is-selected': userAnswers[question.id] === getOptionValue(option, optIndex),
                    'is-correct': questionStatus[question.id] && option.value === question.answer,
                    'is-wrong': questionStatus[question.id] === 'wrong' && userAnswers[question.id] === getOptionValue(option, optIndex)
                  }"
                    @click="selectAnswer(question.id, getOptionValue(option, optIndex))"
                >
                  <div class="option-label">{{ String.fromCharCode(65 + optIndex) }}</div>
                  <div class="option-text">{{ getOptionText(option) }}</div>
                  <div class="option-check">
                    <el-icon v-if="userAnswers[question.id] === getOptionValue(option, optIndex)">
                      <Check />
                    </el-icon>
                  </div>
                </div>
              </div>
                
              <!-- 答案结果 -->
                <div v-if="submitted" class="result-box" :class="questionStatus[question.id]">
                <div class="result-icon">
                  <el-icon v-if="questionStatus[question.id] === 'correct'"><CircleCheck /></el-icon>
                  <el-icon v-else><CircleClose /></el-icon>
                </div>
                <div class="result-text">
                  <h4>{{ questionStatus[question.id] === 'correct' ? '回答正确！' : '回答错误' }}</h4>
                  <p>正确答案：<strong>{{ question.answer }}</strong></p>
                  <p v-if="question.explanation" class="explanation">{{ question.explanation }}</p>
                </div>
              </div>
              
            </div>
          </div>
          
          <!-- 提交与完成按钮 -->
          <div class="finish-section" v-if="groupQuestions.length > 0">
            <div class="finish-actions">
              <el-button 
                type="primary" 
                size="large" 
                @click="submitAllAnswers"
                :disabled="submitted"
              >
                <el-icon><Check /></el-icon>
                提交本组
              </el-button>
              <el-button 
                v-if="submitted" 
                type="success" 
                size="large" 
                @click="finishPractice"
              >
                <el-icon><Select /></el-icon>
                完成练习
              </el-button>
            </div>
            <div v-if="submitted" class="summary-text">
              已判分：{{ Object.values(questionStatus).filter(s => s === 'correct').length }} / {{ groupQuestions.length }}
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Headset, Document, Clock, CaretRight, Check, Close, ArrowRight, 
  CircleCheck, CircleClose, RefreshRight, Select
} from '@element-plus/icons-vue'
import axios from 'axios'

const loading = ref(false)
const listeningGroups = ref([])
const selectedLevel = ref(null)
const filteredGroups = computed(() => {
  if (!selectedLevel.value) {
    return listeningGroups.value
  }
  return listeningGroups.value.filter(group => {
    return group.level === selectedLevel.value
  })
})

const practiceDialogVisible = ref(false)
const currentGroup = ref({})
const groupQuestions = ref([])
const userAnswers = ref({})
const questionStatus = ref({})
const submitted = ref(false)
const remainingPlays = ref(0)
const completedCount = computed(() => {
  return submitted.value ? groupQuestions.value.length : 0
})

const filterByLevel = () => {
  console.log('选择等级:', selectedLevel.value)
}

const loadGroups = async () => {
  try {
    loading.value = true
    axios.defaults.baseURL = '/api'
    console.log('加载听力题组列表...')
    const response = await axios.get('/question/listening-groups/')
    console.log('题组列表响应:', response.data)
    
    const results = response.data.results || response.data || []
    listeningGroups.value = Array.isArray(results) ? results : []
    
    console.log('已加载题组数量:', listeningGroups.value.length)
    
    if (listeningGroups.value.length === 0) {
      ElMessage.warning('暂无听力题组数据')
    }
  } catch (error) {
    console.error('加载题组失败:', error)
    ElMessage.error('加载题组失败')
  } finally {
    loading.value = false
  }
}

const startPractice = async (group) => {
  try {
    console.log('开始练习题组:', group.material_group)
    const response = await axios.get(`/question/listening-group/${group.material_group}/`)
    console.log('题组详情:', response.data)
    
    currentGroup.value = response.data.material
    // 确保音频URL是可访问的绝对路径
    if (currentGroup.value && currentGroup.value.audio_url && !currentGroup.value.audio_url.startsWith('http')) {
      const origin = window.location.origin
      currentGroup.value.audio_url = origin + currentGroup.value.audio_url
    }
    groupQuestions.value = response.data.questions || []
    remainingPlays.value = currentGroup.value.play_times
    practiceDialogVisible.value = true
    
    // 重置答题状态
    userAnswers.value = {}
    questionStatus.value = {}
  } catch (error) {
    console.error('获取题组详情失败:', error)
    ElMessage.error('获取题组详情失败')
  }
}

const selectAnswer = (questionId, answer) => {
  if (submitted.value) return
  userAnswers.value[questionId] = answer
}

const submitAllAnswers = () => {
  if (!groupQuestions.value.length) return
  // 检查是否有未答题
  const unanswered = groupQuestions.value.filter(q => !userAnswers.value[q.id])
  if (unanswered.length > 0) {
    ElMessage.warning(`还有 ${unanswered.length} 题未作答`)
    return
  }

  groupQuestions.value.forEach(q => {
    const isCorrect = userAnswers.value[q.id] === q.answer
    questionStatus.value[q.id] = isCorrect ? 'correct' : 'wrong'
  })
  submitted.value = true

  const correctCount = Object.values(questionStatus.value).filter(s => s === 'correct').length
  const totalCount = groupQuestions.value.length
  const score = Math.round((correctCount / totalCount) * 100)
  ElMessage.success(`本组完成，得分：${score}分 (${correctCount}/${totalCount})`)
}

const finishPractice = () => {
  practiceDialogVisible.value = false
}

const formatDuration = (seconds) => {
  if (!seconds) return '0秒'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return mins > 0 ? `${mins}分${secs}秒` : `${secs}秒`
}

const parseOptions = (options) => {
  try {
    if (!options) return []
    const parsed = typeof options === 'string' ? JSON.parse(options) : options
    
    if (parsed && typeof parsed === 'object' && parsed.options && Array.isArray(parsed.options)) {
      return parsed.options
    }
    
    if (Array.isArray(parsed)) {
      return parsed.map((opt, idx) => {
        if (typeof opt === 'string') {
          return { label: String.fromCharCode(65 + idx), text: opt, value: String.fromCharCode(65 + idx) }
        }
        return opt
      })
    }
    
    return []
  } catch (e) {
    console.error('解析选项失败:', e)
    return []
  }
}

const getOptionValue = (option, index) => {
  if (typeof option === 'object' && option.value !== undefined) {
    return option.value
  }
  if (typeof option === 'object' && option.label !== undefined) {
    return option.label
  }
  return String.fromCharCode(65 + index)
}

const getOptionText = (option) => {
  if (typeof option === 'string') {
    return option
  }
  if (typeof option === 'object') {
    return option.text || option.label || option.value || ''
  }
  return ''
}

const getTypeLabel = (type) => {
  const labels = {
    'single': '单选题',
    'multiple': '多选题',
    'judge': '判断题'
  }
  return labels[type] || '单选题'
}

const handleAudioError = (e) => {
  console.error('音频加载失败:', e)
  ElMessage.error('音频文件加载失败，请检查文件路径')
}

onMounted(() => {
  axios.defaults.baseURL = '/api'
  console.log('听力题组练习页面已挂载，开始加载数据...')
  loadGroups()
})
</script>

<style scoped>
.listening-practice-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
  padding: 40px 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  padding: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  color: white;
}

.header-left {
  flex: 1;
}

.header-filters {
  display: flex;
  gap: 16px;
}

.page-title {
  font-size: 36px;
  font-weight: bold;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-subtitle {
  font-size: 18px;
  opacity: 0.95;
  margin: 0;
}

.empty-state {
  padding: 80px 20px;
  text-align: center;
}

.groups-container {
  margin-top: 32px;
}

.group-card {
  margin-bottom: 24px;
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 12px;
  overflow: hidden;
}

.group-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.group-content {
  margin-bottom: 16px;
}

.group-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #303133;
  line-height: 1.5;
}

.group-meta {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
}

.group-footer {
  text-align: right;
}

/* 练习对话框 */
.practice-dialog :deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 24px;
}

.practice-dialog :deep(.el-dialog__title) {
  color: white;
  font-size: 20px;
  font-weight: 600;
}

.practice-dialog :deep(.el-dialog__close) {
  color: white;
}

.practice-dialog :deep(.el-dialog__body) {
  padding: 0;
  overflow: hidden; /* 避免整个弹窗滚动，右侧内部滚动 */
}

.listening-practice-container {
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: 0;
  height: calc(100vh - 100px);
  overflow: hidden; /* 让内部区域自行滚动 */
}

/* 音频面板 */
.audio-panel {
  position: sticky;
  top: 0;
  align-self: start;
  background: #f8f9fa;
  padding: 24px;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: calc(100vh - 140px);
  overflow-y: auto;
}

.audio-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.audio-header h3 {
  font-size: 18px;
  color: #303133;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.audio-player-box {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.play-info {
  margin-top: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
}

.tips-box {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.tips-box h4 {
  margin: 0 0 12px 0;
  font-size: 16px;
  color: #303133;
}

.tips-box ul {
  margin: 0;
  padding-left: 20px;
  list-style: disc;
}

.tips-box li {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
}

/* 题目面板 */
.questions-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden; /* 由内部容器滚动 */
  background: white;
}

.questions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 2px solid #f0f0f0;
  background: white;
}

.questions-header h3 {
  font-size: 18px;
  color: #303133;
  margin: 0;
}

.progress-text {
  font-size: 14px;
  color: #409eff;
  font-weight: 600;
}

.questions-scroll-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  max-height: calc(100vh - 140px); /* 限制滚动区域高度 */
}

.question-item {
  background: white;
  border: 2px solid #e4e7ed;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.question-item.completed {
  border-color: #67c23a;
  background: #f0f9ff;
}

.question-header-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.question-number-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 16px;
}

.status-icon {
  font-size: 20px;
}

.status-icon.correct {
  color: #67c23a;
}

.status-icon.wrong {
  color: #f56c6c;
}

.question-status {
  margin-left: auto;
}

.finish-section {
  padding: 20px;
  text-align: center;
  border-top: 2px solid #f0f0f0;
  background: #f9fafb;
}
.finish-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  align-items: center;
}
.summary-text {
  margin-top: 12px;
  color: #606266;
}

.question-meta {
  display: flex;
  gap: 8px;
}

.question-text {
  margin: 16px 0 24px 0;
}

.question-text p {
  font-size: 18px;
  line-height: 1.8;
  color: #303133;
  margin: 0;
}

.options-container {
  display: grid;
  gap: 16px;
  margin-bottom: 24px;
}

.option-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: #f8f9fa;
  border: 2px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-card:hover {
  border-color: #667eea;
  background: #f0f2ff;
}

.option-card.is-selected {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
}

.option-card.is-correct {
  border-color: #67c23a;
  background: rgba(103, 194, 58, 0.1);
}

.option-card.is-wrong {
  border-color: #f56c6c;
  background: rgba(245, 108, 108, 0.1);
}

.option-label {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: 2px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  flex-shrink: 0;
}

.option-card.is-selected .option-label {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-color: transparent;
}

.option-card.is-correct .option-label {
  background: #67c23a;
  color: white;
  border-color: transparent;
}

.option-card.is-wrong .option-label {
  background: #f56c6c;
  color: white;
  border-color: transparent;
}

.option-text {
  flex: 1;
  font-size: 16px;
  color: #303133;
  line-height: 1.6;
}

.option-check {
  width: 24px;
  font-size: 20px;
  color: #667eea;
}

.result-box {
  margin-top: 20px;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.result-box.correct {
  background: rgba(103, 194, 58, 0.1);
  border: 2px solid #67c23a;
}

.result-box.wrong {
  background: rgba(245, 108, 108, 0.1);
  border: 2px solid #f56c6c;
}

.result-icon {
  font-size: 32px;
}

.result-box.correct .result-icon {
  color: #67c23a;
}

.result-box.wrong .result-icon {
  color: #f56c6c;
}

.result-text h4 {
  margin: 0 0 8px 0;
  font-size: 18px;
}

.result-text p {
  margin: 4px 0;
  font-size: 14px;
  color: #606266;
}

.explanation {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  font-style: italic;
}

.question-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>
