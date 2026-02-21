<template>
  <div class="practice-page">
    <div class="container">
      <div class="page-header">
        <h1>题目练习</h1>
        <p>选择HSK等级开始练习</p>
      </div>
      
      <div class="filter-section">
        <el-card>
          <div class="filters">
            <el-select v-model="filters.level" placeholder="HSK等级" @change="loadQuestions">
              <el-option label="全部等级" :value="0"></el-option>
              <el-option label="HSK 1" :value="1"></el-option>
              <el-option label="HSK 2" :value="2"></el-option>
              <el-option label="HSK 3" :value="3"></el-option>
              <el-option label="HSK 4" :value="4"></el-option>
              <el-option label="HSK 5" :value="5"></el-option>
              <el-option label="HSK 6" :value="6"></el-option>
            </el-select>
            
            <el-select v-model="filters.type" placeholder="题目类型" @change="loadQuestions">
              <el-option label="全部类型" value=""></el-option>
              <el-option label="单选题" value="single"></el-option>
              <el-option label="多选题" value="multiple"></el-option>
              <el-option label="判断题" value="judge"></el-option>
              <el-option label="填空题" value="fill"></el-option>
              <el-option label="阅读题" value="reading"></el-option>
              <el-option label="书写题" value="writing"></el-option>
            </el-select>
            
            <el-button type="primary" @click="loadQuestions">搜索</el-button>
          </div>
        </el-card>
      </div>
      
      <div class="questions-grid" v-loading="loading">
        <el-empty v-if="!loading && questions.length === 0" description="暂无题目" />
        
        <el-card
          v-for="question in questions"
          :key="question.id"
          class="question-card"
          shadow="hover"
        >
          <div class="question-header">
            <el-tag :type="getTypeColor(question.type)">{{ getTypeLabel(question.type) }}</el-tag>
            <el-tag type="info">HSK {{ question.level }}</el-tag>
            <el-tag v-if="question.audio_url" type="warning">
              <el-icon><Headset /></el-icon> 听力
            </el-tag>
          </div>
          
          <div class="question-content">
            <p>{{ question.content }}</p>
            <div v-if="question.audio_url" class="audio-section">
              <AudioPlayer :audio-url="question.audio_url" />
            </div>
          </div>
          
          <div class="question-footer">
            <el-button type="primary" size="small" @click="startPractice(question)">
              开始练习
            </el-button>
          </div>
        </el-card>
      </div>
      
      <div class="pagination">
        <el-pagination
          v-if="total > 0"
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[12, 24, 48]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @current-change="loadQuestions"
          @size-change="loadQuestions"
        />
      </div>
    </div>
    
    <el-dialog 
      v-model="practiceDialog" 
      :title="`第 ${currentQuestionIndex + 1} 题 / 共 ${questions.length} 题`"
      width="700px"
      :close-on-click-modal="false"
      class="practice-dialog-wrapper"
    >
      <div v-if="currentQuestion" class="practice-dialog">
        <!-- 题目信息栏 -->
        <div class="question-meta">
          <el-tag :type="getTypeColor(currentQuestion.type)">{{ getTypeLabel(currentQuestion.type) }}</el-tag>
          <el-tag type="info">HSK {{ currentQuestion.level }}</el-tag>
          <el-tag v-if="currentQuestion.difficulty" type="warning">
            难度: {{ '★'.repeat(currentQuestion.difficulty) }}
          </el-tag>
        </div>

        <!-- 题目内容 -->
        <div class="dialog-question">
          <div class="question-number-badge">
            <span>{{ currentQuestionIndex + 1 }}</span>
          </div>
          <h3>{{ currentQuestion.content }}</h3>
          
          <!-- 题目图片显示 -->
          <div v-if="currentQuestion.image_url" class="question-image">
            <img :src="currentQuestion.image_url" alt="题目图片" />
          </div>
          
          <!-- 音频播放器 -->
          <div v-if="currentQuestion.audio_url" class="audio-player-section">
            <div class="audio-card">
              <el-icon class="audio-icon"><Headset /></el-icon>
              <div class="audio-info">
                <p class="audio-title">听力材料</p>
                <p class="audio-tip">请仔细听音频后作答</p>
              </div>
            </div>
            <AudioPlayer :audio-url="currentQuestion.audio_url" />
          </div>
        </div>
        
        <!-- 选项区域 -->
        <div class="dialog-options">
          <div class="options-title">请选择答案：</div>
          
          <!-- 单选题选项 - 图片选项 -->
          <div v-if="(currentQuestion.type === 'single' || currentQuestion.type === '单选题' || currentQuestion.type === 'listening' || currentQuestion.type === 'reading' || currentQuestion.type === 'image_choice') && currentQuestion.option_type === 'image'" class="image-options-container">
            <div
              v-for="(option, index) in parseOptions(currentQuestion.options)"
              :key="index"
              class="image-option-item"
              :class="{ 'is-selected': userAnswer === getOptionValue(option, index) }"
              @click="selectOption(getOptionValue(option, index))"
            >
              <div class="image-option-label">{{ String.fromCharCode(65 + index) }}</div>
              <div class="image-option-wrapper">
                <img 
                  :src="getOptionValue(option, index)" 
                  :alt="`选项${String.fromCharCode(65 + index)}`"
                  loading="lazy"
                />
                <div v-if="userAnswer === getOptionValue(option, index)" class="image-option-check">
                  <el-icon :size="40" color="white"><Check /></el-icon>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 单选题选项 - 文字选项 -->
          <div v-else-if="currentQuestion.type === 'single' || currentQuestion.type === '单选题' || currentQuestion.type === 'listening' || currentQuestion.type === 'reading' || currentQuestion.type === 'image_choice'" class="answer-options">
            <div
              v-for="(option, index) in parseOptions(currentQuestion.options)"
              :key="index"
              class="option-card"
              :class="{ 'is-selected': userAnswer === getOptionValue(option, index) }"
              @click="selectOption(getOptionValue(option, index))"
            >
              <div class="option-label-circle">{{ String.fromCharCode(65 + index) }}</div>
              <div class="option-content">
                <span class="option-text">{{ getOptionText(option) }}</span>
              </div>
              <div class="option-check">
                <el-icon v-if="userAnswer === getOptionValue(option, index)"><Check /></el-icon>
              </div>
            </div>
          </div>
          
          <!-- 多选题选项 - 图片选项 -->
          <div v-else-if="(currentQuestion.type === 'multiple' || currentQuestion.type === '多选题') && currentQuestion.option_type === 'image'" class="image-options-container">
            <div
              v-for="(option, index) in parseOptions(currentQuestion.options)"
              :key="index"
              class="image-option-item"
              :class="{ 'is-selected': userAnswer.includes(getOptionValue(option, index)) }"
              @click="toggleMultipleOption(getOptionValue(option, index))"
            >
              <div class="image-option-label">{{ String.fromCharCode(65 + index) }}</div>
              <div class="image-option-wrapper">
                <img 
                  :src="getOptionValue(option, index)" 
                  :alt="`选项${String.fromCharCode(65 + index)}`"
                  loading="lazy"
                />
                <div v-if="userAnswer.includes(getOptionValue(option, index))" class="image-option-check">
                  <el-icon :size="40" color="white"><Check /></el-icon>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 多选题选项 - 文字选项 -->
          <div v-else-if="currentQuestion.type === 'multiple' || currentQuestion.type === '多选题'" class="answer-options">
            <div
              v-for="(option, index) in parseOptions(currentQuestion.options)"
              :key="index"
              class="option-card"
              :class="{ 'is-selected': userAnswer.includes(getOptionValue(option, index)) }"
              @click="toggleMultipleOption(getOptionValue(option, index))"
            >
              <div class="option-label-circle">{{ String.fromCharCode(65 + index) }}</div>
              <div class="option-content">
                <span class="option-text">{{ getOptionText(option) }}</span>
              </div>
              <div class="option-check">
                <el-icon v-if="userAnswer.includes(getOptionValue(option, index))"><Check /></el-icon>
              </div>
            </div>
          </div>
          
          <!-- 判断题选项 -->
          <div v-else-if="currentQuestion.type === 'judge' || currentQuestion.type === '判断题'" class="judge-options">
            <div 
              class="judge-card"
              :class="{ 'is-selected': userAnswer === '正确' }"
              @click="userAnswer = '正确'"
            >
              <el-icon class="judge-icon correct"><CircleCheck /></el-icon>
              <span>正确</span>
            </div>
            <div 
              class="judge-card"
              :class="{ 'is-selected': userAnswer === '错误' }"
              @click="userAnswer = '错误'"
            >
              <el-icon class="judge-icon wrong"><CircleClose /></el-icon>
              <span>错误</span>
            </div>
          </div>
          
          <!-- 填空题输入 -->
          <div v-else-if="currentQuestion.type === 'fill' || currentQuestion.type === '填空题'" class="fill-input">
            <el-input
              v-model="userAnswer"
              placeholder="请输入答案（支持中文/拼音）"
              size="large"
              clearable
            />
          </div>
          
          <!-- 书写题输入 -->
          <div v-else-if="currentQuestion.type === 'writing' || currentQuestion.type === '书写题'" class="writing-input">
            <el-input
              v-model="userAnswer"
              type="textarea"
              :rows="6"
              placeholder="请根据提示写出完整的句子或段落"
              clearable
            />
          </div>
        </div>
        
        <!-- 答题结果 -->
        <div v-if="showResult" class="result-section">
          <div class="result-card" :class="isCorrect ? 'correct' : 'wrong'">
            <div class="result-icon">
              <el-icon v-if="isCorrect"><CircleCheck /></el-icon>
              <el-icon v-else><CircleClose /></el-icon>
            </div>
            <div class="result-text">
              <h4>{{ isCorrect ? '回答正确！' : '回答错误' }}</h4>
              <p class="result-detail">
                <span class="label">正确答案：</span>
                <span class="answer">{{ currentQuestion.answer }}</span>
              </p>
            </div>
          </div>
          
          <div v-if="currentQuestion.explanation" class="explanation-card">
            <div class="explanation-header">
              <el-icon><Document /></el-icon>
              <span>答案解析</span>
            </div>
            <p class="explanation-content">{{ currentQuestion.explanation }}</p>
          </div>
        </div>
      </div>
      
      <template #footer>
        <div class="dialog-footer-actions">
          <div class="footer-left">
            <el-button @click="closePractice" plain>
              <el-icon><Close /></el-icon>
              退出练习
            </el-button>
          </div>
          <div class="footer-right">
            <el-button v-if="!showResult" type="primary" @click="submitAnswer" :disabled="!userAnswer || (Array.isArray(userAnswer) && userAnswer.length === 0)">
              <el-icon><Check /></el-icon>
              提交答案
            </el-button>
            <el-button v-else type="success" @click="nextQuestion">
              下一题
              <el-icon><ArrowRight /></el-icon>
            </el-button>
          </div>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { 
  Headset, Check, Close, ArrowRight, CircleCheck, CircleClose, Document 
} from '@element-plus/icons-vue'
import axios from 'axios'
import AudioPlayer from '../components/AudioPlayer.vue'

