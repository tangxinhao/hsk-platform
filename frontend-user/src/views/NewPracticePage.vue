<template>
  <div class="practice-page">
    <!-- 顶部统计卡片 -->
    <div class="stats-header">
      <div class="container">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #ecf5ff;">
                <el-icon color="#409eff" :size="28"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ totalPracticed }}</div>
                <div class="stat-label">已练习</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #f0f9ff;">
                <el-icon color="#67c23a" :size="28"><Select /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ correctRate }}%</div>
                <div class="stat-label">正确率</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #fef0f0;">
                <el-icon color="#f56c6c" :size="28"><Warning /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ wrongBookCount }}</div>
                <div class="stat-label">错题本</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card">
              <div class="stat-icon" style="background: #fdf6ec;">
                <el-icon color="#e6a23c" :size="28"><TrophyBase /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ streak }}</div>
                <div class="stat-label">连续天数</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <div class="container">
      <!-- 听力题组入口 -->
      <ListeningGroupEntry />
      
      <!-- 快速练习模式 -->
      <div class="quick-practice-section">
        <h2 class="section-title">
          <el-icon><MagicStick /></el-icon>
          快速开始
        </h2>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="mode-card" shadow="hover" @click="startQuickPractice('daily')">
              <div class="mode-icon daily">
                <el-icon :size="40"><Sunny /></el-icon>
              </div>
              <h3>每日练习</h3>
              <p>每天20道题，巩固知识</p>
              <el-tag size="small" type="success">推荐</el-tag>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="mode-card" shadow="hover" @click="startQuickPractice('random')">
              <div class="mode-icon random">
                <el-icon :size="40"><Refresh /></el-icon>
              </div>
              <h3>随机练习</h3>
              <p>随机抽取题目，全面复习</p>
              <el-tag size="small">20题</el-tag>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="mode-card" shadow="hover" @click="startQuickPractice('wrong')">
              <div class="mode-icon wrong">
                <el-icon :size="40"><Finished /></el-icon>
              </div>
              <h3>错题重做</h3>
              <p>针对性突破薄弱环节</p>
              <el-tag size="small" type="warning">{{ wrongBookCount }}题</el-tag>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 筛选和排序 -->
      <div class="filter-section">
        <div class="filter-header">
          <h2 class="section-title">
            <el-icon><Filter /></el-icon>
            题库练习
          </h2>
          <div class="filter-actions">
            <el-button :icon="Grid" :type="viewMode === 'grid' ? 'primary' : ''" @click="viewMode = 'grid'" circle />
            <el-button :icon="List" :type="viewMode === 'list' ? 'primary' : ''" @click="viewMode = 'list'" circle />
          </div>
        </div>

        <!-- 题目状态标签页 -->
        <div class="status-tabs">
          <el-radio-group v-model="statusFilter" @change="loadQuestions" size="large">
            <el-radio-button :value="'all'">
              <el-icon><Grid /></el-icon>
              全部题目
            </el-radio-button>
            <el-radio-button :value="'unanswered'">
              <el-icon><Document /></el-icon>
              未答题目
            </el-radio-button>
            <el-radio-button :value="'answered'">
              <el-icon><CircleCheck /></el-icon>
              已答题目
            </el-radio-button>
            <el-radio-button :value="'wrong'">
              <el-icon><Warning /></el-icon>
              错题本
            </el-radio-button>
          </el-radio-group>
        </div>

        <div class="filters">
          <el-select v-model="filters.level" placeholder="HSK等级" clearable @change="loadQuestions">
            <el-option label="全部等级" :value="0"></el-option>
            <el-option label="HSK 1" :value="1"></el-option>
            <el-option label="HSK 2" :value="2"></el-option>
            <el-option label="HSK 3" :value="3"></el-option>
            <el-option label="HSK 4" :value="4"></el-option>
            <el-option label="HSK 5" :value="5"></el-option>
            <el-option label="HSK 6" :value="6"></el-option>
          </el-select>

          <el-select v-model="filters.type" placeholder="题目类型" clearable @change="loadQuestions">
            <el-option label="全部类型" value=""></el-option>
            <el-option label="单选题" value="single"></el-option>
            <el-option label="多选题" value="multiple"></el-option>
            <el-option label="判断题" value="judge"></el-option>
            <el-option label="填空题" value="fill"></el-option>
            <el-option label="阅读题" value="reading"></el-option>
            <el-option label="书写题" value="writing"></el-option>
          </el-select>

          <el-select v-model="filters.difficulty" placeholder="难度" clearable @change="loadQuestions">
            <el-option label="全部难度" :value="0"></el-option>
            <el-option label="⭐ 简单" :value="1"></el-option>
            <el-option label="⭐⭐ 较易" :value="2"></el-option>
            <el-option label="⭐⭐⭐ 中等" :value="3"></el-option>
            <el-option label="⭐⭐⭐⭐ 较难" :value="4"></el-option>
            <el-option label="⭐⭐⭐⭐⭐ 困难" :value="5"></el-option>
          </el-select>

          <!-- 状态筛选后端尚未提供，先隐藏避免“未练习/已练习”无反应 -->

          <el-input 
            v-model="searchKeyword" 
            placeholder="搜索题目内容" 
            :prefix-icon="Search"
            clearable
            @input="handleSearch"
            style="width: 250px"
          />

          <el-button type="primary" @click="loadQuestions">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
        </div>
      </div>

      <!-- 题目列表 -->
      <div class="questions-section" v-loading="loading">
        <div v-if="questions.length === 0 && !loading" class="empty-state">
          <el-empty description="暂无题目">
            <el-button type="primary" @click="resetFilters">重置筛选</el-button>
          </el-empty>
        </div>

        <!-- 网格视图 -->
        <div v-else-if="viewMode === 'grid'" class="questions-grid">
          <el-card
            v-for="question in questions"
            :key="question.id"
            class="question-card"
            :class="{
              'is-practiced': question.is_practiced,
              'is-correct': question.is_correct_last_time === true,
              'is-wrong': question.is_correct_last_time === false
            }"
            shadow="hover"
          >
            <div class="question-header">
              <div class="question-meta">
                <el-tag :type="getTypeColor(question.type)" size="small">
                  {{ getTypeLabel(question.type) }}
                </el-tag>
                <el-tag type="info" size="small">HSK {{ question.level }}</el-tag>
                <!-- 练习状态标签 -->
                <el-tag v-if="question.is_practiced && question.is_correct_last_time === true" type="success" size="small">
                  <el-icon><CircleCheck /></el-icon> 已答对
                </el-tag>
                <el-tag v-else-if="question.is_practiced && question.is_correct_last_time === false" type="danger" size="small">
                  <el-icon><CircleClose /></el-icon> 待复习
                </el-tag>
                <el-tag v-else-if="question.is_practiced" type="warning" size="small">
                  <el-icon><Clock /></el-icon> 已练习
                </el-tag>
              </div>
              <div class="question-actions">
                <el-button 
                  :icon="question.is_favorite ? StarFilled : Star" 
                  circle 
                  size="small"
                  :type="question.is_favorite ? 'warning' : ''"
                  @click.stop="toggleFavorite(question)"
                  title="收藏"
                />
                <el-button 
                  v-if="question.is_practiced" 
                  :icon="CircleCheck" 
                  circle 
                  size="small"
                  :type="question.is_mastered ? 'success' : ''"
                  @click.stop="toggleMastered(question)"
                  title="标记掌握"
                />
              </div>
            </div>

            <div class="question-content">
              <div class="question-text">
                {{ question.content.length > 80 ? question.content.substring(0, 80) + '...' : question.content }}
              </div>
              <div class="question-difficulty">
                <span class="difficulty-label">难度:</span>
                <el-rate 
                  v-model="question.difficulty" 
                  disabled 
                  :max="5"
                  size="small"
                />
              </div>
            </div>

            <!-- 练习记录信息（仅已练习的题目显示）-->
            <div v-if="question.is_practiced" class="practice-info">
              <div class="practice-meta">
                <span class="practice-item">
                  <el-icon><View /></el-icon>
                  练习{{ question.practice_count || 0 }}次
                </span>
                <span v-if="question.last_practiced_at" class="practice-item">
                  <el-icon><Clock /></el-icon>
                  {{ formatTime(question.last_practiced_at) }}
                </span>
                <span v-if="question.practice_count > 0" class="practice-item">
                  <el-icon><TrendCharts /></el-icon>
                  正确率 {{ calculateAccuracy(question) }}%
                </span>
              </div>
            </div>

            <div class="question-footer">
              <div class="question-stats">
                <span v-if="question.practiced_count">
                  <el-icon><View /></el-icon>
                  {{ question.practiced_count }}
                </span>
                <span v-if="question.correct_rate">
                  <el-icon><TrendCharts /></el-icon>
                  {{ question.correct_rate }}%
                </span>
              </div>
              <div class="footer-actions">
                <el-button 
                  v-if="question.is_practiced" 
                  type="warning" 
                  size="small" 
                  plain
                  @click="restartPractice(question)"
                >
                  <el-icon><Refresh /></el-icon>
                  重做
                </el-button>
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="startPractice(question)"
                >
                  {{ question.is_practiced ? '继续练习' : '开始练习' }}
                </el-button>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 列表视图 -->
        <div v-else class="questions-list">
          <el-table :data="questions" stripe>
            <el-table-column type="index" label="#" width="60" />
            <el-table-column label="类型" width="100">
              <template #default="{ row }">
                <el-tag :type="getTypeColor(row.type)" size="small">
                  {{ getTypeLabel(row.type) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="题目内容" min-width="300">
              <template #default="{ row }">
                <div class="list-question-content">
                  {{ row.content }}
                  <el-icon v-if="row.audio_url" color="#e6a23c"><Headset /></el-icon>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="等级" width="80">
              <template #default="{ row }">
                <el-tag type="info" size="small">HSK{{ row.level }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="难度" width="150">
              <template #default="{ row }">
                <el-rate v-model="row.difficulty" disabled :max="5" size="small" />
              </template>
            </el-table-column>
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.is_mastered" type="success" size="small">已掌握</el-tag>
                <el-tag v-else-if="row.practiced_count" type="warning" size="small">已练习</el-tag>
                <el-tag v-else type="info" size="small">未练习</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button 
                  :icon="row.is_favorite ? StarFilled : Star" 
                  circle 
                  size="small"
                  @click="toggleFavorite(row)"
                />
                <el-button type="primary" size="small" @click="startPractice(row)">
                  练习
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-if="total > 0"
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[12, 24, 48, 96]"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total"
            @current-change="loadQuestions"
            @size-change="loadQuestions"
          />
        </div>
      </div>
    </div>

    <!-- 练习对话框 -->
    <el-dialog 
      v-model="practiceDialog" 
      :title="`第${currentQuestionIndex + 1}题 / 共${practiceQuestions.length}题`"
      width="800px"
      :close-on-click-modal="false"
    >
      <div v-if="currentPracticeQuestion" class="practice-dialog">
        <div class="dialog-header">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: practiceProgress + '%' }"></div>
          </div>
          <div class="dialog-meta">
            <el-tag :type="getTypeColor(currentPracticeQuestion.type)">
              {{ getTypeLabel(currentPracticeQuestion.type) }}
            </el-tag>
            <el-tag type="info">HSK {{ currentPracticeQuestion.level }}</el-tag>
            <span class="difficulty-stars">
              <el-rate 
                v-model="currentPracticeQuestion.difficulty" 
                disabled 
                :max="5"
                size="small"
              />
            </span>
          </div>
        </div>

        <div class="dialog-question">
          <h3>{{ currentPracticeQuestion.content }}</h3>
        </div>

        <div class="dialog-options">
          <!-- 单选题 - 图片选项 -->
          <div v-if="(currentPracticeQuestion.type === 'single' || currentPracticeQuestion.type === 'listening' || currentPracticeQuestion.type === 'reading') && currentPracticeQuestion.option_type === 'image'" class="image-options-practice">
            <div
              v-for="(option, index) in parseOptions(currentPracticeQuestion.options)"
              :key="index"
              class="image-option-practice"
              :class="{
                'is-selected': userAnswer === getOptionValue(option, index),
                'is-disabled': showAnswer,
                'is-correct': showAnswer && getOptionValue(option, index) === currentPracticeQuestion.answer,
                'is-wrong': showAnswer && userAnswer === getOptionValue(option, index) && userAnswer !== currentPracticeQuestion.answer
              }"
              @click="!showAnswer && (userAnswer = getOptionValue(option, index))"
            >
              <div class="image-option-label-practice">{{ String.fromCharCode(65 + index) }}</div>
              <div class="image-option-wrapper-practice">
                <img 
                  :src="getOptionValue(option, index)" 
                  :alt="`选项${String.fromCharCode(65 + index)}`"
                  loading="lazy"
                />
                <div v-if="userAnswer === getOptionValue(option, index)" class="image-check-practice">
                  <el-icon :size="40" color="white"><Check /></el-icon>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 单选题 - 文字选项 -->
          <div v-else-if="currentPracticeQuestion.type === 'single' || currentPracticeQuestion.type === 'listening' || currentPracticeQuestion.type === 'reading'" class="custom-radio-group">
            <div
              v-for="(option, index) in parseOptions(currentPracticeQuestion.options)"
              :key="index"
              class="custom-radio-option"
              :class="{
                'is-selected': userAnswer === getOptionValue(option, index),
                'is-disabled': showAnswer,
                'is-correct': showAnswer && getOptionValue(option, index) === currentPracticeQuestion.answer,
                'is-wrong': showAnswer && userAnswer === getOptionValue(option, index) && userAnswer !== currentPracticeQuestion.answer
              }"
              @click="!showAnswer && (userAnswer = getOptionValue(option, index))"
            >
              <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
              <div class="option-text">{{ getOptionText(option) }}</div>
              <div class="option-indicator">
                <el-icon v-if="userAnswer === getOptionValue(option, index)"><Check /></el-icon>
              </div>
            </div>
          </div>

          <!-- 多选题 - 图片选项 -->
          <div v-if="currentPracticeQuestion.type === 'multiple' && currentPracticeQuestion.option_type === 'image'" class="image-options-practice">
            <div
              v-for="(option, index) in parseOptions(currentPracticeQuestion.options)"
              :key="index"
              class="image-option-practice"
              :class="{
                'is-selected': Array.isArray(userAnswer) && userAnswer.includes(getOptionValue(option, index)),
                'is-disabled': showAnswer
              }"
              @click="!showAnswer && toggleMultipleOption(getOptionValue(option, index))"
            >
              <div class="image-option-label-practice">{{ String.fromCharCode(65 + index) }}</div>
              <div class="image-option-wrapper-practice">
                <img 
                  :src="getOptionValue(option, index)" 
                  :alt="`选项${String.fromCharCode(65 + index)}`"
                  loading="lazy"
                />
                <div v-if="Array.isArray(userAnswer) && userAnswer.includes(getOptionValue(option, index))" class="image-check-practice">
                  <el-icon :size="40" color="white"><Check /></el-icon>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 多选题 - 文字选项 -->
          <div v-else-if="currentPracticeQuestion.type === 'multiple'" class="custom-checkbox-group">
            <div
              v-for="(option, index) in parseOptions(currentPracticeQuestion.options)"
              :key="index"
              class="custom-checkbox-option"
              :class="{
                'is-selected': Array.isArray(userAnswer) && userAnswer.includes(getOptionValue(option, index)),
                'is-disabled': showAnswer
              }"
              @click="!showAnswer && toggleMultipleOption(getOptionValue(option, index))"
            >
              <div class="option-checkbox">
                <el-icon v-if="Array.isArray(userAnswer) && userAnswer.includes(getOptionValue(option, index))"><Check /></el-icon>
              </div>
              <div class="option-label">{{ String.fromCharCode(65 + index) }}</div>
              <div class="option-text">{{ getOptionText(option) }}</div>
            </div>
          </div>

          <!-- 判断题 -->
          <el-radio-group 
            v-else-if="currentPracticeQuestion.type === 'judge'" 
            v-model="userAnswer"
            :disabled="showAnswer"
          >
            <el-radio label="正确" size="large">正确</el-radio>
            <el-radio label="错误" size="large">错误</el-radio>
          </el-radio-group>

          <!-- 填空题 -->
          <el-input
            v-else-if="currentPracticeQuestion.type === 'fill'"
            v-model="userAnswer"
            placeholder="请输入答案"
            size="large"
            :disabled="showAnswer"
          />
          
          <!-- 书写题 -->
          <el-input
            v-else-if="currentPracticeQuestion.type === 'writing'"
            v-model="userAnswer"
            type="textarea"
            :rows="6"
            placeholder="请根据提示写出完整的句子或段落"
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
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import ListeningGroupEntry from '../components/ListeningGroupEntry.vue'
import { 
  Document, Select, Warning, TrophyBase, MagicStick, Sunny, Refresh, Finished,
  Filter, Grid, List, Search, Headset, Star, StarFilled, View, TrendCharts,
  CircleCheck, CircleClose, Clock
} from '@element-plus/icons-vue'
import axios from 'axios'

