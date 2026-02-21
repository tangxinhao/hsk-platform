<template>
  <div class="exam-detail-page">
    <div class="exam-container">
      <!-- 顶部信息栏 -->
      <div class="exam-header">
        <div class="exam-info">
          <h2>{{ examTitle }}</h2>
          <div class="exam-meta">
            <el-tag type="primary">{{ currentQuestionIndex + 1 }} / {{ questions.length }}</el-tag>
            <el-tag type="warning">
              <el-icon><Clock /></el-icon>
              剩余时间: {{ formatTime(remainingTime) }}
            </el-tag>
          </div>
        </div>
        <div class="exam-actions">
          <el-button @click="handleAbandon" type="danger" plain>放弃考试</el-button>
          <el-button v-if="currentQuestionIndex < questions.length - 1" @click="nextQuestion" type="primary">下一题</el-button>
          <el-button v-else @click="handleSubmit" type="success">提交试卷</el-button>
        </div>
      </div>

      <!-- 题目内容 -->
      <div class="exam-content" v-if="currentQuestion" v-loading="loading">
        <el-card class="question-card">
          <div class="question-header">
            <el-tag :type="getQuestionTypeColor(currentQuestion.type)">
              {{ getQuestionTypeLabel(currentQuestion.type) }}
            </el-tag>
            <span class="question-number">第 {{ currentQuestionIndex + 1 }} 题</span>
          </div>

          <div class="question-content">
            <p class="question-text">{{ currentQuestion.content }}</p>
            
            <!-- 听力题音频 -->
            <div v-if="currentQuestion.audio_url" class="audio-player">
              <audio controls :src="currentQuestion.audio_url" style="width: 100%; margin-top: 15px;">
                您的浏览器不支持音频播放
              </audio>
              <p class="audio-tip">
                <el-icon><Headset /></el-icon>
                音频时长：{{ currentQuestion.audio_duration || 0 }}秒
              </p>
            </div>
          </div>

          <div class="answer-section">
            <!-- 单选题 -->
            <el-radio-group 
              v-if="currentQuestion.type === 'single' || currentQuestion.type === 'listening' || currentQuestion.type === 'reading'" 
              v-model="answers[currentQuestion.id]"
              class="answer-options"
            >
              <el-radio 
                v-for="(option, index) in parseOptions(currentQuestion.options)" 
                :key="index"
                :label="option"
                size="large"
              >
                {{ String.fromCharCode(65 + index) }}. {{ option }}
              </el-radio>
            </el-radio-group>

            <!-- 多选题 -->
            <el-checkbox-group 
              v-else-if="currentQuestion.type === 'multiple'" 
              v-model="answers[currentQuestion.id]"
              class="answer-options"
            >
              <el-checkbox 
                v-for="(option, index) in parseOptions(currentQuestion.options)" 
                :key="index"
                :label="option"
                size="large"
              >
                {{ String.fromCharCode(65 + index) }}. {{ option }}
              </el-checkbox>
            </el-checkbox-group>

            <!-- 判断题 -->
            <el-radio-group 
              v-else-if="currentQuestion.type === 'judge'" 
              v-model="answers[currentQuestion.id]"
              class="answer-options"
            >
              <el-radio label="正确" size="large">正确</el-radio>
              <el-radio label="错误" size="large">错误</el-radio>
            </el-radio-group>

            <!-- 填空题 -->
            <el-input
              v-else-if="currentQuestion.type === 'fill'"
              v-model="answers[currentQuestion.id]"
              placeholder="请输入答案"
              size="large"
              class="fill-input"
            />
          </div>
        </el-card>

        <!-- 题目导航 -->
        <el-card class="question-nav">
          <h3>答题卡</h3>
          <div class="nav-grid">
            <div
              v-for="(q, index) in questions"
              :key="q.id"
              :class="['nav-item', {
                'active': index === currentQuestionIndex,
                'answered': answers[q.id] !== undefined && answers[q.id] !== ''
              }]"
              @click="jumpToQuestion(index)"
            >
              {{ index + 1 }}
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Clock, Headset } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const examId = ref(null)
const examTitle = ref('')
const questions = ref([])
const currentQuestionIndex = ref(0)
const answers = ref({})
const remainingTime = ref(0)
let timer = null

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])

// 加载考试数据
const loadExam = async () => {
  loading.value = true
  try {
    const setId = route.query.setId
    examTitle.value = route.query.title || '模拟考试'
    const timeLimit = parseInt(route.query.timeLimit) || 45
    remainingTime.value = timeLimit * 60 // 转换为秒

    // 获取题目列表
    const response = await axios.get(`/question/sets/${setId}/questions/`)
    questions.value = response.data.questions || response.data
    
    console.log('加载的题目:', questions.value)

    // 初始化答案对象
    questions.value.forEach(q => {
      answers.value[q.id] = q.type === 'multiple' ? [] : ''
    })

    // 启动计时器
    startTimer()

  } catch (error) {
    console.error('加载考试失败:', error)
    ElMessage.error('加载考试失败')
    router.back()
  } finally {
    loading.value = false
  }
}

// 启动计时器
const startTimer = () => {
  timer = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--
    } else {
      clearInterval(timer)
      ElMessage.warning('考试时间到！')
      handleSubmit()
    }
  }, 1000)
}

