<template>
  <div class="edit-page">
    <div class="page-header">
      <el-button @click="goBack" :icon="ArrowLeft">返回</el-button>
      <h2>编辑听力题组</h2>
    </div>
    
    <div class="edit-container" v-loading="loading">
      <el-form 
        ref="formRef" 
        :model="formData" 
        label-width="120px"
        :rules="rules"
      >
        <!-- 音频材料信息 -->
        <el-card class="section-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>📝 音频材料信息</span>
            </div>
          </template>
          
          <el-form-item label="材料标题" prop="title">
            <el-input v-model="formData.title" placeholder="例如：HSK1听力第四部分第11-15题对话" />
          </el-form-item>
          
          <el-form-item label="HSK等级" prop="level">
            <el-select v-model="formData.level" placeholder="请选择">
              <el-option :label="`HSK ${i}级`" :value="i" v-for="i in 6" :key="i" />
            </el-select>
          </el-form-item>
          
          <el-form-item label="播放次数" prop="play_times">
            <el-input-number v-model="formData.play_times" :min="1" :max="3" />
            <span style="margin-left: 10px; color: #909399;">听力考试时音频播放次数</span>
          </el-form-item>
          
          <el-form-item label="音频文件">
            <div class="audio-upload-box">
              <div class="upload-actions">
                <el-upload
                  class="audio-uploader"
                  :show-file-list="false"
                  :before-upload="handleAudioUpload"
                  accept="audio/*"
                  :disabled="audioUploading"
                >
                  <el-button :icon="Upload" :loading="audioUploading" type="primary" plain>
                    {{ audioUploading ? '上传中...' : '更换音频（可选）' }}
                  </el-button>
                </el-upload>
                <span v-if="formData.audio_url" class="audio-status">
                  <el-icon color="#67c23a"><CircleCheck /></el-icon>
                  原音频已保存
                </span>
              </div>
              
              <!-- 音频预览 -->
              <div v-if="formData.audio_url" class="audio-preview">
                <audio 
                  ref="audioPlayer"
                  :src="formData.audio_url" 
                  controls 
                  style="width: 100%;"
                  @loadedmetadata="onAudioLoaded"
                  crossorigin="anonymous"
                >
                  您的浏览器不支持音频播放
                </audio>
                <p class="audio-info">
                  <el-icon><Clock /></el-icon>
                  音频时长: {{ audioDuration > 0 ? formatDuration(audioDuration) : formatDuration(formData.audio_duration) }}
                </p>
              </div>
              
              <el-alert 
                title="💡 原音频已保存，如不需要更换请直接编辑题目后保存" 
                type="info" 
                :closable="false"
                show-icon
                style="margin-top: 10px;"
              />
            </div>
          </el-form-item>
        </el-card>
        
        <!-- 题目列表 -->
        <el-card class="section-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span>📋 题目列表 (共{{ formData.questions.length }}题)</span>
            </div>
          </template>
          
          <div class="questions-list">
            <el-collapse v-model="activeQuestions" accordion>
              <el-collapse-item 
                v-for="(question, qIndex) in formData.questions" 
                :key="qIndex"
                :name="String(qIndex)"
              >
                <template #title>
                  <div class="question-title">
                    <span class="question-number">第{{ qIndex + 1 }}题</span>
                    <el-tag size="small">{{ getTypeLabel(question.type) }}</el-tag>
                    <span class="question-preview">{{ question.content }}</span>
                  </div>
                </template>
                
                <el-form-item :label="`题目内容`">
                  <el-input 
                    v-model="question.content" 
                    type="textarea" 
                    :rows="2"
                    placeholder="请输入题目内容"
                  />
                </el-form-item>
                
                <el-form-item label="题目类型">
                  <el-select v-model="question.type" placeholder="请选择">
                    <el-option label="单选题" value="single" />
                    <el-option label="判断题" value="judge" />
                  </el-select>
                </el-form-item>
                
                <el-form-item label="难度">
                  <el-rate v-model="question.difficulty" :max="5" show-score />
                </el-form-item>
                
                <el-form-item label="选项类型">
                  <el-radio-group v-model="question.option_type">
                    <el-radio value="text">纯文字</el-radio>
                    <el-radio value="image">纯图片</el-radio>
                    <el-radio value="mixed">图文混合</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="选项">
                  <div class="options-editor">
                    <div 
                      v-for="(opt, optIndex) in question.options" 
                      :key="optIndex"
                      class="option-edit-card"
                    >
                      <div class="option-header">
                        <span class="option-label">{{ String.fromCharCode(65 + optIndex) }}</span>
                        <el-button 
                          type="danger" 
                          :icon="Delete" 
                          circle 
                          size="small"
                          @click="removeOption(qIndex, optIndex)"
                        />
                      </div>
                      
                      <!-- 纯文字选项 -->
                      <div v-if="question.option_type === 'text'">
                        <el-input 
                          v-model="opt.text" 
                          placeholder="请输入选项文字"
                        />
                      </div>
                      
                      <!-- 纯图片选项 -->
                      <div v-else-if="question.option_type === 'image'">
                        <el-upload
                          class="image-uploader"
                          :show-file-list="false"
                          :before-upload="(file) => handleImageUpload(file, qIndex, optIndex)"
                          accept="image/*"
                        >
                          <img v-if="opt.image" :src="opt.image" class="option-image" />
                          <el-icon v-else class="uploader-icon"><Plus /></el-icon>
                        </el-upload>
                      </div>
                      
                      <!-- 图文混合选项 -->
                      <div v-else-if="question.option_type === 'mixed'" class="mixed-option">
                        <el-upload
                          class="image-uploader small"
                          :show-file-list="false"
                          :before-upload="(file) => handleImageUpload(file, qIndex, optIndex)"
                          accept="image/*"
                        >
                          <img v-if="opt.image" :src="opt.image" class="option-image-small" />
                          <el-icon v-else class="uploader-icon-small"><Plus /></el-icon>
                        </el-upload>
                        <el-input 
                          v-model="opt.text" 
                          placeholder="请输入选项文字"
                          style="flex: 1;"
                        />
                      </div>
                    </div>
                    
                    <el-button 
                      type="primary" 
                      :icon="Plus" 
                      @click="addOption(qIndex)"
                      style="width: 100%; margin-top: 10px;"
                    >
                      添加选项
                    </el-button>
                  </div>
                </el-form-item>
                
                <el-form-item label="正确答案">
                  <el-select v-model="question.answer" placeholder="请选择">
                    <el-option 
                      v-for="(opt, idx) in question.options" 
                      :key="idx"
                      :label="String.fromCharCode(65 + idx)"
                      :value="String.fromCharCode(65 + idx)"
                    />
                  </el-select>
                </el-form-item>
                
                <el-form-item label="答案解析">
                  <el-input 
                    v-model="question.explanation" 
                    type="textarea" 
                    :rows="3"
                    placeholder="请输入答案解析（可选）"
                  />
                </el-form-item>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>
        
        <!-- 操作按钮 -->
        <div class="form-actions">
          <el-button @click="goBack">取消</el-button>
          <el-button type="primary" @click="saveGroup" :loading="saving">
            <el-icon><Select /></el-icon>
            保存修改
          </el-button>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  ArrowLeft, Upload, Clock, Plus, Delete, Select, CircleCheck 
} from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const saving = ref(false)
const audioUploading = ref(false)
const audioDuration = ref(0)
const audioPlayer = ref(null)
const activeQuestions = ref('0')