// 数据定义
const loading = ref(false)
const questions = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const viewMode = ref('grid') // grid 或 list
const searchKeyword = ref('')
const statusFilter = ref('all') // all, unanswered, answered, wrong

// 统计数据（后端输出）
const totalPracticed = ref(0)
const correctRate = ref(0)
const wrongBookCount = ref(0)
const streak = ref(0)

// 筛选条件
const filters = reactive({
  level: 0,
  type: '',
  difficulty: 0
})

// 练习相关
const practiceDialog = ref(false)
const practiceQuestions = ref([])
const currentQuestionIndex = ref(0)
const userAnswer = ref('')
const showAnswer = ref(false)
const isCorrect = ref(false)
const practiceStats = reactive({
  correct: 0,
  total: 0
})

const currentPracticeQuestion = computed(() => practiceQuestions.value[currentQuestionIndex.value])
const practiceProgress = computed(() => {
  if (practiceQuestions.value.length === 0) return 0
  return ((currentQuestionIndex.value + 1) / practiceQuestions.value.length) * 100
})

// 加载题目列表
const loadQuestions = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      exclude_groups: 'true'  // 排除听力题组中的题目
    }

    if (filters.level) params.level = filters.level
    if (filters.difficulty) params.difficulty = filters.difficulty
    if (searchKeyword.value) params.search = searchKeyword.value
    
    // 完全排除听力题型和听力题组
    params.exclude_groups = 'true'
    
    // 根据状态筛选
    if (statusFilter.value === 'unanswered') {
      params.is_practiced = 'false'
    } else if (statusFilter.value === 'answered') {
      params.is_practiced = 'true'
    } else if (statusFilter.value === 'wrong') {
      params.is_practiced = 'true'
      params.is_correct = 'false'
    }
    
    // 映射前端选择到后端实际题型/前缀
    if (filters.type) {
      const typeMap = {
        'fill': 'reading_fill_blank',
      }
      if (filters.type === 'listening' || filters.type === 'reading' || filters.type === 'writing') {
        params.type_like = filters.type
      } else {
        params.type = typeMap[filters.type] || filters.type
      }
    }

    console.log('请求参数:', params)
    const response = await axios.get('/question/questions/', { params })
    console.log('返回数据:', response.data)
    questions.value = response.data.results || response.data
    total.value = response.data.count || questions.value.length

    // 模拟一些额外数据
    questions.value = questions.value.map(q => ({
      ...q,
      is_favorite: false,
      practiced_count: Math.floor(Math.random() * 100),
      correct_rate: Math.floor(Math.random() * 100),
      is_mastered: Math.random() > 0.7
    }))

  } catch (error) {
    console.error('加载题目失败:', error)
    ElMessage.error('加载题目失败')
  } finally {
    loading.value = false
  }
}

