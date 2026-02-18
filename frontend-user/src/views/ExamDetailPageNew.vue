<template>
  <div class="exam-detail-page">
    <!-- 顶部固定栏 -->
    <div class="exam-header-fixed">
      <div class="header-left">
        <h2>{{ examTitle }}</h2>
        <el-tag type="info" size="large">{{ currentSectionName }}</el-tag>
      </div>
      <div class="header-center">
        <el-progress 
          :percentage="overallProgress" 
          :stroke-width="20"
          :format="format => `${answeredCount}/${totalQuestions}`"
        />
      </div>
      <div class="header-right">
        <el-tag type="warning" size="large" effect="dark">
          <el-icon><Clock /></el-icon>
          {{ formatTime(remainingTime) }}
        </el-tag>
        <el-button type="danger" plain @click="handleAbandon">退出</el-button>
      </div>
    </div>

    <div class="exam-body">
      <!-- 左侧：Section和Part导航 -->
      <div class="exam-sidebar">
        <div class="section-nav">
          <div 
            v-for="section in sections" 
            :key="section.id"
            class="section-item"
            :class="{ 'is-active': currentSectionId === section.id }"
          >
            <div class="section-header" @click="switchSection(section.id)">
              <div class="section-icon">
                <el-icon :size="24">
                  <component :is="section.icon" />
                </el-icon>
              </div>
              <div class="section-info">
                <div class="section-name">{{ section.name }}</div>
                <div class="section-progress">
                  {{ getSectionAnsweredCount(section.id) }}/{{ getSectionQuestionCount(section.id) }}
                </div>
              </div>
            </div>
            
            <!-- Part列表 -->
            <div class="part-list" v-if="currentSectionId === section.id">
              <div 
                v-for="part in section.parts" 
                :key="part.id"
                class="part-item"
                :class="{ 
                  'is-active': currentPartId === part.id,
                  'is-completed': isPartCompleted(part.id)
                }"
                @click="switchPart(part.id)"
              >
                <div class="part-number">Part {{ part.part_number }}</div>
                <div class="part-name">{{ part.title }}</div>
                <div class="part-count">{{ getPartAnsweredCount(part.id) }}/{{ part.questions.length }}</div>
                <el-icon v-if="isPartCompleted(part.id)" class="part-check"><CircleCheck /></el-icon>
              </div>
            </div>
          </div>
        </div>

        <!-- 听力音频控制器（仅在听力部分显示） -->
        <div class="audio-control" v-if="currentSection?.type === 'listening' && currentSection?.audio_url">
          <div class="audio-header">
            <el-icon><Headset /></el-icon>
            <span>听力音频 - 完整录音</span>
          </div>
          <audio 
            ref="audioPlayer"
            :src="currentSection.audio_url"
            @timeupdate="handleAudioTimeUpdate"
            @ended="handleAudioEnded"
            @loadedmetadata="handleAudioLoaded"
            controls
            style="width: 100%"
          >
            您的浏览器不支持音频播放
          </audio>
          <div class="audio-info">
            <div class="audio-meta">
              <span>{{ currentSection.name }}</span>
              <span>{{ formatAudioTime(audioCurrentTime) }} / {{ formatAudioTime(audioTotalTime) }}</span>
            </div>
            <div class="audio-tip">
              <el-icon><InfoFilled /></el-icon>
              <span>完整听力音频，对应所有听力题目</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 中间：题目内容区 -->
      <div class="exam-content">
        <div class="content-header">
          <div class="part-title-bar">
            <h3>Part {{ currentPart?.part_number }}: {{ currentPart?.title }}</h3>
            <el-tag>{{ currentPart?.description }}</el-tag>
          </div>
          <div class="question-nav-bar">
            <el-button 
              :disabled="currentQuestionIndex === 0"
              @click="prevQuestion"
              :icon="ArrowLeft"
            >
              上一题
            </el-button>
            <span class="question-indicator">
              题目 {{ currentQuestionIndex + 1 }} / {{ totalQuestions }}
            </span>
            <el-button 
              :disabled="currentQuestionIndex >= totalQuestions - 1"
              @click="nextQuestion"
              :icon="ArrowRight"
            >
              下一题
            </el-button>
          </div>
        </div>

        <!-- 题目卡片 -->
        <el-card class="question-card" v-if="currentQuestion">

          <!-- 阅读材料（如果有） -->
          <div class="passage-section" v-if="currentPart?.passage">
            <div class="passage-header">
              <el-icon><Reading /></el-icon>
              <span>阅读材料</span>
            </div>
            <div class="passage-content">
              {{ currentPart.passage }}
            </div>
          </div>

          <!-- 题目内容 -->
          <div class="question-content">
            <div class="question-header">
              <span class="question-number">第 {{ currentQuestionIndex + 1 }} 题</span>
              <div class="question-divider"></div>
            </div>
            <p class="question-text">{{ currentQuestion.content }}</p>
            
            <!-- 图片（如果有） -->
            <div class="question-image" v-if="currentQuestion.image_url">
              <img :src="currentQuestion.image_url" alt="题目图片" />
            </div>
          </div>

          <!-- 答题区域 -->
          <div class="answer-section">
            <!-- 单选题 -->
            <div v-if="isChoiceQuestion(currentQuestion.type)" class="choice-options">
              <!-- 图片选项 -->
              <div v-if="currentQuestion.option_type === 'image'" class="image-options">
                <div 
                  v-for="(option, index) in parseOptions(currentQuestion.options)" 
                  :key="index"
                  class="image-option-item"
                  :class="{ 'is-selected': answers[currentQuestion.id] === option }"
                  @click="selectAnswer(currentQuestion.id, option)"
                >
                  <div class="image-option-label">{{ String.fromCharCode(65 + index) }}</div>
                  <div class="image-option-wrapper">
                    <img 
                      :src="option" 
                      :alt="`选项${String.fromCharCode(65 + index)}`"
                      @error="handleImageError"
                      loading="lazy"
                    />
                    <div v-if="answers[currentQuestion.id] === option" class="image-option-check">
                      <el-icon :size="40" color="#67c23a"><CircleCheck /></el-icon>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- 如果选项内容只是单个字母，说明是旧数据格式，只显示字母选项 -->
              <div v-else-if="parseOptions(currentQuestion.options).length > 0 && parseOptions(currentQuestion.options)[0].length === 1" 
                   class="legacy-notice">
                <div class="legacy-tip">
                  <el-icon color="#e6a23c"><InfoFilled /></el-icon>
                  <span>请根据题目内容选择答案</span>
                </div>
                <div class="legacy-options">
                  <div
                    v-for="(option, index) in parseOptions(currentQuestion.options)" 
                    :key="index"
                    class="legacy-option-item"
                    :class="{ 'is-selected': answers[currentQuestion.id] === option }"
                    @click="selectAnswer(currentQuestion.id, option)"
                  >
                    <div class="option-letter">{{ option }}</div>
                  </div>
                </div>
              </div>
              
              <!-- 正常的文字选项显示 -->
              <div v-else>
                <div 
                  v-for="(option, index) in parseOptions(currentQuestion.options)" 
                  :key="index"
                  class="option-item"
                  :class="{ 'is-selected': answers[currentQuestion.id] === option }"
                  @click="selectAnswer(currentQuestion.id, option)"
                >
                  <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
                  <div class="option-content">{{ option }}</div>
                  <div class="option-check">
                    <el-icon v-if="answers[currentQuestion.id] === option"><CircleCheck /></el-icon>
                  </div>
                </div>
              </div>
            </div>

            <!-- 判断题 -->
            <div v-else-if="currentQuestion.type === 'judge'" class="judge-options">
              <div 
                class="judge-item"
                :class="{ 'is-selected': answers[currentQuestion.id] === '正确' }"
                @click="selectAnswer(currentQuestion.id, '正确')"
              >
                <el-icon :size="40"><CircleCheck /></el-icon>
                <span>正确</span>
              </div>
              <div 
                class="judge-item"
                :class="{ 'is-selected': answers[currentQuestion.id] === '错误' }"
                @click="selectAnswer(currentQuestion.id, '错误')"
              >
                <el-icon :size="40"><CircleClose /></el-icon>
                <span>错误</span>
              </div>
            </div>

            <!-- 填空题 -->
            <div v-else-if="currentQuestion.type === 'fill' || currentQuestion.type === 'writing'" class="fill-input-section">
              <el-input
                v-model="answers[currentQuestion.id]"
                type="textarea"
                :rows="currentQuestion.type === 'writing' ? 10 : 4"
                placeholder="请输入答案..."
                maxlength="500"
                show-word-limit
              />
            </div>
          </div>
        </el-card>

        <!-- 底部操作栏 -->
        <div class="content-footer">
          <el-button 
            size="large"
            @click="prevQuestion"
            :disabled="currentQuestionIndex === 0"
          >
            <el-icon><ArrowLeft /></el-icon>
            上一题
          </el-button>
          
          <div class="footer-center">
            <el-button 
              type="warning" 
              size="large"
              plain
              @click="showQuestionList = true"
            >
              <el-icon><Grid /></el-icon>
              题目列表
            </el-button>
            <el-button 
              v-if="isLastQuestionInPart"
              type="success" 
              size="large"
              @click="completePartAndNext"
            >
              完成 Part {{ currentPart?.part_number }}
            </el-button>
          </div>
          
          <el-button 
            size="large"
            type="primary"
            @click="nextQuestion"
            :disabled="currentQuestionIndex >= totalQuestions - 1"
          >
            下一题
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>

      <!-- 右侧：答题卡 -->
      <div class="exam-answer-sheet">
        <div class="sheet-header">
          <h3>答题卡</h3>
          <el-button type="primary" size="small" @click="handleSubmit">提交试卷</el-button>
        </div>
        
        <div class="sheet-content">
          <div v-for="section in sections" :key="section.id" class="sheet-section">
            <div class="sheet-section-title">{{ section.name }}</div>
            <div class="sheet-questions">
              <div 
                v-for="question in getSectionQuestions(section.id)" 
                :key="question.id"
                class="sheet-question-item"
                :class="{
                  'is-current': currentQuestion?.id === question.id,
                  'is-answered': answers[question.id] !== undefined && answers[question.id] !== '',
                  'is-unanswered': !answers[question.id]
                }"
                @click="jumpToQuestion(getQuestionGlobalIndex(question.id))"
              >
                {{ getQuestionGlobalIndex(question.id) + 1 }}
              </div>
            </div>
          </div>
        </div>

        <div class="sheet-legend">
          <div class="legend-item">
            <div class="legend-box is-answered"></div>
            <span>已答</span>
          </div>
          <div class="legend-item">
            <div class="legend-box is-current"></div>
            <span>当前</span>
          </div>
          <div class="legend-item">
            <div class="legend-box is-unanswered"></div>
            <span>未答</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 题目列表弹窗 -->
    <el-drawer v-model="showQuestionList" title="题目列表" size="60%">
      <div class="question-list-drawer">
        <div v-for="section in sections" :key="section.id" class="list-section">
          <h3>{{ section.name }}</h3>
          <div v-for="part in section.parts" :key="part.id" class="list-part">
            <h4>Part {{ part.part_number }}: {{ part.title }}</h4>
            <div class="list-questions">
              <el-button
                v-for="question in part.questions"
                :key="question.id"
                :type="answers[question.id] ? 'success' : 'default'"
                @click="jumpToQuestionAndClose(getQuestionGlobalIndex(question.id))"
              >
                {{ getQuestionGlobalIndex(question.id) + 1 }}
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Clock,
  Headset,
  Reading,
  Edit,
  Document,
  CircleCheck,
  CircleClose,
  ArrowLeft,
  ArrowRight,
  Grid,
  InfoFilled
} from '@element-plus/icons-vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()