// 格式化时间
const formatTime = (seconds) => {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

// 解析选项
const parseOptions = (options) => {
  try {
    let parsed = options
    if (typeof options === 'string') {
      parsed = JSON.parse(options)
    }
    
    // 处理新格式：{option_type: 'text', options: [{label, text, value}]}
    if (parsed && typeof parsed === 'object' && parsed.options && Array.isArray(parsed.options)) {
      return parsed.options
    }
    
    // 处理旧格式：直接是数组
    if (Array.isArray(parsed)) {
      return parsed.map((opt, idx) => {
        if (typeof opt === 'string') {
          return {
            label: String.fromCharCode(65 + idx),
            text: opt,
            value: opt  // 使用原始字符串作为value
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

// 获取题目类型颜色
const getQuestionTypeColor = (type) => {
  const colorMap = {
    'single': 'primary',
    'multiple': 'success',
    'judge': 'warning',
    'fill': 'info',
    'listening': 'danger'
  }
  return colorMap[type] || 'info'
}

// 获取题目类型标签
const getQuestionTypeLabel = (type) => {
  const labelMap = {
    'single': '单选题',
    'multiple': '多选题',
    'judge': '判断题',
    'fill': '填空题',
    'listening': '听力题',
    'reading': '阅读题'
  }
  return labelMap[type] || type
}

// 下一题
const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  }
}

// 跳转到指定题目
const jumpToQuestion = (index) => {
  currentQuestionIndex.value = index
}

// 放弃考试
const handleAbandon = async () => {
  try {
    const confirmed = await ElMessageBox.confirm(
      '确定要放弃本次考试吗？已答题目将不会保存。',
      '放弃考试',
      {
        confirmButtonText: '确定放弃',
        cancelButtonText: '继续考试',
        type: 'warning'
      }
    ).catch(() => false)

    if (confirmed) {
      clearInterval(timer)
      ElMessage.info('已放弃考试')
      router.push('/exam')
    }
  } catch (error) {
    console.error('放弃考试失败:', error)
  }
}

// 提交试卷
const handleSubmit = async () => {
  try {
    // 检查未作答题目
    const unanswered = questions.value.filter(q => {
      const answer = answers.value[q.id]
      return answer === undefined || answer === '' || (Array.isArray(answer) && answer.length === 0)
    })

    if (unanswered.length > 0) {
      const confirmed = await ElMessageBox.confirm(
        `还有 ${unanswered.length} 道题未作答，确定要提交吗？`,
        '提交确认',
        {
          confirmButtonText: '确定提交',
          cancelButtonText: '继续答题',
          type: 'warning'
        }
      ).catch(() => false)

      if (!confirmed) return
    }

    clearInterval(timer)
    loading.value = true

    // 计算得分
    let correctCount = 0
    questions.value.forEach(q => {
      const userAnswer = answers.value[q.id]
      if (Array.isArray(userAnswer)) {
        if (userAnswer.sort().join(',') === q.answer) {
          correctCount++
        }
      } else {
        if (userAnswer === q.answer) {
          correctCount++
        }
      }
    })

    const score = Math.round((correctCount / questions.value.length) * 100)

    ElMessage.success(`考试完成！得分：${score}分`)

    // 跳转到成绩页面
    router.push({
      name: 'ExamResult',
      query: {
        score: score,
        total: questions.value.length,
        correct: correctCount,
        title: examTitle.value
      }
    })

  } catch (error) {
    console.error('提交试卷失败:', error)
    ElMessage.error('提交失败，请重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadExam()
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped>
.exam-detail-page {
  min-height: calc(100vh - 64px);
  background: #F8F9FA;
  padding: 20px;
}

.exam-container {
  max-width: 1200px;
  margin: 0 auto;
}

.exam-header {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.exam-info h2 {
  margin: 0 0 10px 0;
  color: #333333;
}

.exam-meta {
  display: flex;
  gap: 15px;
}

.exam-actions {
  display: flex;
  gap: 10px;
}

.exam-content {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 20px;
}

.question-card {
  height: fit-content;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.question-number {
  font-size: 16px;
  font-weight: 600;
  color: #666;
}

.question-content {
  margin-bottom: 30px;
}

.question-text {
  font-size: 18px;
  line-height: 1.8;
  color: #333333;
  margin-bottom: 20px;
}

.audio-player {
  background: #FFFFFF;
  border: 1px solid #6699CC;
  padding: 15px;
  border-radius: 8px;
  border: 1px solid #b3d8ff;
}

.audio-tip {
  margin: 10px 0 0;
  font-size: 14px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 5px;
}

.answer-section {
  margin-top: 20px;
}

.answer-options :deep(.el-radio),
.answer-options :deep(.el-checkbox) {
  display: block;
  margin: 15px 0;
  padding: 15px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.answer-options :deep(.el-radio:hover),
.answer-options :deep(.el-checkbox:hover) {
  border-color: #6699CC;
  background: #f5f7ff;
}

.answer-options :deep(.el-radio.is-checked),
.answer-options :deep(.el-checkbox.is-checked) {
  border-color: #6699CC;
  background: #f0f4ff;
}

.fill-input {
  margin-top: 15px;
}

.question-nav {
  height: fit-content;
  position: sticky;
  top: 20px;
}

.question-nav h3 {
  margin: 0 0 15px 0;
  color: #333333;
}

.nav-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 10px;
}

.nav-item {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
}

.nav-item:hover {
  border-color: #6699CC;
  background: #f5f7ff;
}

.nav-item.active {
  border-color: #6699CC;
  background: #667eea;
  color: white;
}

.nav-item.answered {
  background: #67c23a;
  color: white;
  border-color: #67c23a;
}

.nav-item.answered.active {
  background: #667eea;
  border-color: #6699CC;
}

@media (max-width: 768px) {
  .exam-content {
    grid-template-columns: 1fr;
  }
  
  .question-nav {
    position: static;
  }
}
</style>