const loading = ref(false)
const questions = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const practiceDialog = ref(false)
const currentQuestion = ref(null)
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const showResult = ref(false)
const isCorrect = ref(false)

const filters = reactive({
  level: 0,
  type: ''
})

const loadQuestions = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    if (filters.level) params.level = filters.level
    if (filters.type) params.type = filters.type
    
    const response = await axios.get('/question/questions/', { params })
    questions.value = response.data.results || response.data
    total.value = response.data.count || questions.value.length
    
  } catch (error) {
    console.error('加载题目失败:', error)
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
}

const startPractice = (question) => {
  currentQuestion.value = question
  currentQuestionIndex.value = questions.value.findIndex(q => q.id === question.id)
  userAnswer.value = (question.type === 'multiple' || question.type === '多选题') ? [] : ''
  showResult.value = false
  practiceDialog.value = true
}

const selectOption = (value) => {
  userAnswer.value = value
}

const toggleMultipleOption = (value) => {
  if (!Array.isArray(userAnswer.value)) {
    userAnswer.value = []
  }
  const index = userAnswer.value.indexOf(value)
  if (index > -1) {
    userAnswer.value.splice(index, 1)
  } else {
    userAnswer.value.push(value)
  }
}

const getOptionValue = (option, index) => {
  if (typeof option === 'object' && option !== null) {
    return option.value || option.label || String.fromCharCode(65 + index)
  }
  return option
}