// 数据定义
const examTitle = ref('')
const examId = ref(null)
const loading = ref(false)
const remainingTime = ref(0)
const timerInterval = ref(null)
const audioPlayer = ref(null)
const audioCurrentTime = ref(0)
const audioTotalTime = ref(0)

// 考试结构数据
const sections = ref([])
const currentSectionId = ref(null)
const currentPartId = ref(null)
const currentQuestionIndex = ref(0)
const answers = ref({})
const showQuestionList = ref(false)

// 当前section
const currentSection = computed(() => {
  return sections.value.find(s => s.id === currentSectionId.value)
})

// 当前section名称
const currentSectionName = computed(() => {
  return currentSection.value?.name || ''
})

// 当前part
const currentPart = computed(() => {
  if (!currentSection.value) return null
  return currentSection.value.parts.find(p => p.id === currentPartId.value)
})

// 所有题目（扁平化）
const allQuestions = computed(() => {
  const questions = []
  sections.value.forEach(section => {
    section.parts.forEach(part => {
      questions.push(...part.questions)
    })
  })
  return questions
})

// 当前题目
const currentQuestion = computed(() => {
  const question = allQuestions.value[currentQuestionIndex.value]
  if (!question) return null
  
  // 清理题目内容，移除可能的题号前缀
  const cleanContent = question.content.replace(/^(HSK\d+[^：:]*[：:])\s*/, '')
  
  return {
    ...question,
    content: cleanContent
  }
})