// 加载统计数据（从后端）
const loadStats = async () => {
  try {
    const resp = await axios.get('/user/progress/overview/')
    const data = resp.data || {}
    totalPracticed.value = data.total_practices || 0
    correctRate.value = data.correct_rate || 0
    wrongBookCount.value = data.wrong_count || 0
    streak.value = data.study_days || 0
  } catch (err) {
    console.error('加载统计失败:', err)
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  loadQuestions()
}

// 重置筛选
const resetFilters = () => {
  filters.level = 0
  filters.type = ''
  filters.difficulty = 0
  searchKeyword.value = ''
  loadQuestions()
}

// 快速练习
const startQuickPractice = async (mode) => {
  try {
    let params = { page_size: 20 }
    
    if (mode === 'daily') {
      ElMessage.info('开始每日练习...')
    } else if (mode === 'random') {
      ElMessage.info('开始随机练习...')
    } else if (mode === 'wrong') {
      if (wrongBookCount.value === 0) {
        ElMessage.warning('错题本为空')
        return
      }
      ElMessage.info('开始错题练习...')
      params.wrong_only = true
    }

    const response = await axios.get('/question/questions/', { params })
    practiceQuestions.value = response.data.results || response.data
    
    if (practiceQuestions.value.length === 0) {
      ElMessage.warning('没有可练习的题目')
      return
    }

    startPracticeMode()
  } catch (error) {
    console.error('开始练习失败:', error)
    ElMessage.error('开始练习失败')
  }
}

// 开始单题练习
const startPractice = (question) => {
  practiceQuestions.value = [question]
  startPracticeMode()
}

// 启动练习模式
const startPracticeMode = () => {
  currentQuestionIndex.value = 0
  userAnswer.value = practiceQuestions.value[0]?.type === 'multiple' ? [] : ''
  showAnswer.value = false
  practiceStats.correct = 0
  practiceStats.total = 0
  practiceDialog.value = true
}

// 提交答案
const submitAnswer = async () => {
  if (!userAnswer.value || (Array.isArray(userAnswer.value) && userAnswer.value.length === 0)) {
    ElMessage.warning('请选择答案')
    return
  }

  let answer = userAnswer.value
  
  // 如果是图片选项，需要将URL转换为字母
  if (currentPracticeQuestion.value.option_type === 'image') {
    const options = parseOptions(currentPracticeQuestion.value.options)
    
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

  const correctAnswer = currentPracticeQuestion.value.answer.trim()
  const userAnswerTrimmed = String(answer).trim()
  
  console.log('用户答案:', userAnswerTrimmed, '正确答案:', correctAnswer)
  isCorrect.value = userAnswerTrimmed === correctAnswer
  showAnswer.value = true
  practiceStats.total++
  
  if (isCorrect.value) {
    practiceStats.correct++
  }
  
  // 提交答题记录到后端
  try {
    await axios.post('/question/answer/', {
      question_id: currentPracticeQuestion.value.id,
      user_answer: userAnswerTrimmed
    })
  } catch (error) {
    console.error('提交答题记录失败:', error)
  }
}

// 切换多选选项
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

// 下一题
const nextQuestion = () => {
  if (currentQuestionIndex.value < practiceQuestions.value.length - 1) {
    currentQuestionIndex.value++
    userAnswer.value = practiceQuestions.value[currentQuestionIndex.value]?.type === 'multiple' ? [] : ''
    showAnswer.value = false
  }
}

// 完成练习
const completePractice = () => {
  const score = Math.round((practiceStats.correct / practiceStats.total) * 100)
  ElMessage.success(`练习完成！答对 ${practiceStats.correct}/${practiceStats.total} 题，正确率 ${score}%`)
  closePractice()
  loadStats() // 刷新统计数据
  loadQuestions() // 重新加载题目列表以更新练习状态
}

// 关闭练习
const closePractice = () => {
  practiceDialog.value = false
  practiceQuestions.value = []
  currentQuestionIndex.value = 0
  userAnswer.value = ''
  showAnswer.value = false
}

// 收藏/取消收藏
const toggleFavorite = (question) => {
  question.is_favorite = !question.is_favorite
  ElMessage.success(question.is_favorite ? '已收藏' : '已取消收藏')
}

// 标记掌握/取消掌握
const toggleMastered = (question) => {
  question.is_mastered = !question.is_mastered
  ElMessage.success(question.is_mastered ? '已标记为掌握' : '已取消掌握标记')
  // TODO: 调用后端API保存掌握状态
}

// 重做题目
const restartPractice = (question) => {
  ElMessage.info('重新开始练习此题目')
  startPractice(question)
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
  
  if (days > 0) {
    return `${days}天前`
  } else if (hours > 0) {
    return `${hours}小时前`
  } else if (minutes > 0) {
    return `${minutes}分钟前`
  } else {
    return '刚刚'
  }
}

// 计算正确率
const calculateAccuracy = (question) => {
  if (!question.practice_count || question.practice_count === 0) return 0
  // 如果有is_correct_last_time，假设正确率基于此
  // 实际应该从后端获取真实的正确率数据
  if (question.is_correct_last_time === true) {
    return 100
  } else if (question.is_correct_last_time === false) {
    return 0
  }
  return 50
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

// 获取选项的值（用于v-model绑定）
const getOptionValue = (option, index) => {
  if (typeof option === 'string') {
    return option
  }
  return option.value || option.label || String.fromCharCode(65 + index)
}

// 获取选项的显示文本
const getOptionText = (option) => {
  if (typeof option === 'string') {
    return option
  }
  return option.text || option.label || option.value || ''
}

// 获取类型颜色
const getTypeColor = (type) => {
  if (!type) return 'info'
  const t = normalizeType(type)
  const colorMap = {
    'single': 'primary',
    'multiple': 'success',
    'judge': 'warning',
    'fill': 'info',
    'reading': 'info',
    'writing': 'danger'
  }
  return colorMap[t] || 'info'
}

// 获取类型标签
const getTypeLabel = (type) => {
  if (!type) return '未知题型'
  const t = normalizeType(type)
  const labelMap = {
    'single': '单选题',
    'multiple': '多选题',
    'judge': '判断题',
    'fill': '填空题',
    'reading': '阅读题',
    'writing': '书写题'
  }
  return labelMap[t] || t
}

// 规范化后端题型
const normalizeType = (type) => {
  if (!type) return ''
  const lower = String(type).toLowerCase()
  if (lower.includes('reading')) return 'reading'
  if (lower.includes('writing') || lower.includes('write')) return 'writing'
  if (lower.includes('fill')) return 'fill'
  return lower
}

onMounted(() => {
  loadQuestions()
  loadStats()
})
</script>

<style scoped>
.practice-page {
  min-height: 100vh;
  background: #f5f7fa;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* 统计头部 */
.stats-header {
  background: white;
  padding: 30px 0;
  margin-bottom: 30px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  border: 1px solid #eee;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
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
  font-size: 32px;
  font-weight: 700;
  color: #333333;
  line-height: 1;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

/* 快速练习 */
.quick-practice-section {
  margin-bottom: 40px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 20px;
}

.mode-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.mode-card:hover {
  border-color: #667eea;
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.2);
}

.mode-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.mode-icon.daily {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.mode-icon.random {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.mode-icon.wrong {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.mode-card h3 {
  font-size: 18px;
  margin: 10px 0;
  color: #333333;
}

.mode-card p {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
}

/* 筛选区域 */
.filter-section {
  background: white;
  padding: 25px;
  border-radius: 12px;
  margin-bottom: 25px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.status-tabs {
  margin-bottom: 20px;
}

.status-tabs :deep(.el-radio-group) {
  display: flex;
  gap: 12px;
}

.status-tabs :deep(.el-radio-button) {
  flex: 1;
}

.status-tabs :deep(.el-radio-button__inner) {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 12px 20px;
  border-radius: 10px;
  transition: all 0.3s;
}

.status-tabs :deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.filter-actions {
  display: flex;
  gap: 10px;
}

.filters {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.filters .el-select {
  width: 150px;
}

/* 题目列表 */
.questions-section {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  min-height: 500px;
}

.questions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.question-card {
  transition: all 0.3s;
  border: 2px solid transparent;
  position: relative;
}

.question-card.is-practiced {
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
}

.question-card.is-practiced::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  border-radius: 4px 0 0 4px;
}

.question-card.is-correct::before {
  background: linear-gradient(180deg, #67c23a 0%, #85ce61 100%);
}

.question-card.is-wrong::before {
  background: linear-gradient(180deg, #f56c6c 0%, #f78787 100%);
}

.question-card:hover {
  border-color: #667eea;
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
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

.question-content {
  margin-bottom: 15px;
  min-height: 80px;
}

.question-text {
  font-size: 15px;
  line-height: 1.6;
  color: #333333;
  margin-bottom: 10px;
}

.question-difficulty {
  display: flex;
  align-items: center;
  gap: 8px;
}

.difficulty-label {
  font-size: 13px;
  color: #666;
}

.practice-info {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  padding: 10px 12px;
  border-radius: 8px;
  margin-bottom: 12px;
}

.practice-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.practice-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #606266;
}

.practice-item .el-icon {
  font-size: 14px;
  color: #909399;
}

.question-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.footer-actions {
  display: flex;
  gap: 8px;
}

.question-stats {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: #666;
}

.question-stats span {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 列表视图 */
.list-question-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* 练习对话框 */
.practice-dialog {
  padding: 20px 0;
}

.dialog-header {
  margin-bottom: 25px;
}

.progress-bar {
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s;
}

.dialog-meta {
  display: flex;
  gap: 10px;
  align-items: center;
}

.dialog-question h3 {
  font-size: 18px;
  line-height: 1.8;
  color: #333333;
  margin-bottom: 20px;
}

.audio-section {
  background: #f0f9ff;
  padding: 15px;
  border-radius: 8px;
  margin: 15px 0;
}

.audio-tip {
  margin: 10px 0 0;
  font-size: 14px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 5px;
}

.dialog-options {
  margin: 25px 0;
}

/* 自定义单选题样式 */
.custom-radio-group,
.custom-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-height: 340px;
  overflow-y: auto;
  padding: 2px;
}

.custom-radio-option,
.custom-checkbox-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 2px solid #e8eaed;
  border-radius: 8px;
  background: linear-gradient(135deg, #ffffff 0%, #fafbfc 100%);
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  min-height: 40px;
}

.custom-radio-option::before,
.custom-checkbox-option::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 5px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  transform: scaleY(0);
  transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.custom-radio-option:hover,
.custom-checkbox-option:hover {
  border-color: #667eea;
  background: linear-gradient(135deg, #f8f9ff 0%, #fafbff 100%);
  transform: translateX(6px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.18);
}

.custom-radio-option:hover::before,
.custom-checkbox-option:hover::before {
  transform: scaleY(1);
}

.custom-radio-option.is-selected,
.custom-checkbox-option.is-selected {
  border-color: #667eea;
  background: linear-gradient(135deg, #ecf2ff 0%, #f5f7ff 100%);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.28);
  transform: translateX(6px);
}

.custom-radio-option.is-selected::before,
.custom-checkbox-option.is-selected::before {
  transform: scaleY(1);
}

.custom-radio-option.is-correct {
  border-color: #67c23a;
  background: linear-gradient(135deg, #f0f9ff 0%, #e8f5e9 100%);
}

.custom-radio-option.is-correct::before {
  background: linear-gradient(180deg, #67c23a 0%, #85ce61 100%);
}

.custom-radio-option.is-wrong {
  border-color: #f56c6c;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
}

.custom-radio-option.is-wrong::before {
  background: linear-gradient(180deg, #f56c6c 0%, #f78787 100%);
}

.custom-radio-option.is-disabled,
.custom-checkbox-option.is-disabled {
  cursor: not-allowed;
  opacity: 0.8;
}

.option-label {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #f0f2f5 0%, #e8eaed 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: #606266;
  flex-shrink: 0;
  transition: all 0.35s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.custom-radio-option:hover .option-label,
.custom-checkbox-option:hover .option-label {
  transform: scale(1.08);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.custom-radio-option.is-selected .option-label,
.custom-checkbox-option.is-selected .option-label {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  transform: scale(1.12);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.custom-radio-option.is-correct .option-label {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  color: white;
}

.custom-radio-option.is-wrong .option-label {
  background: linear-gradient(135deg, #f56c6c 0%, #f78787 100%);
  color: white;
}

.option-text {
  flex: 1;
  font-size: 13px;
  line-height: 1.3;
  color: #303133;
  font-weight: 500;
  word-wrap: break-word;
}

.custom-radio-option.is-selected .option-text,
.custom-checkbox-option.is-selected .option-text {
  color: #667eea;
  font-weight: 600;
}

.option-indicator {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0);
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  flex-shrink: 0;
}

.custom-radio-option.is-selected .option-indicator {
  opacity: 1;
  transform: scale(1);
}

.option-indicator .el-icon {
  color: white;
  font-size: 14px;
  font-weight: bold;
}

/* 多选框特殊样式 */
.option-checkbox {
  width: 24px;
  height: 24px;
  border: 2px solid #dcdfe6;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  flex-shrink: 0;
}

.custom-checkbox-option.is-selected .option-checkbox {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
}

.option-checkbox .el-icon {
  color: white;
  font-size: 16px;
  font-weight: bold;
}

.answer-section {
  margin-top: 25px;
}

.answer-details p {
  margin: 8px 0;
  line-height: 1.6;
}

.pagination-container {
  display: flex;
  justify-content: center;
  padding: 30px 0 10px;
}

/* 图片选项样式 */
.image-options-practice {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 15px;
  margin: 20px 0;
}

.image-option-practice {
  position: relative;
  background: #ffffff;
  border: 3px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.image-option-practice:hover {
  border-color: #667eea;
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.25);
}

.image-option-practice.is-selected {
  border-color: #667eea;
  background: linear-gradient(145deg, #667eea, #764ba2);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  transform: scale(1.05);
}

.image-option-practice.is-correct {
  border-color: #67c23a;
  background: linear-gradient(145deg, #67c23a, #85ce61);
}

.image-option-practice.is-wrong {
  border-color: #f56c6c;
  background: linear-gradient(145deg, #f56c6c, #f78989);
}

.image-option-practice.is-disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.image-option-label-practice {
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

.image-option-practice.is-selected .image-option-label-practice {
  background: white;
  color: #667eea;
  transform: scale(1.1);
}

.image-option-wrapper-practice {
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

.image-option-wrapper-practice img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  transition: transform 0.3s;
}

.image-option-practice:hover .image-option-wrapper-practice img {
  transform: scale(1.08);
}

.image-check-practice {
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
  animation: checkBounce 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes checkBounce {
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
  .questions-grid {
    grid-template-columns: 1fr;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .filters .el-select,
  .filters .el-input {
    width: 100% !important;
  }
  
  .image-options-practice {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
  
  .image-option-wrapper-practice {
    width: 120px;
    height: 120px;
  }
}
</style>