const getOptionText = (option) => {
  if (typeof option === 'object' && option !== null) {
    return option.text || option.label || ''
  }
  return option || ''
}

const closePractice = () => {
  practiceDialog.value = false
  currentQuestion.value = null
  userAnswer.value = ''
  showResult.value = false
}

const nextQuestion = () => {
  const nextIndex = currentQuestionIndex.value + 1
  if (nextIndex < questions.value.length) {
    startPractice(questions.value[nextIndex])
  } else {
    ElMessage.success('已完成所有题目！')
    closePractice()
  }
}

const submitAnswer = async () => {
  if (!userAnswer.value || (Array.isArray(userAnswer.value) && userAnswer.value.length === 0)) {
    ElMessage.warning('请选择答案')
    return
  }
  
  let answer = userAnswer.value
  
  // 如果是图片选项，需要将URL转换为字母
  if (currentQuestion.value.option_type === 'image') {
    const options = parseOptions(currentQuestion.value.options)
    
    if (Array.isArray(answer)) {
      // 多选题：将每个URL转换为对应的字母
      answer = answer.map(url => {
        const index = options.findIndex(opt => getOptionValue(opt, options.indexOf(opt)) === url)
        return index !== -1 ? String.fromCharCode(65 + index) : url
      }).sort().join(',')
    } else {
      // 单选题：将URL转换为对应的字母
      const index = options.findIndex(opt => getOptionValue(opt, options.indexOf(opt)) === answer)
      answer = index !== -1 ? String.fromCharCode(65 + index) : answer
    }
  } else if (Array.isArray(answer)) {
    // 文字选项的多选题
    answer = answer.sort().join(',')
  }
  
  const correctAnswer = currentQuestion.value.answer.trim()
  const userAnswerTrimmed = String(answer).trim()
  
  console.log('用户答案:', userAnswerTrimmed, '正确答案:', correctAnswer)
  isCorrect.value = userAnswerTrimmed === correctAnswer
  showResult.value = true
  
  // 提交答题记录到后端
  try {
    await axios.post('/question/answer/', {
      question_id: currentQuestion.value.id,
      user_answer: userAnswerTrimmed
    })
  } catch (error) {
    console.error('提交答题记录失败:', error)
  }
}

