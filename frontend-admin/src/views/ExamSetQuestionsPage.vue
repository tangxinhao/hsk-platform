<template>
  <div class="exam-set-questions-page">
    <div class="page-header">
      <div class="header-left">
        <el-button @click="goBack" icon="ArrowLeft">返回</el-button>
        <div class="title-section">
          <h2>{{ examSetTitle }}</h2>
          <el-tag type="warning" size="large">HSK{{ examSetLevel }}</el-tag>
        </div>
      </div>
      <el-button type="primary" icon="Plus" @click="showAddDialog">
        添加题目
      </el-button>
    </div>

    <!-- 听力音频设置 -->
    <el-card class="audio-settings-card">
      <template #header>
        <div class="card-header">
          <el-icon><Headset /></el-icon>
          <span>听力音频设置</span>
          <el-tag size="small" type="info" style="margin-left: 8px">统一音频</el-tag>
        </div>
      </template>
      
      <div class="audio-settings-content">
        <el-alert
          title="为整套听力section设置统一音频，所有听力题目将共享此音频"
          type="info"
          :closable="false"
          show-icon
          style="margin-bottom: 16px"
        />
        
        <el-form :inline="true">
          <el-form-item label="听力音频URL">
            <el-input
              v-model="listeningAudioUrl"
              placeholder="/media/audio/H11556.mp3 或 http://..."
              style="width: 450px"
            >
              <template #prepend>
                <el-icon><Link /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="saveListeningAudio" :loading="savingAudio">
              <el-icon><Check /></el-icon>
              保存音频设置
            </el-button>
          </el-form-item>
        </el-form>
        
        <div class="audio-tip">
          <el-icon><InfoFilled /></el-icon>
          <span>音频时长将在前端播放时自动获取，无需手动设置</span>
        </div>
        
        <div v-if="examSetData.listening_audio_url" class="current-audio">
          <el-tag type="success" size="large">
            <el-icon><SuccessFilled /></el-icon>
            当前音频: {{ examSetData.listening_audio_url }}
          </el-tag>
        </div>
      </div>
    </el-card>

    <!-- Section标签页 -->
    <el-card class="section-tabs-card">
      <el-radio-group v-model="currentSection" size="large" @change="filterQuestions">
        <el-radio-button value="all">全部题目</el-radio-button>
        <el-radio-button value="listening">听力</el-radio-button>
        <el-radio-button value="reading">阅读</el-radio-button>
        <el-radio-button value="writing">书写</el-radio-button>
      </el-radio-group>

      <div class="stats-info">
        <el-tag type="info">共 {{ filteredQuestions.length }} 题</el-tag>
      </div>
    </el-card>

    <!-- 题目列表 -->
    <el-card class="table-card">
      <el-table
        :data="paginatedQuestions"
        v-loading="loading"
        style="width: 100%"
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="部分" width="100">
          <template #default="{ row }">
            <el-tag :type="getSectionColor(row.section_type)" size="small">
              {{ getSectionLabel(row.section_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="part_number" label="Part" width="80" />
        <el-table-column prop="question_number" label="题号" width="80" />
        <el-table-column label="题型" width="100">
          <template #default="{ row }">
            <el-tag size="small">{{ getTypeLabel(row.type) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="题目内容" min-width="300" show-overflow-tooltip />
        <el-table-column prop="answer" label="答案" width="150" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="editQuestion(row)">
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deleteQuestion(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination" v-if="filteredQuestions.length > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredQuestions.length"
        />
      </div>

      <el-empty v-if="!loading && filteredQuestions.length === 0" description="暂无题目" />
    </el-card>

    <!-- 添加/编辑题目对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'add' ? '添加题目' : '编辑题目'"
      width="800px"
      :close-on-click-modal="false"
    >
      <el-form
        :model="formData"
        :rules="formRules"
        ref="formRef"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部分类型" prop="section_type">
              <el-select v-model="formData.section_type" placeholder="选择部分">
                <el-option label="听力" value="listening" />
                <el-option label="阅读" value="reading" />
                <el-option label="书写" value="writing" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="题目类型" prop="type">
              <el-select v-model="formData.type" placeholder="选择题型">
                <el-option label="单选题" value="single" />
                <el-option label="多选题" value="multiple" />
                <el-option label="判断题" value="judge" />
                <el-option label="填空题" value="fill" />
                <el-option label="阅读题" value="reading" />
                <el-option label="书写题" value="writing" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="Part编号" prop="part_number">
              <el-input-number v-model="formData.part_number" :min="1" :max="10" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="题号" prop="question_number">
              <el-input-number v-model="formData.question_number" :min="1" :max="200" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="难度" prop="difficulty">
              <el-select v-model="formData.difficulty">
                <el-option label="简单" :value="1" />
                <el-option label="较易" :value="2" />
                <el-option label="中等" :value="3" />
                <el-option label="较难" :value="4" />
                <el-option label="困难" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="题目内容" prop="content">
          <el-input
            v-model="formData.content"
            type="textarea"
            :rows="3"
            placeholder="请输入题目内容"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="选项类型" v-if="['single', 'multiple', 'reading'].includes(formData.type)">
          <el-radio-group v-model="formData.option_type">
            <el-radio value="text">
              <el-icon><Reading /></el-icon>
              文字选项
            </el-radio>
            <el-radio value="image">
              <el-icon><Picture /></el-icon>
              图片选项
            </el-radio>
          </el-radio-group>
          <div style="font-size: 12px; color: #909399; margin-top: 4px;">
            <span v-if="formData.option_type === 'text'">选项内容为文字（如：A. 苹果 B. 香蕉）</span>
            <div v-else style="line-height: 1.8;">
              <div style="font-weight: 600; color: #409eff; margin-bottom: 4px;">
                📸 图片上传说明
              </div>
              <div>• <strong>推荐尺寸：</strong>400x400px 或 600x600px（正方形）</div>
              <div>• <strong>支持格式：</strong>JPG、PNG、GIF、WebP</div>
              <div>• <strong>本地路径：</strong>/media/images/option_a.jpg</div>
              <div>• <strong>外部链接：</strong>https://example.com/image.png</div>
              <div style="margin-top: 4px; color: #67c23a;">
                ✓ 系统会自动缩放适配，无需担心尺寸不符
              </div>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="选项" v-if="['single', 'multiple', 'reading'].includes(formData.type)">
          <div class="options-editor">
            <div v-for="(option, index) in formData.options_list" :key="index" class="option-item-container">
              <el-input
                v-model="formData.options_list[index]"
                :placeholder="formData.option_type === 'image' 
                  ? (index === 0 ? '可输入本地路径或外部链接' : `选项 ${String.fromCharCode(65 + index)} 图片URL`)
                  : `选项 ${String.fromCharCode(65 + index)}`"
                style="margin-bottom: 10px"
              >
                <template #prepend v-if="formData.option_type === 'text'">
                  {{ String.fromCharCode(65 + index) }}
                </template>
                <template #prepend v-else>
                  <el-icon><Picture /></el-icon>
                  {{ String.fromCharCode(65 + index) }}
                </template>
                <template #append>
                  <el-button @click="removeOption(index)" icon="Close" />
                </template>
              </el-input>
              <div v-if="formData.option_type === 'image' && formData.options_list[index]" class="image-preview">
                <el-popover
                  placement="right"
                  :width="300"
                  trigger="hover"
                >
                  <template #reference>
                    <div class="preview-thumbnail">
                      <img 
                        :src="formData.options_list[index]" 
                        @error="handleImageError" 
                        alt="预览"
                      />
                      <div class="preview-overlay">
                        <el-icon><ZoomIn /></el-icon>
                      </div>
                    </div>
                  </template>
                  <div class="preview-large">
                    <img 
                      :src="formData.options_list[index]" 
                      style="width: 100%; border-radius: 4px;"
                      alt="大图预览"
                    />
                  </div>
                </el-popover>
              </div>
            </div>
            <el-button @click="addOption" icon="Plus" style="width: 100%">添加选项</el-button>
          </div>
        </el-form-item>

        <el-form-item label="正确答案" prop="answer">
          <el-input
            v-model="formData.answer"
            placeholder="请输入正确答案"
            maxlength="500"
          />
        </el-form-item>

        <el-form-item label="答案解析">
          <el-input
            v-model="formData.explanation"
            type="textarea"
            :rows="3"
            placeholder="请输入答案解析"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <!-- 听力部分提示 -->
        <el-alert
          v-if="formData.section_type === 'listening'"
          type="success"
          :closable="false"
          show-icon
          style="margin-top: 16px;"
        >
          <template #title>
            <span v-if="examSetData.listening_audio_url">✓ 该套卷已设置统一听力音频，所有听力题共享此音频</span>
            <span v-else>⚠️ 请先在上方"统一听力音频设置"中添加听力音频</span>
          </template>
        </el-alert>

        <!-- 阅读题目配图（仅阅读理解题型需要） -->
        <el-form-item 
          label="题目配图" 
          v-if="formData.section_type === 'reading' && formData.type === 'reading' && formData.option_type !== 'image'"
        >
          <el-input
            v-model="formData.image_url"
            placeholder="支持本地路径或外部链接，如：https://example.com/image.png"
          >
            <template #prepend>
              <el-icon><Picture /></el-icon>
            </template>
          </el-input>
          <div style="font-size: 12px; color: #909399; margin-top: 4px;">
            用于阅读文章的配图（可选），支持本地路径和外部URL
          </div>
        </el-form-item>

        <!-- 材料组标识（仅阅读部分需要） -->
        <el-form-item 
          label="材料组标识" 
          v-if="formData.section_type === 'reading'"
        >
          <el-input
            v-model="formData.material_group"
            placeholder="例如：HSK3_R_P1（同一组阅读题共享一篇文章）"
          >
            <template #prepend>
              <el-icon><Collection /></el-icon>
            </template>
          </el-input>
          <div style="font-size: 12px; color: #909399; margin-top: 4px;">
            用于标识共享同一材料的题目组，相同标识的题目会被归为一组
          </div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Plus, Close, Headset, Link, Check, InfoFilled, SuccessFilled, Picture, Collection, Reading, ZoomIn } from '@element-plus/icons-vue'
import { apiService } from '../api/index.js'

const route = useRoute()
const router = useRouter()

const examSetId = ref(null)
const examSetTitle = ref('')
const examSetLevel = ref(1)
const examSetData = ref({})
const loading = ref(false)
const submitting = ref(false)
const savingAudio = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref('add')
const formRef = ref(null)
const listeningAudioUrl = ref('')
const listeningAudioDuration = ref(0)

const questions = ref([])
const currentSection = ref('all')
const currentPage = ref(1)
const pageSize = ref(10)

const formData = reactive({
  id: null,
  type: 'single',
  section_type: 'listening',
  part_number: 1,
  question_number: 1,
  content: '',
  answer: '',
  options_list: ['', '', '', ''],
  option_type: 'text', // 'text' | 'image'
  explanation: '',
  difficulty: 3,
  audio_url: '',
  image_url: '',
  material_group: ''
})

const formRules = {
  section_type: [{ required: true, message: '请选择部分类型', trigger: 'change' }],
  type: [{ required: true, message: '请选择题目类型', trigger: 'change' }],
  part_number: [{ required: true, message: '请输入Part编号', trigger: 'blur' }],
  question_number: [{ required: true, message: '请输入题号', trigger: 'blur' }],
  content: [{ required: true, message: '请输入题目内容', trigger: 'blur' }],
  answer: [{ required: true, message: '请输入正确答案', trigger: 'blur' }]
}

const filteredQuestions = computed(() => {
  if (currentSection.value === 'all') {
    return questions.value
  }
  // 如果题目的section_type为null，根据type推断所属section
  return questions.value.filter(q => {
    if (q.section_type === currentSection.value) {
      return true
    }
    // 兼容旧数据：section_type为null时，根据type推断
    if (!q.section_type || q.section_type === null) {
      if (currentSection.value === 'listening' && q.type === 'listening') {
        return true
      }
      if (currentSection.value === 'reading' && q.type === 'reading') {
        return true
      }
      if (currentSection.value === 'writing' && (q.type === 'writing' || q.type === 'fill_blank')) {
        return true
      }
    }
    return false
  })
})

const paginatedQuestions = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredQuestions.value.slice(start, end)
})

const loadExamSet = async () => {
  try {
    const response = await apiService.getExamSetDetail(examSetId.value)
    examSetData.value = response.data
    examSetTitle.value = response.data.title
    examSetLevel.value = response.data.level
    listeningAudioUrl.value = response.data.listening_audio_url || ''
    listeningAudioDuration.value = response.data.listening_audio_duration || 0
  } catch (error) {
    console.error('加载套卷信息失败:', error)
  }
}

const saveListeningAudio = async () => {
  if (!listeningAudioUrl.value) {
    ElMessage.warning('请输入听力音频URL')
    return
  }
  
  savingAudio.value = true
  try {
    await apiService.updateExamSet(examSetId.value, {
      listening_audio_url: listeningAudioUrl.value,
      listening_audio_duration: 0  // 时长由前端自动获取，这里设为0
    })
    ElMessage.success('听力音频设置已保存')
    loadExamSet()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    savingAudio.value = false
  }
}

const loadQuestions = async () => {
  loading.value = true
  try {
    console.log('正在加载套卷ID:', examSetId.value, '的题目')
    
    // 添加page_size参数，确保获取所有题目
    const response = await apiService.getQuestions({ 
      question_set: examSetId.value,
      page_size: 1000  // 设置足够大的值以获取所有题目
    })
    
    console.log('API响应:', response.data)
    
    if (response.data.results) {
      questions.value = response.data.results
    } else if (Array.isArray(response.data)) {
      questions.value = response.data
    }
    
    console.log('加载的题目:', questions.value.map(q => ({ id: q.id, section: q.section_type, type: q.type })))
    
    questions.value.sort((a, b) => {
      if (a.section_type !== b.section_type) {
        const order = { listening: 1, reading: 2, writing: 3, null: 4 }
        const aOrder = order[a.section_type] !== undefined ? order[a.section_type] : 99
        const bOrder = order[b.section_type] !== undefined ? order[b.section_type] : 99
        return aOrder - bOrder
      }
      if (a.part_number !== b.part_number) {
        return (a.part_number || 0) - (b.part_number || 0)
      }
      return (a.question_number || 0) - (b.question_number || 0)
    })
    
    console.log(`成功加载 ${questions.value.length} 道题目`)
  } catch (error) {
    console.error('加载题目失败:', error)
    ElMessage.error('加载题目失败: ' + (error.message || ''))
  } finally {
    loading.value = false
  }
}

const filterQuestions = () => {
  currentPage.value = 1
}

const showAddDialog = () => {
  dialogMode.value = 'add'
  Object.assign(formData, {
    id: null,
    type: 'single',
    section_type: currentSection.value !== 'all' ? currentSection.value : 'listening',
    part_number: 1,
    question_number: questions.value.length + 1,
    content: '',
    answer: '',
    options_list: ['', '', '', ''],
    option_type: 'text',
    explanation: '',
    difficulty: 3,
    audio_url: '',
    image_url: '',
    material_group: ''
  })
  dialogVisible.value = true
}

const editQuestion = (row) => {
  dialogMode.value = 'edit'
  
  let optionsList = ['', '', '', '']
  if (row.options) {
    try {
      const parsed = JSON.parse(row.options)
      if (Array.isArray(parsed)) {
        optionsList = parsed
      }
    } catch (e) {
      console.error('解析选项失败:', e)
    }
  }
  
  Object.assign(formData, {
    id: row.id,
    type: row.type,
    section_type: row.section_type || 'listening',
    part_number: row.part_number || 1,
    question_number: row.question_number || 1,
    content: row.content,
    answer: row.answer,
    options_list: optionsList,
    option_type: row.option_type || 'text',
    explanation: row.explanation || '',
    difficulty: row.difficulty || 3,
    audio_url: row.audio_url || '',
    image_url: row.image_url || '',
    material_group: row.material_group || ''
  })
  
  dialogVisible.value = true
}

const addOption = () => {
  formData.options_list.push('')
}

const removeOption = (index) => {
  if (formData.options_list.length > 2) {
    formData.options_list.splice(index, 1)
  } else {
    ElMessage.warning('至少保留2个选项')
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    const options = ['single', 'multiple', 'reading'].includes(formData.type)
      ? JSON.stringify(formData.options_list.filter(opt => opt.trim() !== ''))
      : ''
    
    const data = {
      type: formData.type,
      level: examSetLevel.value,
      content: formData.content,
      answer: formData.answer,
      options: options,
      option_type: formData.option_type,
      explanation: formData.explanation,
      question_set: examSetId.value,
      section_type: formData.section_type,
      part_number: formData.part_number,
      question_number: formData.question_number,
      difficulty: formData.difficulty,
      // 如果是听力题且套卷有统一音频，则不保存单个题目的audio_url
      audio_url: (formData.section_type === 'listening' && examSetData.value.listening_audio_url) ? '' : formData.audio_url,
      image_url: formData.image_url,
      material_group: formData.material_group
    }
    
    if (dialogMode.value === 'add') {
      await apiService.createQuestion(data)
      ElMessage.success('添加成功')
    } else {
      await apiService.updateQuestion(formData.id, data)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    loadQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('提交失败:', error)
      ElMessage.error('操作失败')
    }
  } finally {
    submitting.value = false
  }
}

const deleteQuestion = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除这道题目吗？`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await apiService.deleteQuestion(row.id)
    ElMessage.success('删除成功')
    loadQuestions()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const goBack = () => {
  router.push('/mock-exam-questions')
}

const getSectionColor = (type) => {
  const colorMap = {
    'listening': 'primary',
    'reading': 'success',
    'writing': 'warning'
  }
  return colorMap[type] || 'info'
}

const getSectionLabel = (type) => {
  const labelMap = {
    'listening': '听力',
    'reading': '阅读',
    'writing': '书写'
  }
  return labelMap[type] || '未知'
}

const getTypeLabel = (type) => {
  const labelMap = {
    'single': '单选',
    'multiple': '多选',
    'judge': '判断',
    'fill': '填空',
    'reading': '阅读',
    'writing': '书写'
  }
  return labelMap[type] || '未知'
}

const handleImageError = (event) => {
  event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23f5f5f5" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23999"%3E加载失败%3C/text%3E%3C/svg%3E'
}

onMounted(() => {
  examSetId.value = route.params.id
  if (examSetId.value) {
    loadExamSet()
    loadQuestions()
  }
})
</script>

<style scoped>
.exam-set-questions-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-section h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.audio-settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

.audio-settings-content {
  padding: 10px 0;
}

.audio-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}

.current-audio {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}

.section-tabs-card {
  margin-bottom: 20px;
}

.stats-info {
  margin-top: 15px;
}

.table-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.options-editor {
  width: 100%;
}

.option-item-container {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.image-preview {
  flex-shrink: 0;
}

.preview-thumbnail {
  position: relative;
  width: 80px;
  height: 80px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  background: #f5f7fa;
}

.preview-thumbnail:hover {
  border-color: #409eff;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.preview-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
  font-size: 24px;
}

.preview-thumbnail:hover .preview-overlay {
  opacity: 1;
}

.preview-large {
  text-align: center;
}

:deep(.el-radio-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
</style>
