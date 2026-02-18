<template>
  <div class="listening-group-page">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon style="margin-right: 8px; vertical-align: middle;"><Headset /></el-icon>
            批量添加听力题组
          </h3>
          <el-button @click="$router.back()">
            <el-icon style="margin-right: 4px;"><ArrowLeft /></el-icon>
            返回
          </el-button>
        </div>
      </template>

      <!-- 音频材料区域 -->
      <el-form :model="formData" label-width="120px">
        <el-divider content-position="left">
          <el-icon><Headset /></el-icon>
          音频材料
        </el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="材料标题" required>
              <el-input 
                v-model="formData.material.title" 
                placeholder="例如：HSK1 听力 Part1"
              />
            </el-form-item>
          </el-col>
          
          <el-col :span="6">
            <el-form-item label="HSK等级" required>
              <el-select v-model="formData.material.level" placeholder="选择等级">
                <el-option v-for="i in 6" :key="i" :label="`HSK ${i}级`" :value="i" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="6">
            <el-form-item label="播放次数">
              <el-input-number v-model="formData.material.play_times" :min="1" :max="5" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="音频文件" required>
          <el-upload
            class="audio-uploader"
            :auto-upload="false"
            :show-file-list="true"
            :on-change="handleAudioChange"
            accept="audio/mp3,audio/wav"
            drag
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽音频文件到此处 或 <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 MP3/WAV 格式，建议文件大小不超过 50MB
              </div>
            </template>
          </el-upload>
          <div v-if="audioFileName" class="audio-preview-box">
            <div class="audio-file-info">
              <el-icon><Headset /></el-icon>
              <span>{{ audioFileName }}</span>
              <el-tag v-if="audioDuration > 0" type="success" size="small">
                <el-icon><Clock /></el-icon>
                {{ formatDuration(audioDuration) }}
              </el-tag>
            </div>
            <audio 
              v-if="audioPreviewUrl" 
              ref="audioPlayer"
              :src="audioPreviewUrl" 
              controls 
              class="audio-player"
            />
          </div>
        </el-form-item>

        <!-- 题目列表区域 -->
        <el-divider content-position="left">
          <el-icon><Document /></el-icon>
          题目列表 ({{ formData.questions.length }}道)
        </el-divider>

        <div class="questions-container">
          <el-card 
            v-for="(question, index) in formData.questions" 
            :key="index"
            class="question-card"
            shadow="hover"
          >
            <template #header>
              <div class="question-header">
                <span class="question-number">第 {{ index + 1 }} 题</span>
                <el-button 
                  type="danger" 
                  size="small" 
                  :icon="Delete"
                  @click="removeQuestion(index)"
                  v-if="formData.questions.length > 1"
                >
                  删除此题
                </el-button>
              </div>
            </template>

            <el-form-item label="题目内容">
              <el-input 
                v-model="question.content" 
                placeholder="输入题目内容或说明"
                type="textarea"
                :rows="2"
              />
            </el-form-item>

            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="题型">
                  <el-select v-model="question.type">
                    <el-option label="单选题" value="single" />
                    <el-option label="多选题" value="multiple" />
                    <el-option label="判断题" value="judge" />
                  </el-select>
                </el-form-item>
              </el-col>

              <el-col :span="8">
                <el-form-item label="选项类型">
                  <el-radio-group v-model="question.option_type" @change="handleOptionTypeChange(index)">
                    <el-radio value="text">文字</el-radio>
                    <el-radio value="image">图片</el-radio>
                    <el-radio value="mixed">混合</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>

              <el-col :span="8">
                <el-form-item label="难度">
                  <el-rate v-model="question.difficulty" :max="5" show-score />
                </el-form-item>
              </el-col>
            </el-row>

            <!-- 选项列表 -->
            <div class="options-container">
              <div 
                v-for="(option, optIndex) in question.options" 
                :key="optIndex"
                class="option-item"
              >
                <el-tag size="large" class="option-label">{{ option.label }}</el-tag>
                
                <!-- 文字选项 -->
                <el-input 
                  v-if="question.option_type === 'text'"
                  v-model="option.text"
                  placeholder="输入选项内容"
                  class="option-input"
                />

                <!-- 图片选项 -->
                <div v-else-if="question.option_type === 'image'" class="option-image-container">
                  <el-upload
                    class="option-image-uploader"
                    :auto-upload="false"
                    :show-file-list="false"
                    :on-change="(file) => handleOptionImageChange(file, index, optIndex)"
                    accept="image/*"
                  >
                    <img v-if="option.image" :src="option.image" class="option-image" />
                    <el-icon v-else class="option-image-icon"><Plus /></el-icon>
                  </el-upload>
                  <el-input 
                    v-model="option.text" 
                    placeholder="图片说明（可选）"
                    size="small"
                    class="image-description"
                  />
                </div>

                <!-- 混合选项 -->
                <div v-else-if="question.option_type === 'mixed'" class="option-mixed-container">
                  <el-upload
                    class="mixed-image-uploader"
                    :auto-upload="false"
                    :show-file-list="false"
                    :on-change="(file) => handleOptionImageChange(file, index, optIndex)"
                    accept="image/*"
                  >
                    <img v-if="option.image" :src="option.image" class="mixed-image" />
                    <el-icon v-else class="mixed-image-icon"><Plus /></el-icon>
                  </el-upload>
                  <el-input 
                    v-model="option.text" 
                    placeholder="输入文字说明"
                    type="textarea"
                    :rows="2"
                    class="mixed-text"
                  />
                </div>
              </div>
            </div>

            <el-form-item label="正确答案" style="margin-top: 20px;">
              <el-select v-model="question.answer" placeholder="选择正确答案">
                <el-option 
                  v-for="opt in question.options" 
                  :key="opt.value"
                  :label="opt.label" 
                  :value="opt.value" 
                />
              </el-select>
            </el-form-item>

            <el-form-item label="答案解析">
              <el-input 
                v-model="question.explanation" 
                placeholder="输入答案解析（选填）"
                type="textarea"
                :rows="2"
              />
            </el-form-item>
          </el-card>

          <el-button 
            type="primary" 
            :icon="Plus" 
            @click="addQuestion"
            class="add-question-btn"
            plain
          >
            添加新题目
          </el-button>
        </div>

        <!-- 操作按钮 -->
        <el-form-item style="margin-top: 30px;">
          <el-button @click="$router.back()">取消</el-button>
          <el-button type="primary" @click="saveListeningGroup" :loading="saving">
            保存题组
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Headset, Document, Plus, Delete, UploadFilled, ArrowLeft
} from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'ListeningGroupPage',
  components: {
    Headset,
    Document,
    Plus,
    Delete,
    UploadFilled,
    ArrowLeft
  },
  setup() {
    const router = useRouter()
    const saving = ref(false)
    const audioFileName = ref('')
    const audioPreviewUrl = ref('')
    const audioUploading = ref(false)
    const audioDuration = ref(0)
    const audioPlayer = ref(null)
    
    // 确保axios使用正确的baseURL
    if (!axios.defaults.baseURL) {
      axios.defaults.baseURL = '/api'
      console.log('已设置axios.defaults.baseURL = /api')
    }

    const formData = reactive({
      material: {
        title: '',
        level: 1,
        play_times: 2,
        part_number: 1,
        duration: 0,
        audio_file: null
      },
      questions: [
        createNewQuestion()
      ]
    })

    function createNewQuestion() {
      return {
        content: '',
        type: 'single',
        option_type: 'text',
        difficulty: 2,
        answer: '',
        explanation: '',
        options: [
          { label: 'A', value: 'A', text: '', image: '' },
          { label: 'B', value: 'B', text: '', image: '' },
          { label: 'C', value: 'C', text: '', image: '' },
          { label: 'D', value: 'D', text: '', image: '' }
        ]
      }
    }

    function addQuestion() {
      formData.questions.push(createNewQuestion())
      ElMessage.success('已添加新题目')
    }

    function removeQuestion(index) {
      formData.questions.splice(index, 1)
      ElMessage.success('已删除题目')
    }

    function handleAudioChange(file) {
      const reader = new FileReader()
      audioUploading.value = true
      
      reader.onload = (e) => {
        formData.material.audio_file = e.target.result
        audioFileName.value = file.name
        audioPreviewUrl.value = e.target.result
        
        // 自动获取音频时长
        const audio = new Audio(e.target.result)
        audio.addEventListener('loadedmetadata', () => {
          audioDuration.value = Math.round(audio.duration)
          formData.material.duration = audioDuration.value
          audioUploading.value = false
          ElMessage.success(`音频上传成功，时长：${formatDuration(audioDuration.value)}`)
        })
        
        audio.addEventListener('error', () => {
          audioUploading.value = false
          ElMessage.error('音频加载失败，请检查文件格式')
        })
      }
      
      reader.onerror = () => {
        audioUploading.value = false
        ElMessage.error('音频文件读取失败')
      }
      
      reader.readAsDataURL(file.raw)
    }
    
    function formatDuration(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return mins > 0 ? `${mins}分${secs}秒` : `${secs}秒`
    }

    function handleOptionImageChange(file, questionIndex, optionIndex) {
      const reader = new FileReader()
      reader.onload = (e) => {
        formData.questions[questionIndex].options[optionIndex].image = e.target.result
      }
      reader.readAsDataURL(file.raw)
    }

    function handleOptionTypeChange(questionIndex) {
      // 当选项类型改变时，重置选项数据
      const question = formData.questions[questionIndex]
      question.options.forEach(opt => {
        opt.text = ''
        opt.image = ''
      })
    }

    async function saveListeningGroup() {
      // 验证必填字段
      if (!formData.material.title) {
        ElMessage.error('请输入材料标题')
        return
      }
      if (!formData.material.audio_file) {
        ElMessage.error('请上传音频文件')
        return
      }
      if (formData.questions.length === 0) {
        ElMessage.error('请至少添加一道题目')
        return
      }

      // 验证每道题目
      for (let i = 0; i < formData.questions.length; i++) {
        const q = formData.questions[i]
        if (!q.content.trim()) {
          ElMessage.error(`第 ${i + 1} 题的内容不能为空`)
          return
        }
        if (!q.answer) {
          ElMessage.error(`第 ${i + 1} 题请选择正确答案`)
          return
        }
        // 检查选项是否填写
        const hasEmptyOption = q.options.some(opt => {
          if (q.option_type === 'text') {
            return !opt.text.trim()
          } else if (q.option_type === 'image') {
            return !opt.image
          } else if (q.option_type === 'mixed') {
            return !opt.image || !opt.text.trim()
          }
          return false
        })
        if (hasEmptyOption) {
          ElMessage.error(`第 ${i + 1} 题的选项未填写完整`)
          return
        }
      }

      saving.value = true

      try {
        console.log('正在提交题组数据...', formData)
        const response = await axios.post('/question/listening-group/', formData)
        
        if (response.data.success) {
          ElMessage.success(response.data.message)
          router.push('/questions')
        } else {
          ElMessage.error(response.data.error || '保存失败')
        }
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败：' + (error.response?.data?.error || error.message))
      } finally {
        saving.value = false
      }
    }

    return {
      formData,
      saving,
      audioFileName,
      audioPreviewUrl,
      addQuestion,
      removeQuestion,
      handleAudioChange,
      handleOptionImageChange,
      handleOptionTypeChange,
      saveListeningGroup,
      formatDuration,
      audioUploading,
      audioDuration,
      audioPlayer,
      Delete,
      Plus
    }
  }
}
</script>