const parseOptions = (options) => {
  try {
    let parsed = options
    
    // 如果是字符串，先解析
    if (typeof options === 'string') {
      parsed = JSON.parse(options)
    }
    
    // 处理新的数据结构 {option_type: 'text', options: [{label, text, value}]}
    if (parsed && typeof parsed === 'object' && parsed.options && Array.isArray(parsed.options)) {
      return parsed.options
    }
    
    // 处理旧的数据结构（直接是数组）
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

// 判断选项是否是图片URL
const isImageOption = (option) => {
  if (!option || typeof option !== 'string') return false
  // 检查是否是图片URL（以常见图片扩展名结尾或包含/media/images/）
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
  const lowerOption = option.toLowerCase()
  return imageExtensions.some(ext => lowerOption.endsWith(ext)) || 
         lowerOption.includes('/media/images/') ||
         lowerOption.includes('/media/image/') ||
         lowerOption.startsWith('http') && (lowerOption.includes('image') || lowerOption.includes('img'))
}

const getTypeColor = (type) => {
  const colorMap = {
    'single': 'primary',
    'multiple': 'success',
    'judge': 'warning',
    'fill': 'info',
    'reading': 'info',
    'writing': 'danger',
    '单选题': 'primary',
    '多选题': 'success',
    '判断题': 'warning',
    '填空题': 'info',
    '阅读题': 'info',
    '书写题': 'danger'
  }
  return colorMap[type] || 'info'
}

const getTypeLabel = (type) => {
  const labelMap = {
    'single': '单选题',
    'multiple': '多选题',
    'judge': '判断题',
    'fill': '填空题',
    'reading': '阅读题',
    'writing': '书写题'
  }
  return labelMap[type] || type
}

onMounted(() => {
  loadQuestions()
})
</script>

<style scoped>
.practice-page {
  padding: 40px 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 64px);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  font-weight: 700;
  color: #333333;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 16px;
  color: #666666;
}

.filter-section {
  margin-bottom: 30px;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.filters .el-select {
  width: 200px;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.question-card {
  transition: all 0.3s;
}

.question-card:hover {
  transform: translateY(-5px);
}

.question-header {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.question-content {
  margin: 15px 0;
  min-height: 60px;
}

.question-content p {
  font-size: 15px;
  line-height: 1.6;
  color: #333333;
}

.question-footer {
  text-align: right;
}

.pagination {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

/* 练习弹窗样式 */
.practice-dialog-wrapper :deep(.el-dialog__header) {
  background: #CCFFFF;
  color: #333333;
  color: white;
  padding: 20px 24px;
  margin: 0;
}

.practice-dialog-wrapper :deep(.el-dialog__title) {
  color: white;
  font-size: 18px;
  font-weight: 600;
}

.practice-dialog-wrapper :deep(.el-dialog__close) {
  color: white;
}

.practice-dialog {
  padding: 0;
}

.question-meta {
  display: flex;
  gap: 10px;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
  background: #FFFFFF;
}

.dialog-question {
  padding: 24px;
  position: relative;
}

.question-number-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background: #CCFFFF;
  color: #333333;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 20px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.dialog-question h3 {
  font-size: 20px;
  line-height: 1.8;
  margin-bottom: 24px;
  color: #333333;
  padding-right: 70px;
  font-weight: 600;
}

.question-image img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 12px;
  margin: 20px 0;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.audio-player-section {
  margin: 24px 0;
}

.audio-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
  border-radius: 12px;
  margin-bottom: 12px;
}

.audio-icon {
  font-size: 32px;
  color: #CCFFFF;
}

.audio-info {
  flex: 1;
}

.audio-title {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
  margin: 0 0 4px 0;
}

.audio-tip {
  font-size: 14px;
  color: #606266;
  margin: 0;
}

.dialog-options {
  padding: 0 24px 24px;
}

.options-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

/* 选项卡片样式 - 优化版 */
.answer-options {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.option-card {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 24px;
  border: 2px solid #e8eaed;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
  position: relative;
  overflow: hidden;
}

.option-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: #CCFFFF;
  color: #333333;
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.option-card:hover {
  border-color: #667eea;
  background: linear-gradient(135deg, #f8f9ff 0%, #fafbff 100%);
  transform: translateX(6px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.15);
}

.option-card:hover::before {
  transform: scaleY(1);
}

.option-card.is-selected {
  border-color: #667eea;
  background: linear-gradient(135deg, #f0f3ff 0%, #f5f7ff 100%);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
  transform: translateX(6px);
}

.option-card.is-selected::before {
  transform: scaleY(1);
}

.option-label-circle {
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f0f2f5 0%, #e8eaed 100%);
  color: #606266;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 19px;
  font-weight: 700;
  flex-shrink: 0;
  transition: all 0.35s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.option-card:hover .option-label-circle {
  transform: scale(1.08) rotate(5deg);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.option-card.is-selected .option-label-circle {
  background: #CCFFFF;
  color: #333333;
  color: white;
  transform: scale(1.1);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.option-content {
  flex: 1;
  min-width: 0;
}

.option-text {
  font-size: 17px;
  line-height: 1.7;
  color: #303133;
  font-weight: 500;
  word-wrap: break-word;
  transition: color 0.3s;
}

.option-card:hover .option-text {
  color: #CCFFFF;
}

.option-card.is-selected .option-text {
  color: #CCFFFF;
  font-weight: 600;
}

.option-check {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #CCFFFF;
  color: #333333;
  border-radius: 50%;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.option-card.is-selected .option-check {
  opacity: 1;
  transform: scale(1);
}

.option-check .el-icon {
  font-size: 18px;
  color: white;
  font-weight: bold;
}

/* 判断题样式 */
.judge-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.judge-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 32px 20px;
  border: 2px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  background: white;
}

.judge-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.judge-card.is-selected {
  border-color: #667eea;
  background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
}

.judge-icon {
  font-size: 48px;
}

.judge-icon.correct {
  color: #67c23a;
}

.judge-icon.wrong {
  color: #f56c6c;
}

.judge-card span {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

/* 填空题样式 */
.fill-input {
  margin-top: 8px;
}

.fill-input :deep(.el-input__inner) {
  height: 50px;
  font-size: 16px;
}

.result-section {
  margin-top: 25px;
}

/* 结果区域样式 - 优化版 */
.result-section {
  padding: 0 24px 24px;
  animation: slideInUp 0.4s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-card {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 28px;
  border-radius: 16px;
  margin-bottom: 18px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.result-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.result-card.correct {
  background: linear-gradient(135deg, #f0f9ff 0%, #e8f5e9 100%);
  border: 2px solid #67c23a;
}

.result-card.correct::before {
  background: linear-gradient(90deg, #67c23a 0%, #85ce61 100%);
}

.result-card.wrong {
  background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
  border: 2px solid #f56c6c;
}

.result-card.wrong::before {
  background: linear-gradient(90deg, #f56c6c 0%, #f78787 100%);
}

.result-icon {
  font-size: 56px;
  flex-shrink: 0;
  animation: bounceIn 0.6s ease-out;
}

@keyframes bounceIn {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

.result-card.correct .result-icon {
  color: #67c23a;
  filter: drop-shadow(0 4px 8px rgba(103, 194, 58, 0.3));
}

.result-card.wrong .result-icon {
  color: #f56c6c;
  filter: drop-shadow(0 4px 8px rgba(245, 108, 108, 0.3));
}

.result-text {
  flex: 1;
}

.result-text h4 {
  font-size: 22px;
  margin: 0 0 10px 0;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.result-card.correct h4 {
  color: #67c23a;
}

.result-card.wrong h4 {
  color: #f56c6c;
}

.result-detail {
  margin: 0;
  font-size: 17px;
  color: #606266;
  line-height: 1.6;
}

.result-detail .label {
  font-weight: 600;
  color: #303133;
}

.result-detail .answer {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  color: white;
  font-weight: 700;
  font-size: 18px;
  border-radius: 8px;
  margin-left: 8px;
  box-shadow: 0 2px 8px rgba(64, 158, 255, 0.3);
}

.explanation-card {
  padding: 24px;
  background: linear-gradient(135deg, #f9fafb 0%, #f5f7fa 100%);
  border-radius: 14px;
  border-left: 5px solid #409eff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.explanation-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 14px;
}

.explanation-header .el-icon {
  color: #409eff;
  font-size: 22px;
}

.explanation-content {
  font-size: 16px;
  line-height: 1.9;
  color: #606266;
  margin: 0;
  font-weight: 500;
}

/* 底部操作区 */
.dialog-footer-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-top: 1px solid #f0f0f0;
}

.footer-left,
.footer-right {
  display: flex;
  gap: 12px;
}

/* 图片选项样式 */
.image-options-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 16px;
  margin: 20px 0;
}

.image-option-item {
  position: relative;
  background: #ffffff;
  border: 3px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  padding: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-option-item:hover {
  border-color: #667eea;
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.25);
}

.image-option-item.is-selected {
  border-color: #667eea;
  background: linear-gradient(145deg, #667eea, #764ba2);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  transform: scale(1.05);
}

.image-option-label {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 32px;
  height: 32px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #606266;
  font-size: 14px;
  z-index: 1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
}

.image-option-item.is-selected .image-option-label {
  background: white;
  color: #CCFFFF;
  transform: scale(1.1);
}

.image-option-wrapper {
  width: 140px;
  height: 140px;
  margin: 5px 0;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  position: relative;
}

.image-option-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.3s;
}

.image-option-item:hover .image-option-wrapper img {
  transform: scale(1.08);
}

.image-option-check {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(102, 126, 234, 0.9);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: imageBounce 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes imageBounce {
  0% {
    transform: translate(-50%, -50%) scale(0);
  }
  50% {
    transform: translate(-50%, -50%) scale(1.2);
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
  }
}

@media (max-width: 768px) {
  .image-options-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .image-option-wrapper {
    width: 120px;
    height: 120px;
  }
}
</style>