const formData = reactive({
  material_group: '',
  title: '',
  level: 1,
  play_times: 2,
  audio_url: '',
  audio_duration: 0,
  questions: []
})

const rules = {
  title: [{ required: true, message: '请输入材料标题', trigger: 'blur' }]
}

// 加载题组数据
const loadGroupData = async () => {
  const materialGroup = route.params.id
  if (!materialGroup) {
    ElMessage.error('缺少题组ID')
    goBack()
    return
  }
  
  loading.value = true
  try {
    // 设置axios baseURL
    if (!axios.defaults.baseURL) {
      axios.defaults.baseURL = '/api'
    }
    
    console.log('加载题组数据:', materialGroup)
    const response = await axios.get(`/question/listening-group/${materialGroup}/`)
    const data = response.data
    console.log('题组数据:', data)
    
    formData.material_group = materialGroup
    formData.title = data.material.title
    formData.level = data.material.level
    formData.play_times = data.material.play_times
    formData.audio_url = data.material.audio_url
    formData.audio_duration = data.material.audio_duration || 0
    
    // 关键修复：保存原音频URL和时长
    if (data.material.audio_url) {
      audioDuration.value = data.material.audio_duration || 0
      console.log('原音频URL:', formData.audio_url, '时长:', audioDuration.value)
    }
    
    // 解析题目数据
    formData.questions = data.questions.map(q => {
      let parsedOptions = []
      let optionType = 'text'
      
      try {
        const opts = JSON.parse(q.options)
        if (opts.option_type) {
          optionType = opts.option_type
          parsedOptions = opts.options || []
        } else if (Array.isArray(opts)) {
          parsedOptions = opts.map((opt, idx) => ({
            label: String.fromCharCode(65 + idx),
            text: typeof opt === 'string' ? opt : opt.text || opt.label,
            value: String.fromCharCode(65 + idx)
          }))
        }
      } catch (e) {
        console.error('解析选项失败:', e)
      }
      
      return {
        id: q.id,
        content: q.content,
        type: q.type || 'single',
        difficulty: q.difficulty || 2,
        option_type: optionType,
        options: parsedOptions,
        answer: q.answer,
        explanation: q.explanation || ''
      }
    })
    
    ElMessage.success('题组数据加载成功')
    
  } catch (error) {
    console.error('加载题组失败:', error)
    ElMessage.error('加载题组数据失败: ' + (error.response?.data?.error || error.message))
  } finally {
    loading.value = false
  }
}