// 当前题目在Part中的索引
const currentQuestionIndexInPart = computed(() => {
  if (!currentPart.value) return 0
  const questionId = currentQuestion.value?.id
  return currentPart.value.questions.findIndex(q => q.id === questionId)
})

// 是否是Part中的最后一题
const isLastQuestionInPart = computed(() => {
  if (!currentPart.value) return false
  return currentQuestionIndexInPart.value === currentPart.value.questions.length - 1
})

// 总题目数
const totalQuestions = computed(() => allQuestions.value.length)

// 已答题数
const answeredCount = computed(() => {
  return Object.keys(answers.value).filter(key => {
    const answer = answers.value[key]
    return answer !== undefined && answer !== '' && answer !== null
  }).length
})

// 总体进度
const overallProgress = computed(() => {
  if (totalQuestions.value === 0) return 0
  return Math.round((answeredCount.value / totalQuestions.value) * 100)
})

// 音频加载完成
const handleAudioLoaded = () => {
  if (audioPlayer.value) {
    audioTotalTime.value = audioPlayer.value.duration || 0
  }
}

// 加载考试数据
const loadExamData = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    // 优先从query获取setId，否则从params获取examId
    const questionSetId = route.query.setId || route.params.examId
    
    // 1. 先启动考试（或恢复考试）
    // axios 的全局 baseURL 为 /api，这里使用相对路径 /question/...
    const startResponse = await axios.post(
      '/question/exam/start/',
      { question_set_id: questionSetId },
      { headers: { Authorization: `Bearer ${token}` } }
    )
    
    examId.value = startResponse.data.exam_id
    examTitle.value = startResponse.data.question_set_title
    remainingTime.value = startResponse.data.time_limit * 60
    
    // 使用后端返回的question_set_id确保正确性
    const actualQuestionSetId = startResponse.data.question_set_id
    
    // 2. 获取结构化的题目数据
    const structuredResponse = await axios.get(
      `/question/sets/${actualQuestionSetId}/structured/`,
      { headers: { Authorization: `Bearer ${token}` } }
    )
    
    const data = structuredResponse.data
    
    // 处理sections数据，添加图标
    sections.value = data.sections.map(section => ({
      ...section,
      icon: section.icon === 'Headset' ? Headset : (section.icon === 'Reading' ? Reading : Edit)
    }))
    
    // 设置初始section和part
    if (sections.value.length > 0) {
      currentSectionId.value = sections.value[0].id
      if (sections.value[0].parts.length > 0) {
        currentPartId.value = sections.value[0].parts[0].id
      }
    }
    
    // 启动计时器
    startTimer()
    
    // 启动自动保存
    startAutoSave()
  } catch (error) {
    console.error('加载考试数据失败:', error)
    ElMessage.error('加载考试失败: ' + (error.response?.data?.error || error.message))
    router.push('/exam')
  } finally {
    loading.value = false
  }
}