<style scoped>
.listening-group-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 20px;
}

.audio-uploader {
  width: 100%;
}

.audio-preview-box {
  margin-top: 15px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
  border: 1px solid #e4e7ed;
}

.audio-file-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 14px;
  color: #606266;
}

.audio-file-info span {
  flex: 1;
}

.audio-player {
  width: 100%;
  max-width: 500px;
}

.questions-container {
  margin-top: 20px;
}

.question-card {
  margin-bottom: 20px;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.question-number {
  font-weight: bold;
  font-size: 16px;
  color: #409eff;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 15px;
}

.option-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.option-label {
  flex-shrink: 0;
  height: 32px;
  line-height: 32px;
  min-width: 40px;
  text-align: center;
}

.option-input {
  flex: 1;
}

/* 图片选项样式 */
.option-image-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.option-image-uploader {
  width: 120px;
  height: 120px;
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
}

.option-image-uploader:hover {
  border-color: #409eff;
}

.option-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.option-image-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-description {
  width: 100%;
}

/* 混合选项样式（图片在上，文字在下）*/
.option-mixed-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.mixed-image-uploader {
  width: 180px;
  height: 120px;
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
  align-self: center;
}

.mixed-image-uploader:hover {
  border-color: #409eff;
}

.mixed-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mixed-image-icon {
  font-size: 28px;
  color: #8c939d;
  width: 180px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mixed-text {
  width: 100%;
}

.add-question-btn {
  width: 100%;
  height: 60px;
  font-size: 16px;
  border-style: dashed;
}
</style>