// 音频上传（可选，用于更换音频）
const handleAudioUpload = (file) => {
  const reader = new FileReader()
  audioUploading.value = true
  
  reader.onload = (e) => {
    formData.audio_url = e.target.result
    
    // 自动获取新音频时长
    const audio = new Audio(e.target.result)
    audio.addEventListener('loadedmetadata', () => {
      audioDuration.value = Math.round(audio.duration)
      formData.audio_duration = audioDuration.value
      audioUploading.value = false
      ElMessage.success(`音频更换成功，时长：${formatDuration(audioDuration.value)}`)
    })
    
    audio.addEventListener('error', () => {
      audioUploading.value = false
      ElMessage.error('音频加载失败')
    })
  }
  
  reader.onerror = () => {
    audioUploading.value = false
    ElMessage.error('音频文件读取失败')
  }
  
  reader.readAsDataURL(file)
  return false // 阻止自动上传
}

// 音频加载完成，自动获取时长
const onAudioLoaded = () => {
  if (audioPlayer.value && audioDuration.value === 0) {
    audioDuration.value = Math.round(audioPlayer.value.duration)
  }
}

// 图片上传
const handleImageUpload = (file, qIndex, optIndex) => {
  const reader = new FileReader()
  
  reader.onload = (e) => {
    formData.questions[qIndex].options[optIndex].image = e.target.result
    ElMessage.success('图片上传成功')
  }
  
  reader.onerror = () => {
    ElMessage.error('图片上传失败')
  }
  
  reader.readAsDataURL(file)
  return false
}

// 添加选项
const addOption = (qIndex) => {
  const question = formData.questions[qIndex]
  const newLabel = String.fromCharCode(65 + question.options.length)
  
  question.options.push({
    label: newLabel,
    text: '',
    value: newLabel,
    image: ''
  })
}

// 删除选项
const removeOption = (qIndex, optIndex) => {
  if (formData.questions[qIndex].options.length <= 2) {
    ElMessage.warning('至少保留2个选项')
    return
  }
  formData.questions[qIndex].options.splice(optIndex, 1)
}

// 保存题组
const saveGroup = async () => {
  if (!formData.audio_url) {
    ElMessage.warning('音频文件丢失，请重新上传')
    return
  }
  
  if (formData.questions.length === 0) {
    ElMessage.warning('至少添加一道题目')
    return
  }
  
  // 验证所有题目都有答案
  for (let i = 0; i < formData.questions.length; i++) {
    const q = formData.questions[i]
    if (!q.answer) {
      ElMessage.warning(`第${i+1}题缺少正确答案`)
      return
    }
  }
  
  saving.value = true
  try {
    const payload = {
      material: {
        title: formData.title,
        level: formData.level,
        play_times: formData.play_times,
        audio_url: formData.audio_url,  // 保留原音频URL或使用新上传的
        audio_duration: audioDuration.value || formData.audio_duration
      },
      questions: formData.questions.map((q, idx) => ({
        id: q.id || null,  // 包含题目ID用于更新
        content: q.content,
        type: q.type,
        difficulty: q.difficulty,
        answer: q.answer,
        explanation: q.explanation,
        question_number: idx + 1,
        options: {
          option_type: q.option_type,
          options: q.options
        }
      }))
    }
    
    console.log('提交更新数据:', payload)
    
    await axios.put(`/question/listening-group/${formData.material_group}/`, payload)
    
    ElMessage.success('保存成功！')
    setTimeout(() => {
      goBack()
    }, 1000)
    
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败: ' + (error.response?.data?.error || error.message))
  } finally {
    saving.value = false
  }
}

const formatDuration = (seconds) => {
  if (!seconds) return '0秒'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return mins > 0 ? `${mins}分${secs}秒` : `${secs}秒`
}

const getTypeLabel = (type) => {
  const labels = { 'single': '单选题', 'judge': '判断题', 'multiple': '多选题' }
  return labels[type] || '单选题'
}

const goBack = () => {
  router.push('/listening-groups')
}

onMounted(() => {
  loadGroupData()
})
</script>

<style scoped>
.edit-page {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 64px);
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.edit-container {
  max-width: 1000px;
  margin: 0 auto;
}

.section-card {
  margin-bottom: 20px;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.audio-upload-box {
  width: 100%;
}

.upload-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.audio-status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #67c23a;
  font-size: 14px;
  font-weight: 500;
}

.audio-preview {
  margin-top: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.audio-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
  margin-top: 12px;
  margin-bottom: 0;
}

.questions-list {
  margin-top: 16px;
}

.question-title {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.question-number {
  font-weight: 600;
  color: #409eff;
}

.question-preview {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #606266;
}

.options-editor {
  width: 100%;
}

.option-edit-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 12px;
  background: #fafafa;
}

.option-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.option-label {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.image-uploader {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.image-uploader:hover {
  border-color: #409eff;
}

.option-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
  display: block;
}

.uploader-icon {
  font-size: 40px;
  color: #8c939d;
  width: 200px;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mixed-option {
  display: flex;
  gap: 12px;
  align-items: center;
}

.image-uploader.small {
  width: 100px;
  height: 80px;
}

.option-image-small {
  width: 100px;
  height: 80px;
  object-fit: cover;
}

.uploader-icon-small {
  font-size: 24px;
  color: #8c939d;
  width: 100px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
  padding: 20px 0;
}
</style>