// 初始化考试
const initExamData = () => {
  loadExamData()
}

// 计时器
const startTimer = () => {
  timerInterval.value = setInterval(() => {
    if (remainingTime.value > 0) {
      remainingTime.value--
    } else {
      clearInterval(timerInterval.value)
      ElMessage.warning('考试时间已到')
      handleSubmit()
    }
  }, 1000)
}

// 格式化时间
const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  if (hours > 0) {
    return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
  }
  return `${minutes}:${String(secs).padStart(2, '0')}`
}

// 格式化音频时间
const formatAudioTime = (seconds) => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${String(secs).padStart(2, '0')}`
}

// 切换section
const switchSection = (sectionId) => {
  currentSectionId.value = sectionId
  const section = sections.value.find(s => s.id === sectionId)
  if (section && section.parts.length > 0) {
    currentPartId.value = section.parts[0].id
    // 跳转到该section的第一题
    const firstQuestionIndex = getQuestionGlobalIndex(section.parts[0].questions[0].id)
    currentQuestionIndex.value = firstQuestionIndex
  }
}

// 切换part
const switchPart = (partId) => {
  currentPartId.value = partId
  const part = currentSection.value?.parts.find(p => p.id === partId)
  if (part && part.questions.length > 0) {
    const firstQuestionIndex = getQuestionGlobalIndex(part.questions[0].id)
    currentQuestionIndex.value = firstQuestionIndex
  }
}

// 获取section的题目数
const getSectionQuestionCount = (sectionId) => {
  const section = sections.value.find(s => s.id === sectionId)
  if (!section) return 0
  return section.parts.reduce((sum, part) => sum + part.questions.length, 0)
}

// 获取section已答题数
const getSectionAnsweredCount = (sectionId) => {
  const section = sections.value.find(s => s.id === sectionId)
  if (!section) return 0
  let count = 0
  section.parts.forEach(part => {
    part.questions.forEach(q => {
      if (answers.value[q.id] !== undefined && answers.value[q.id] !== '') {
        count++
      }
    })
  })
  return count
}

// 获取part已答题数
const getPartAnsweredCount = (partId) => {
  let count = 0
  sections.value.forEach(section => {
    const part = section.parts.find(p => p.id === partId)
    if (part) {
      part.questions.forEach(q => {
        if (answers.value[q.id] !== undefined && answers.value[q.id] !== '') {
          count++
        }
      })
    }
  })
  return count
}

// Part是否完成
const isPartCompleted = (partId) => {
  let total = 0
  let answered = 0
  sections.value.forEach(section => {
    const part = section.parts.find(p => p.id === partId)
    if (part) {
      total = part.questions.length
      part.questions.forEach(q => {
        if (answers.value[q.id] !== undefined && answers.value[q.id] !== '') {
          answered++
        }
      })
    }
  })
  return total > 0 && answered === total
}

// 获取section的所有题目
const getSectionQuestions = (sectionId) => {
  const section = sections.value.find(s => s.id === sectionId)
  if (!section) return []
  const questions = []
  section.parts.forEach(part => {
    questions.push(...part.questions)
  })
  return questions
}

// 获取题目的全局索引
const getQuestionGlobalIndex = (questionId) => {
  return allQuestions.value.findIndex(q => q.id === questionId)
}

// 跳转到指定题目
const jumpToQuestion = (index) => {
  if (index >= 0 && index < allQuestions.value.length) {
    currentQuestionIndex.value = index
    updateCurrentSectionAndPart()
  }
}

// 跳转并关闭抽屉
const jumpToQuestionAndClose = (index) => {
  jumpToQuestion(index)
  showQuestionList.value = false
}

// 更新当前section和part
const updateCurrentSectionAndPart = () => {
  const question = currentQuestion.value
  if (!question) return
  
  for (const section of sections.value) {
    for (const part of section.parts) {
      if (part.questions.some(q => q.id === question.id)) {
        currentSectionId.value = section.id
        currentPartId.value = part.id
        return
      }
    }
  }
}

// 上一题
const prevQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    updateCurrentSectionAndPart()
  }
}

// 下一题
const nextQuestion = () => {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    currentQuestionIndex.value++
    updateCurrentSectionAndPart()
  }
}

// 完成Part并进入下一个
const completePartAndNext = () => {
  if (currentQuestionIndex.value < totalQuestions.value - 1) {
    nextQuestion()
  }
}

// 自动保存相关
const autoSaveInterval = ref(null)
const saveQueue = ref(new Set()) // 待保存的题目ID队列

// 选择答案
const selectAnswer = (questionId, answer) => {
  answers.value[questionId] = answer
  // 添加到保存队列
  saveQueue.value.add(questionId)
}

// 图片加载错误处理
const handleImageError = (event) => {
  console.warn('图片加载失败:', event.target.src)
  // 设置占位样式
  event.target.style.backgroundColor = '#f5f5f5'
  event.target.style.border = '2px dashed #dcdfe6'
  event.target.style.display = 'flex'
  event.target.style.alignItems = 'center'
  event.target.style.justifyContent = 'center'
  event.target.style.color = '#909399'
  event.target.style.fontSize = '14px'
  event.target.style.fontWeight = '500'
  event.target.alt = '❌ 图片加载失败'
  
  // 如果是外部链接，可能是CORS问题
  if (event.target.src.startsWith('http://') || event.target.src.startsWith('https://')) {
    console.warn('外部图片加载失败，可能是CORS策略限制')
  }
}

// 启动自动保存
const startAutoSave = () => {
  autoSaveInterval.value = setInterval(async () => {
    if (saveQueue.value.size > 0) {
      await batchSaveAnswers()
    }
  }, 5000) // 每5秒自动保存一次
}

// 批量保存答案
const batchSaveAnswers = async () => {
  if (saveQueue.value.size === 0) return
  
  const token = localStorage.getItem('token')
  const questionIds = Array.from(saveQueue.value)
  
  try {
    // 逐个提交答案（避免并发问题）
    for (const questionId of questionIds) {
      const answer = answers.value[questionId]
      if (answer !== undefined && answer !== null) {
        await axios.post(
          `/question/exam/${examId.value}/submit-answer/`,
          {
            question_id: questionId,
            answer: answer
          },
          { headers: { Authorization: `Bearer ${token}` } }
        )
      }
    }
    
    // 清空保存队列
    saveQueue.value.clear()
  } catch (error) {
    console.error('保存答案失败:', error)
    // 不显示错误提示，避免打扰用户
  }
}

// 手动保存所有答案
const saveAllAnswers = async () => {
  const token = localStorage.getItem('token')
  
  try {
    for (const [questionId, answer] of Object.entries(answers.value)) {
      if (answer !== undefined && answer !== null && answer !== '') {
        await axios.post(
          `/question/exam/${examId.value}/submit-answer/`,
          {
            question_id: questionId,
            answer: answer
          },
          { headers: { Authorization: `Bearer ${token}` } }
        )
      }
    }
  } catch (error) {
    console.error('保存答案失败:', error)
    throw error
  }
}

// 是否是选择题
const isChoiceQuestion = (type) => {
  return ['single', 'reading', 'multiple'].includes(type)
}

// 解析选项
const parseOptions = (options) => {
  if (!options) return []
  try {
    const parsed = JSON.parse(options)
    if (Array.isArray(parsed)) {
      return parsed
    }
    if (parsed.options && Array.isArray(parsed.options)) {
      return parsed.options.map(opt => opt.text || opt.label || opt)
    }
    return []
  } catch (e) {
    console.error('解析选项失败:', e)
    return []
  }
}

// 音频时间更新
const handleAudioTimeUpdate = (e) => {
  if (audioPlayer.value) {
    audioCurrentTime.value = audioPlayer.value.currentTime
    audioTotalTime.value = audioPlayer.value.duration || 0
  }
}

// 音频结束
const handleAudioEnded = () => {
  // 音频结束，不显示提示
}

// 提交试卷
const handleSubmit = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要提交试卷吗？您已完成 ${answeredCount.value}/${totalQuestions.value} 题`,
      '提交确认',
      {
        confirmButtonText: '提交',
        cancelButtonText: '再检查一下',
        type: 'warning'
      }
    )
    
    loading.value = true
    
    try {
      // 1. 先保存所有答案
      await saveAllAnswers()
      
      // 2. 提交考试
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `/question/exam/${examId.value}/complete/`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      
      // 3. 停止计时器和自动保存
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
      }
      if (autoSaveInterval.value) {
        clearInterval(autoSaveInterval.value)
      }
      
      ElMessage.success('提交成功！正在生成报告...')
      
      // 4. 跳转到结果页面
      router.push({
        path: '/exam/result',
        query: {
          examId: examId.value,
          score: response.data.score
        }
      })
    } catch (error) {
      console.error('提交考试失败:', error)
      ElMessage.error('提交失败: ' + (error.response?.data?.error || error.message))
    } finally {
      loading.value = false
    }
  } catch (e) {
    // 取消提交
  }
}

// 放弃考试
const handleAbandon = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要放弃考试吗？已答题目将不会保存。',
      '警告',
      {
        confirmButtonText: '确定放弃',
        cancelButtonText: '继续考试',
        type: 'warning'
      }
    )
    
    try {
      const token = localStorage.getItem('token')
      await axios.post(
        `/question/exam/${examId.value}/abandon/`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      
      // 停止计时器和自动保存
      if (timerInterval.value) {
        clearInterval(timerInterval.value)
      }
      if (autoSaveInterval.value) {
        clearInterval(autoSaveInterval.value)
      }
      
      ElMessage.info('已放弃考试')
      router.push('/exam')
    } catch (error) {
      console.error('放弃考试失败:', error)
      ElMessage.error('操作失败: ' + (error.response?.data?.error || error.message))
    }
  } catch (e) {
    // 取消
  }
}

// 键盘快捷键处理
const handleKeyboard = (e) => {
  // 如果在输入框中，不处理快捷键
  if (['INPUT', 'TEXTAREA'].includes(e.target.tagName)) {
    return
  }
  
  switch (e.key) {
    case 'ArrowLeft':
      e.preventDefault()
      prevQuestion()
      break
    case 'ArrowRight':
      e.preventDefault()
      nextQuestion()
      break
    case '1':
    case '2':
    case '3':
    case '4':
      e.preventDefault()
      selectOptionByNumber(parseInt(e.key) - 1)
      break
    case 'Enter':
      e.preventDefault()
      if (currentQuestionIndex.value < totalQuestions.value - 1) {
        nextQuestion()
      }
      break
  }
}

// 通过数字选择选项
const selectOptionByNumber = (index) => {
  if (!currentQuestion.value || !isChoiceQuestion(currentQuestion.value.type)) {
    return
  }
  
  const options = parseOptions(currentQuestion.value.options)
  if (index >= 0 && index < options.length) {
    selectAnswer(currentQuestion.value.id, options[index])
  }
}

// 监听当前Section变化，处理音频
watch(() => currentSection.value, (newSection, oldSection) => {
  // 当切换到听力Section时，加载音频
  if (newSection && newSection.type === 'listening' && newSection.audio_url) {
    // 只在Section实际改变或首次进入听力Section时加载
    if (!oldSection || oldSection.id !== newSection.id) {
      setTimeout(() => {
        if (audioPlayer.value) {
          audioPlayer.value.load()
          // 尝试自动播放
          const playPromise = audioPlayer.value.play()
          if (playPromise !== undefined) {
            playPromise.catch(e => {
              console.log('自动播放失败，需要用户手动点击播放')
              ElMessage.info({ message: '请点击播放按钮开始听力', duration: 2000 })
            })
          }
        }
      }, 300)
    }
  }
}, { deep: true, immediate: true })

onMounted(() => {
  initExamData()
  // 添加键盘事件监听
  window.addEventListener('keydown', handleKeyboard)
})

onUnmounted(() => {
  // 清理计时器
  if (timerInterval.value) {
    clearInterval(timerInterval.value)
  }
  // 清理自动保存
  if (autoSaveInterval.value) {
    clearInterval(autoSaveInterval.value)
  }
  // 最后保存一次
  if (saveQueue.value.size > 0) {
    batchSaveAnswers()
  }
  // 移除键盘事件监听
  window.removeEventListener('keydown', handleKeyboard)
})
</script>

<style scoped>
.exam-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
}

/* 顶部固定栏 */
.exam-header-fixed {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left h2 {
  margin: 0 0 8px 0;
  font-size: 20px;
}

.header-center {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;
}

.header-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* 主体区域 */
.exam-body {
  display: flex;
  height: calc(100vh - 76px);
}

/* 左侧导航 */
.exam-sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e4e7ed;
  overflow-y: auto;
}

.section-nav {
  padding: 16px 0;
}

.section-item {
  margin-bottom: 8px;
}

.section-header {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.section-header:hover {
  background: #f5f7fa;
}

.section-item.is-active .section-header {
  background: #ecf5ff;
}

.section-icon {
  margin-right: 12px;
  color: #409eff;
}

.section-info {
  flex: 1;
}

.section-name {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.section-progress {
  font-size: 12px;
  color: #909399;
}

/* Part列表 */
.part-list {
  padding: 0 20px 12px;
}

.part-item {
  padding: 10px 16px;
  margin: 6px 0;
  background: #f5f7fa;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.part-item:hover {
  background: #e6f0ff;
}

.part-item.is-active {
  background: #409eff;
  color: white;
}

.part-item.is-completed {
  border: 2px solid #67c23a;
}

.part-number {
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 4px;
}

.part-name {
  font-size: 13px;
  margin-bottom: 4px;
}

.part-count {
  font-size: 11px;
  opacity: 0.8;
}

.part-check {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #67c23a;
  font-size: 20px;
}

/* 音频控制器 */
.audio-control {
  margin: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.audio-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 600;
  color: #409eff;
}

.audio-info {
  margin-top: 12px;
}

.audio-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #606266;
  margin-bottom: 8px;
}

.audio-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #909399;
}

/* 中间内容区 */
.exam-content {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.content-header {
  margin-bottom: 20px;
}

.part-title-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.part-title-bar h3 {
  margin: 0;
  font-size: 18px;
}

.question-nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
}

.question-indicator {
  font-size: 15px;
  font-weight: 600;
  color: #606266;
}

/* 题目卡片 */
.question-card {
  margin-bottom: 20px;
  position: relative;
}

.passage-section {
  margin-bottom: 24px;
  padding: 20px;
  background: #f9fafb;
  border-radius: 8px;
}

.passage-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 600;
  color: #409eff;
}

.passage-content {
  line-height: 1.8;
  color: #303133;
}

.question-content {
  margin: 20px 0;
}

.question-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.question-number {
  font-size: 16px;
  font-weight: 700;
  color: #409eff;
  flex-shrink: 0;
  padding: 6px 16px;
  background: linear-gradient(135deg, #ecf5ff 0%, #d9ecff 100%);
  border-radius: 20px;
  border: 1px solid #b3d8ff;
}

.question-divider {
  flex: 1;
  height: 2px;
  background: linear-gradient(90deg, #409eff 0%, transparent 100%);
  opacity: 0.2;
}

.question-text {
  font-size: 18px;
  line-height: 1.8;
  color: #303133;
  margin: 0;
}

.question-image {
  margin-top: 20px;
  text-align: center;
}

.question-image img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 8px;
}

/* 答题区域 */
.answer-section {
  margin-top: 24px;
}

.choice-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 图片选项 */
.image-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  margin: 20px 0;
  max-width: 800px; /* 限制最大宽度，避免图片太大 */
}

@media (min-width: 768px) {
  .image-options {
    grid-template-columns: repeat(2, 1fr); /* 中等屏幕2列 */
  }
}

@media (min-width: 1024px) {
  .image-options {
    grid-template-columns: repeat(4, 1fr); /* 大屏幕4列 */
  }
}

.image-option-item {
  position: relative;
  cursor: pointer;
  border-radius: 16px;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  border: 3px solid #e4e7ed;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.image-option-item:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 12px 32px rgba(64, 158, 255, 0.2);
  border-color: #409eff;
}

.image-option-item.is-selected {
  border-color: #67c23a;
  box-shadow: 0 12px 32px rgba(103, 194, 58, 0.35);
  transform: translateY(-6px) scale(1.02);
}

.image-option-label {
  position: absolute;
  top: 12px;
  left: 12px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  font-weight: 700;
  font-size: 18px;
  color: #409eff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 10;
  backdrop-filter: blur(8px);
}

.image-option-item.is-selected .image-option-label {
  background: #67c23a;
  color: white;
}

.image-option-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 100%; /* 1:1 正方形比例 */
  overflow: hidden;
  background: #f8f9fa;
}

.image-option-wrapper img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 自动裁剪适配 */
  object-position: center; /* 居中显示 */
  transition: transform 0.3s;
  background: #fff;
}

.image-option-item:hover .image-option-wrapper img {
  transform: scale(1.08); /* 悬停时稍微放大 */
  cursor: zoom-in;
}

.image-option-check {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255, 255, 255, 0.95);
  border-radius: 50%;
  padding: 8px;
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
}

.legacy-notice {
  margin-bottom: 16px;
}

.legacy-tip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #fdf6ec;
  border: 1px solid #f5dab1;
  border-radius: 6px;
  font-size: 13px;
  color: #e6a23c;
  margin-bottom: 16px;
}

.legacy-options {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: flex-start;
}

.legacy-option-item {
  background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
  border: 2px solid #e4e7ed;
  border-radius: 16px;
  width: 60px;
  height: 60px;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.legacy-option-item::after {
  content: '';
  position: absolute;
  inset: -2px;
  border-radius: 18px;
  background: linear-gradient(135deg, #409eff 0%, #3a8ee6 100%);
  opacity: 0;
  z-index: -1;
  transition: opacity 0.35s;
}

.legacy-option-item:hover {
  border-color: #409eff;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.2);
}

.legacy-option-item.is-selected {
  background: linear-gradient(145deg, #409eff 0%, #3a8ee6 100%);
  border-color: #409eff;
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.35), inset 0 2px 4px rgba(255, 255, 255, 0.2);
  transform: translateY(-4px) scale(1.05);
}

.legacy-option-item.is-selected::after {
  opacity: 1;
}

.option-letter {
  font-size: 24px;
  font-weight: 700;
  color: #606266;
  position: relative;
  z-index: 1;
  letter-spacing: -0.5px;
  user-select: none;
}

.legacy-option-item.is-selected .option-letter {
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.option-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: #f5f7fa;
  border: 2px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.option-item:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

.option-item.is-selected {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.option-label {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
  font-weight: 600;
  color: #409eff;
  flex-shrink: 0;
}

.option-item.is-selected .option-label {
  background: white;
  color: #409eff;
}

.option-content {
  flex: 1;
  font-size: 16px;
}

.option-check {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.judge-options {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.judge-item {
  flex: 1;
  max-width: 200px;
  padding: 40px 20px;
  text-align: center;
  background: #f5f7fa;
  border: 2px solid transparent;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.judge-item:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

.judge-item.is-selected {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.judge-item span {
  display: block;
  margin-top: 12px;
  font-size: 18px;
  font-weight: 600;
}

.fill-input-section {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

/* 底部操作栏 */
.content-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.footer-center {
  display: flex;
  gap: 12px;
}

/* 右侧答题卡 */
.exam-answer-sheet {
  width: 320px;
  background: white;
  border-left: 1px solid #e4e7ed;
  overflow-y: auto;
}

.sheet-header {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sheet-header h3 {
  margin: 0;
  font-size: 16px;
}

.sheet-content {
  padding: 16px;
}

.sheet-section {
  margin-bottom: 20px;
}

.sheet-section-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
  color: #303133;
}

.sheet-questions {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.sheet-question-item {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  font-weight: 600;
  color: #606266;
}

.sheet-question-item:hover {
  border-color: #409eff;
  color: #409eff;
}

.sheet-question-item.is-answered {
  background: #67c23a;
  border-color: #67c23a;
  color: white;
}

.sheet-question-item.is-current {
  background: #409eff;
  border-color: #409eff;
  color: white;
  transform: scale(1.1);
}

.sheet-legend {
  padding: 16px 20px;
  border-top: 1px solid #e4e7ed;
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
}

.legend-box {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 2px solid #dcdfe6;
}

.legend-box.is-answered {
  background: #67c23a;
  border-color: #67c23a;
}

.legend-box.is-current {
  background: #409eff;
  border-color: #409eff;
}

/* 题目列表抽屉 */
.question-list-drawer {
  padding: 20px;
}

.list-section {
  margin-bottom: 30px;
}

.list-section h3 {
  margin: 0 0 16px 0;
  font-size: 18px;
}

.list-part {
  margin-bottom: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.list-part h4 {
  margin: 0 0 12px 0;
  font-size: 15px;
  color: #606266;
}

.list-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

/* 响应式 */
@media (max-width: 1200px) {
  .exam-sidebar {
    width: 240px;
  }
  
  .exam-answer-sheet {
    width: 280px;
  }
  
  .sheet-questions {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 992px) {
  .exam-header-fixed {
    flex-wrap: wrap;
    padding: 12px 16px;
  }
  
  .header-left h2 {
    font-size: 16px;
  }
  
  .header-center {
    order: 3;
    width: 100%;
    margin: 12px 0 0 0;
  }
  
  .exam-body {
    flex-direction: column;
    height: auto;
  }
  
  .exam-sidebar {
    width: 100%;
    height: auto;
    max-height: none;
    border-right: none;
    border-bottom: 1px solid #e4e7ed;
  }
  
  .section-nav {
    display: flex;
    overflow-x: auto;
    padding: 12px 16px;
  }
  
  .section-item {
    margin: 0 8px 0 0;
    flex-shrink: 0;
  }
  
  .part-list {
    display: flex;
    overflow-x: auto;
    padding: 8px 16px;
  }
  
  .part-item {
    margin: 0 8px 0 0;
    flex-shrink: 0;
    min-width: 150px;
  }
  
  .audio-control {
    margin: 12px;
  }
  
  .exam-content {
    padding: 16px;
  }
  
  .question-nav-bar {
    flex-direction: column;
    gap: 12px;
  }
  
  .question-card {
    margin-bottom: 16px;
  }
  
  .option-item {
    padding: 12px 16px;
  }
  
  .content-footer {
    flex-direction: column;
    gap: 12px;
  }
  
  .footer-center {
    width: 100%;
    flex-direction: column;
  }
  
  .content-footer .el-button {
    width: 100%;
  }
  
  .exam-answer-sheet {
    width: 100%;
    height: auto;
    border-left: none;
    border-top: 1px solid #e4e7ed;
  }
  
  .sheet-questions {
    grid-template-columns: repeat(6, 1fr);
  }
  
  .sheet-question-item {
    width: 40px;
    height: 40px;
  }
}

@media (max-width: 768px) {
  .exam-header-fixed {
    padding: 10px 12px;
  }
  
  .header-left h2 {
    font-size: 14px;
    margin-bottom: 6px;
  }
  
  .exam-content {
    padding: 12px;
  }
  
  .part-title-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .question-text {
    font-size: 16px;
  }
  
  .option-label {
    width: 28px;
    height: 28px;
    font-size: 14px;
  }
  
  .option-content {
    font-size: 14px;
  }
  
  .judge-options {
    flex-direction: column;
  }
  
  .judge-item {
    max-width: 100%;
    padding: 30px 20px;
  }
  
  .sheet-questions {
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
  }
  
  .sheet-question-item {
    width: 36px;
    height: 36px;
    font-size: 13px;
  }
  
  .stat-row {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .header-center {
    font-size: 12px;
  }
  
  
  .passage-section {
    padding: 16px;
  }
  
  .choice-options {
    gap: 10px;
  }
  
  .option-item {
    padding: 10px 12px;
  }
  
  .fill-input-section {
    padding: 16px;
  }
  
  .sheet-questions {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .legacy-options {
    justify-content: center;
    gap: 12px;
  }
  
  .legacy-option-item {
    width: 56px;
    height: 56px;
  }
  
  .option-letter {
    font-size: 22px;
  }
  
  .legacy-tip {
    font-size: 12px;
    padding: 6px 12px;
  }
  
  .question-number {
    font-size: 14px;
    padding: 4px 12px;
  }
  
  .question-text {
    font-size: 16px;
  }
  
  .image-options {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 12px;
    max-width: 100%;
  }
  
  .image-option-label {
    width: 28px;
    height: 28px;
    font-size: 14px;
    top: 6px;
    left: 6px;
  }
  
  .image-option-item {
    border-radius: 12px;
  }
}
</style>
