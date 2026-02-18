<template>
  <div class="question-page">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h3>题目管理</h3>
          <div class="header-actions">
            <el-button type="success" @click="refreshQuestions" :icon="Refresh">刷新</el-button>
            <el-button type="warning" @click="$router.push('/listening-groups')">
              <el-icon><Headset /></el-icon>
              听力题组管理
            </el-button>
            <el-button type="primary" @click="showAddDialog" :icon="Plus">新增题目</el-button>
          </div>
        </div>
      </template>
      
      <!-- 搜索过滤区域 -->
      <div class="filter-container">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索题目内容"
          class="search-input"
          :prefix-icon="Search"
          clearable
          @input="handleSearch"
        ></el-input>
        
        <el-select v-model="typeFilter" placeholder="题目类型" clearable @change="handleSearch">
          <el-option label="全部" value=""></el-option>
          <el-option 
            v-for="type in questionTypes" 
            :key="type" 
            :label="type" 
            :value="type"
          ></el-option>
        </el-select>
        
        <el-select v-model="levelFilter" placeholder="HSK等级" clearable @change="handleSearch">
          <el-option label="全部" value=""></el-option>
          <el-option label="HSK 1级" :value="1"></el-option>
          <el-option label="HSK 2级" :value="2"></el-option>
          <el-option label="HSK 3级" :value="3"></el-option>
          <el-option label="HSK 4级" :value="4"></el-option>
          <el-option label="HSK 5级" :value="5"></el-option>
          <el-option label="HSK 6级" :value="6"></el-option>
        </el-select>
        
        <el-select v-model="difficultyFilter" placeholder="难度系数" clearable @change="handleSearch">
          <el-option label="全部" value=""></el-option>
          <el-option label="⭐ 简单" :value="1"></el-option>
          <el-option label="⭐⭐ 较易" :value="2"></el-option>
          <el-option label="⭐⭐⭐ 中等" :value="3"></el-option>
          <el-option label="⭐⭐⭐⭐ 较难" :value="4"></el-option>
          <el-option label="⭐⭐⭐⭐⭐ 困难" :value="5"></el-option>
        </el-select>
      </div>
      
      <!-- 调试信息 -->
      <el-alert 
        v-if="questions.length > 0 && filteredQuestions.length === 0"
        type="warning" 
        title="筛选器过滤提示" 
        :closable="false"
        style="margin-bottom: 15px;"
      >
        <template #default>
          <p>当前有 <strong>{{ questions.length }}</strong> 道题目，但筛选器过滤后为 <strong>0</strong> 道</p>
          <p>当前筛选条件：</p>
          <ul>
            <li v-if="searchKeyword">搜索关键词：{{ searchKeyword }}</li>
            <li v-if="typeFilter">题目类型：{{ typeFilter }}</li>
            <li v-if="levelFilter">HSK等级：{{ levelFilter }}级</li>
            <li v-if="difficultyFilter">难度系数：{{ difficultyFilter }}星</li>
          </ul>
          <el-button type="primary" size="small" @click="clearAllFilters" style="margin-top: 10px;">清空所有筛选器</el-button>
        </template>
      </el-alert>
      
      <!-- 表格区域 -->
      <el-table
        :data="paginatedQuestions"
        style="width: 100%"
        v-loading="loading"
        border
        stripe
        highlight-current-row
      >
        <el-table-column prop="id" label="ID" width="80" sortable></el-table-column>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getTagType(row.type)">{{ row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="题目内容" min-width="250">
          <template #default="{ row }">
            <el-tooltip :content="row.content" placement="top" :disabled="row.content.length < 30">
              <div>{{ row.content.length > 30 ? row.content.substring(0, 30) + '...' : row.content }}</div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="level" label="HSK等级" width="100">
          <template #default="{ row }">
            <el-tag type="success">HSK {{ row.level }}级</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="difficulty" label="难度" width="120">
          <template #default="{ row }">
            <el-rate
              v-model="row.difficulty"
              :max="5"
              disabled
              show-score
              text-color="#ff9900"
              size="small"
            ></el-rate>
          </template>
        </el-table-column>
        <el-table-column prop="answer" label="答案" min-width="150">
          <template #default="{ row }">
            <el-tooltip :content="row.answer" placement="top" :disabled="row.answer.length < 20">
              <div>{{ row.answer.length > 20 ? row.answer.substring(0, 20) + '...' : row.answer }}</div>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column prop="options" label="选项" min-width="200">
          <template #default="{ row }">
            <el-popover placement="right" trigger="hover" width="300">
              <template #reference>
                <el-button link type="primary">查看选项</el-button>
              </template>
              <div v-if="row.options && row.options.length > 0">
                <template v-if="parseOptionsForDisplay(row.options).length > 0">
                  <p v-for="(option, index) in parseOptionsForDisplay(row.options)" :key="index">
                    {{ ['A', 'B', 'C', 'D'][index] || index }}: {{ option }}
                  </p>
                </template>
                <div v-else>选项格式错误</div>
              </div>
              <div v-else>无选项</div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" @click="editQuestion(scope.row)" :icon="Edit">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteQuestion(scope.row.id)" :icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页器 -->
      <div class="pagination-container">
        <el-pagination
          v-if="filteredQuestions.length > 0"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="filteredQuestions.length"
          layout="total, sizes, prev, pager, next, jumper"
          :page-sizes="[10, 20, 50, 100]"
          @current-change="handleCurrentChange"
          @size-change="handleSizeChange"
          background
        ></el-pagination>
      </div>
    </el-card>
    
    <!-- 题目编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingQuestion.id ? '编辑题目' : '新增题目'"
      width="700px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form
        :model="editingQuestion"
        :rules="formRules"
        ref="questionFormRef"
        label-width="100px"
        status-icon
      >
        <el-form-item label="题目类型" prop="type">
          <el-select v-model="editingQuestion.type" placeholder="请选择题目类型" style="width: 100%" @change="handleTypeChange">
            <el-option 
              v-for="type in questionTypes" 
              :key="type" 
              :label="typeLabels[type] || type" 
              :value="type"
            ></el-option>
          </el-select>
          <div style="margin-top: 8px; padding: 8px; background: #f0f9ff; border-radius: 4px; font-size: 12px; color: #1890ff;">
            <strong>当前题型说明：</strong>{{ getTypeDescription(editingQuestion.type) }}
          </div>
        </el-form-item>
        
        <!-- 图片相关字段（图片题） -->
        <template v-if="['image_choice', 'image_description'].includes(editingQuestion.type)">
          <el-form-item label="图片URL" prop="image_url">
            <el-input
              v-model="editingQuestion.image_url"
              placeholder="例如：http://localhost:8000/media/images/apple.jpg"
              maxlength="500"
            >
              <template #prepend>🖼️</template>
            </el-input>
            <div style="margin-top: 5px; font-size: 12px; color: #909399;">
              提示：请将图片文件放到 backend/media/images/ 目录，然后填写完整URL
            </div>
          </el-form-item>
          
          <!-- 图片预览 -->
          <el-form-item label="图片预览" v-if="editingQuestion.image_url">
            <img :src="editingQuestion.image_url" alt="题目图片" style="max-width: 300px; max-height: 200px; border: 1px solid #ddd; border-radius: 4px;" />
          </el-form-item>
        </template>
        
        <!-- 文章/对话内容（阅读理解、对话题） -->
        <template v-if="['passage_reading', 'dialogue', 'cloze'].includes(editingQuestion.type)">
          <el-form-item label="文章/对话内容" prop="passage">
            <el-input
              v-model="editingQuestion.passage"
              type="textarea"
              placeholder="请输入完整的文章或对话内容"
              :rows="6"
              maxlength="5000"
              show-word-limit
            ></el-input>
          </el-form-item>
          
          <el-form-item label="文章标题" prop="passage_title">
            <el-input
              v-model="editingQuestion.passage_title"
              placeholder="请输入文章标题（可选）"
              maxlength="200"
            ></el-input>
          </el-form-item>
        </template>
        
        <el-form-item label="题目内容" prop="content">
          <el-input
            v-model="editingQuestion.content"
            type="textarea"
            placeholder="请输入题目内容"
            :rows="4"
            maxlength="1000"
            show-word-limit
          ></el-input>
        </el-form-item>
        
        <el-form-item label="HSK等级" prop="level">
          <el-select v-model="editingQuestion.level" placeholder="请选择HSK等级" style="width: 100%">
            <el-option label="HSK 1级" :value="1"></el-option>
            <el-option label="HSK 2级" :value="2"></el-option>
            <el-option label="HSK 3级" :value="3"></el-option>
            <el-option label="HSK 4级" :value="4"></el-option>
            <el-option label="HSK 5级" :value="5"></el-option>
            <el-option label="HSK 6级" :value="6"></el-option>
          </el-select>
          <div style="margin-top: 4px; font-size: 12px; color: #909399;">
            选择题目所属的HSK等级（1-6级）
          </div>
        </el-form-item>
        
        <el-form-item label="难度系数" prop="difficulty">
          <div class="difficulty-selector">
            <el-rate
              v-model="editingQuestion.difficulty"
              :max="5"
              show-score
              text-color="#ff9900"
            ></el-rate>
            <span class="difficulty-text">{{ getDifficultyText(editingQuestion.difficulty) }}</span>
          </div>
          <div style="margin-top: 4px; font-size: 12px; color: #909399;">
            题目的难度系数（1星=简单，5星=困难）
          </div>
        </el-form-item>
        
        <el-form-item label="选项类型" v-if="['single', 'multiple', 'reading'].includes(editingQuestion.type)">
          <el-radio-group v-model="editingQuestion.option_type">
            <el-radio value="text">
              📝 文字选项
            </el-radio>
            <el-radio value="image">
              🖼️ 图片选项
            </el-radio>
          </el-radio-group>
          <div style="font-size: 12px; color: #909399; margin-top: 4px;">
            <span v-if="editingQuestion.option_type === 'text'">选项内容为文字（如：A. 苹果 B. 香蕉）</span>
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

        <el-form-item label="选项" prop="options" v-if="['single', 'multiple', 'reading'].includes(editingQuestion.type)">
          <div class="options-container">
            <div v-for="(option, index) in parsedOptions" :key="index" class="option-item">
              <div style="display: flex; align-items: flex-start; gap: 10px; width: 100%;">
                <span class="option-label">{{ ['A', 'B', 'C', 'D'][index] || index }}:</span>
                <el-input 
                  v-model="parsedOptions[index]" 
                  :placeholder="editingQuestion.option_type === 'image' 
                    ? (index === 0 ? '可输入本地路径或外部链接' : `选项 ${['A', 'B', 'C', 'D'][index]} 图片URL`)
                    : `选项 ${['A', 'B', 'C', 'D'][index]}`"
                  style="flex: 1;"
                ></el-input>
                <el-button 
                  type="danger" 
                  circle 
                  :icon="Delete" 
                  @click="removeOption(index)"
                  size="small"
                ></el-button>
              </div>
              <!-- 图片预览 -->
              <div v-if="editingQuestion.option_type === 'image' && parsedOptions[index]" style="margin-top: 8px; margin-left: 30px;">
                <el-popover placement="right" :width="300" trigger="hover">
                  <template #reference>
                    <div class="preview-thumbnail">
                      <img 
                        :src="parsedOptions[index]" 
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
                      :src="parsedOptions[index]" 
                      style="width: 100%; border-radius: 4px;"
                      alt="大图预览"
                    />
                  </div>
                </el-popover>
              </div>
            </div>
            <el-button type="primary" @click="addOption" :icon="Plus">添加选项</el-button>
          </div>
        </el-form-item>
        
        <el-form-item label="正确答案" prop="answer">
          <el-input
            v-model="editingQuestion.answer"
            placeholder="请输入正确答案"
            maxlength="500"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm" :loading="submitting">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, reactive, onMounted, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, Search, Refresh, Headset, ZoomIn } from '@element-plus/icons-vue'
import { apiService } from '../api/index.js'

export default {
  name: 'QuestionPage',
  setup() {
    // 数据定义
    const questions = ref([])
    const loading = ref(false)
    const submitting = ref(false)
    const dialogVisible = ref(false)
    const questionFormRef = ref(null)
    const searchKeyword = ref('')
    const typeFilter = ref('')
    const levelFilter = ref('')
    const difficultyFilter = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const parsedOptions = ref([])
    
    // 简化后的题目类型（6种主要类型，听力题通过听力题组管理）
    const questionTypes = [
      'reading',    // 阅读题
      'writing',    // 书写题
      'fill',       // 填空题
      'single',     // 单选题
      'multiple',   // 多选题
      'judge'       // 判断题
    ]
    
    // 题目类型标签映射（简化版，听力题通过听力题组管理）
    const typeLabels = {
      'reading': '阅读题',
      'writing': '书写题',
      'fill': '填空题',
      'single': '单选题',
      'multiple': '多选题',
      'judge': '判断题'
    }
    
    // 编辑的题目对象 - 包含所有字段
    const editingQuestion = reactive({
      id: null,
      type: '',
      content: '',
      level: 1,
      answer: '',
      options: '[]',
      option_type: 'text', // 'text' | 'image'
      explanation: '',
      // 音频字段
      audio_url: '',
      audio_duration: 0,
      audio_group: '',
      // 图片字段
      image_url: '',
      // 阅读理解字段
      passage: '',
      passage_title: '',
      sub_questions: null,
      // 连线/排序字段
      matching_pairs: null,
      ordering_items: null,
      // 其他字段
      tags: null,
      points: 0,
      time_limit: 0,
      category: null,
      question_set: null,
      difficulty: 3  // 默认中等难度
    })
    
    // 表单验证规则
    const formRules = {
      type: [
        { required: true, message: '请选择题目类型', trigger: 'change' }
      ],
      content: [
        { required: true, message: '请输入题目内容', trigger: 'blur' },
        { min: 2, max: 1000, message: '长度在 2 到 1000 个字符之间', trigger: 'blur' }
      ],
      level: [
        { required: true, message: '请选择HSK等级', trigger: 'change' },
        { type: 'number', min: 1, max: 6, message: 'HSK等级在 1-6 之间', trigger: 'change' }
      ],
      difficulty: [
        { required: true, message: '请选择难度系数', trigger: 'change' },
        { type: 'number', min: 1, max: 5, message: '难度系数在 1-5 之间', trigger: 'change' }
      ],
      answer: [
        { required: true, message: '请输入正确答案', trigger: 'blur' }
      ]
    }
    
    // 计算属性：过滤后的题目列表
    const filteredQuestions = computed(() => {
      let result = questions.value
      
      if (searchKeyword.value) {
        result = result.filter(item => 
          item.content.toLowerCase().includes(searchKeyword.value.toLowerCase())
        )
      }
      
      if (typeFilter.value) {
        result = result.filter(item => item.type === typeFilter.value)
      }
      
      if (levelFilter.value !== '' && levelFilter.value !== null) {
        result = result.filter(item => item.level === levelFilter.value)
      }
      
      if (difficultyFilter.value !== '' && difficultyFilter.value !== null) {
        result = result.filter(item => item.difficulty === difficultyFilter.value)
      }
      
      return result
    })
    
    // 分页后的数据
    const paginatedQuestions = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredQuestions.value.slice(start, end)
    })
    
    // 监听选项变化，并更新editingQuestion.options
    watch(parsedOptions, (newValue) => {
      editingQuestion.options = JSON.stringify(newValue)
    })
    
    // 获取题目列表
    const fetchQuestions = async () => {
      loading.value = true
      console.log('开始获取题目列表')
      try {
        // 传递page_size参数获取所有数据
        const response = await apiService.getQuestions({ page_size: 10000 })
        
        // 处理分页响应
        if (response.data && response.data.results) {
          questions.value = response.data.results
          console.log('获取题目列表成功:', questions.value.length, '/', response.data.count, '道题目')
        } else {
          questions.value = response.data || []
        }
      } catch (error) {
        console.error('获取题目列表失败:', error)
        ElMessage.error('获取题目列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 刷新题目列表
    const refreshQuestions = () => {
      fetchQuestions()
      ElMessage.success('刷新成功')
    }
    
    // 图片加载错误处理
    const handleImageError = (event) => {
      event.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23f5f5f5" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" text-anchor="middle" dy=".3em" fill="%23999"%3E加载失败%3C/text%3E%3C/svg%3E'
    }
    
    // 显示新增对话框
    const showAddDialog = () => {
      Object.assign(editingQuestion, {
        id: null,
        type: '',
        content: '',
        level: 1,
        answer: '',
        options: '[]',
        option_type: 'text',
        explanation: '',
        audio_url: '',
        audio_duration: 0,
        audio_group: '',
        image_url: '',
        passage: '',
        passage_title: '',
        sub_questions: null,
        matching_pairs: null,
        ordering_items: null,
        tags: null,
        points: 0,
        time_limit: 0,
        category: null,
        question_set: null,
        difficulty: 3  // 默认中等难度
      })
      
      parsedOptions.value = []
      dialogVisible.value = true
      
      // 等待DOM更新后设置焦点
      nextTick(() => {
        if (questionFormRef.value) {
          questionFormRef.value.clearValidate()
        }
      })
    }
    
    // 编辑题目
    const editQuestion = (row) => {
      Object.assign(editingQuestion, { ...row })
      
      // 确保option_type有效
      if (!editingQuestion.option_type) {
        editingQuestion.option_type = 'text'
      }
      
      // 确保difficulty有效（1-5），如果无效则使用默认值3
      if (!editingQuestion.difficulty || editingQuestion.difficulty < 1 || editingQuestion.difficulty > 5) {
        editingQuestion.difficulty = 3
      }
      
      try {
        // 如果options已经是数组或对象，直接使用；否则解析JSON字符串
        let optionsData = editingQuestion.options
        if (typeof optionsData === 'string') {
          optionsData = JSON.parse(optionsData || '[]')
        }
        
        // 处理新格式的选项数据 {option_type: 'text', options: [{label, text, value}]}
        if (optionsData && typeof optionsData === 'object' && optionsData.options && Array.isArray(optionsData.options)) {
          // 提取文本内容
          parsedOptions.value = optionsData.options.map(opt => opt.text || opt.label || '')
        } 
        // 处理旧格式（直接是数组）
        else if (Array.isArray(optionsData)) {
          parsedOptions.value = optionsData
        } 
        else {
          parsedOptions.value = []
        }
      } catch (e) {
        console.error('解析选项失败:', e, editingQuestion.options)
        parsedOptions.value = []
      }
      
      dialogVisible.value = true
      
      // 等待DOM更新后设置焦点
      nextTick(() => {
        if (questionFormRef.value) {
          questionFormRef.value.clearValidate()
        }
      })
    }
    
    // 删除题目
    const deleteQuestion = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除该题目吗？删除后无法恢复！', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        loading.value = true
        await apiService.deleteQuestion(id)
        ElMessage.success('删除题目成功')
        await fetchQuestions()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除题目失败:', error)
          ElMessage.error('删除题目失败')
        }
      } finally {
        loading.value = false
      }
    }
    
    // 添加选项
    const addOption = () => {
      parsedOptions.value.push('')
    }
    
    // 移除选项
    const removeOption = (index) => {
      // 确保parsedOptions.value是一个数组
      if (Array.isArray(parsedOptions.value)) {
        parsedOptions.value.splice(index, 1)
      } else {
        // 如果不是数组，先转换为数组再操作
        parsedOptions.value = Array.from(parsedOptions.value || [])
        parsedOptions.value.splice(index, 1)
      }
    }
    
    // 提交表单
    const submitForm = async () => {
      if (!questionFormRef.value) return
      
      try {
        await questionFormRef.value.validate()
        
        // 确保选项是有效的JSON字符串
        if (parsedOptions.value.some(opt => opt === '')) {
          ElMessage.warning('选项内容不能为空')
          return
        }
        
        // 构建要提交的数据 - 包含所有字段
        const questionData = {
          type: editingQuestion.type,
          content: editingQuestion.content,
          level: parseInt(editingQuestion.level) || 1,
          answer: editingQuestion.answer,
          options: JSON.stringify(parsedOptions.value),
          option_type: editingQuestion.option_type || 'text',
          explanation: editingQuestion.explanation || '',
          // 音频字段
          audio_url: editingQuestion.audio_url || '',
          audio_duration: parseInt(editingQuestion.audio_duration) || 0,
          audio_group: editingQuestion.audio_group || '',
          // 图片字段
          image_url: editingQuestion.image_url || '',
          // 阅读理解字段
          passage: editingQuestion.passage || '',
          passage_title: editingQuestion.passage_title || '',
          sub_questions: editingQuestion.sub_questions || null,
          // 连线/排序字段
          matching_pairs: editingQuestion.matching_pairs || null,
          ordering_items: editingQuestion.ordering_items || null,
          // 其他字段
          tags: editingQuestion.tags || null,
          points: parseInt(editingQuestion.points) || 0,
          time_limit: parseInt(editingQuestion.time_limit) || 0,
          category: editingQuestion.category || null,
          question_set: editingQuestion.question_set || null,
          difficulty: parseInt(editingQuestion.difficulty) || 3  // 默认中等难度(1-5)
        }
        
        // 移除空值字段（避免后端验证问题）
        Object.keys(questionData).forEach(key => {
          if (questionData[key] === null || questionData[key] === undefined || questionData[key] === '') {
            if (!['explanation', 'audio_url', 'image_url', 'passage', 'passage_title'].includes(key)) {
              delete questionData[key]
            }
          }
        })
        
        console.log('提交完整数据:', questionData)
        submitting.value = true
        
        if (editingQuestion.id) {
          // 更新
          await apiService.updateQuestion(editingQuestion.id, questionData)
          ElMessage.success('✅ 题目更新成功！所有字段已保存')
        } else {
          // 新增
          await apiService.createQuestion(questionData)
          ElMessage.success('✅ 题目创建成功！')
          
          // 清除筛选器和重置分页，确保新题目可见
          searchKeyword.value = ''
          typeFilter.value = ''
          levelFilter.value = ''
          difficultyFilter.value = ''
          currentPage.value = 1
        }
        
        dialogVisible.value = false
        await fetchQuestions()
      } catch (error) {
        console.error('保存题目失败:', error)
        ElMessage.error('保存题目失败')
      } finally {
        submitting.value = false
      }
    }
    
    // 搜索处理
    const handleSearch = () => {
      currentPage.value = 1
    }
    
    // 清空所有筛选器
    const clearAllFilters = () => {
      searchKeyword.value = ''
      typeFilter.value = ''
      levelFilter.value = ''
      difficultyFilter.value = ''
      currentPage.value = 1
      ElMessage.success('已清空所有筛选器')
    }
    
    // 分页处理
    const handleCurrentChange = (page) => {
      currentPage.value = page
    }
    
    // 更改每页条数
    const handleSizeChange = (size) => {
      pageSize.value = size
      currentPage.value = 1
    }
    
    // 获取标签类型
    const getTagType = (type) => {
      const typeMap = {
        '单选题': 'success',
        '多选题': 'warning',
        '判断题': 'info',
        '填空题': 'danger',
        '连线题': 'primary',
        '阅读理解题': 'primary'
      }
      return typeMap[type] || 'info' // 确保始终返回有效的type值
    }
    
    // 获取难度文字描述
    const getDifficultyText = (difficulty) => {
      const difficultyMap = {
        1: '简单',
        2: '较易',
        3: '中等',
        4: '较难',
        5: '困难'
      }
      return difficultyMap[difficulty] || '中等'
    }
    
    // 获取题型说明
    const getTypeDescription = (type) => {
      const descriptions = {
        'reading': '阅读题 - 包含所有阅读相关题型，可配合文章/对话内容使用',
        'writing': '书写题 - 包含组句、汉字填空、作文等书写相关题型',
        'fill': '填空题 - 需要填写正确答案的题目，包括完形填空等',
        'single': '单选题 - 从多个选项中选择一个正确答案，包括看图选择、匹配题等',
        'multiple': '多选题 - 可以选择多个正确答案',
        'judge': '判断题 - 判断对错'
      }
      return descriptions[type] || '请选择题目类型（听力题请使用听力题组管理）'
    }
    
    // 处理题型变化
    const handleTypeChange = (newType) => {
      // 根据题型初始化相应字段
      if (['image_choice', 'image_description'].includes(newType)) {
        editingQuestion.image_url = editingQuestion.image_url || ''
      }
      if (['passage_reading', 'cloze'].includes(newType)) {
        editingQuestion.passage = editingQuestion.passage || ''
        editingQuestion.passage_title = editingQuestion.passage_title || ''
      }
    }
    
    // 安全解析选项用于显示
    const parseOptionsForDisplay = (options) => {
      if (!options) return []
      try {
        // 如果已经是数组或对象，直接使用；否则解析JSON
        const parsed = typeof options === 'string' ? JSON.parse(options) : options
        
        // 处理新格式 {option_type: 'text', options: [{label, text, value}]}
        if (parsed && typeof parsed === 'object' && parsed.options && Array.isArray(parsed.options)) {
          return parsed.options.map(opt => opt.text || opt.label || opt.value || '')
        }
        
        // 处理旧格式（直接是数组）
        if (Array.isArray(parsed)) {
          return parsed
        }
        
        return []
      } catch (e) {
        console.error('解析选项失败:', e, options)
        return []
      }
    }
    
    // 生命周期钩子
    onMounted(() => {
      fetchQuestions()
    })
    
    return {
      // 数据
      questions,
      filteredQuestions,
      paginatedQuestions,
      loading,
      submitting,
      dialogVisible,
      editingQuestion,
      formRules,
      questionFormRef,
      searchKeyword,
      typeFilter,
      levelFilter,
      difficultyFilter,
      currentPage,
      pageSize,
      parsedOptions,
      questionTypes,
      typeLabels,
      
      // 方法
      fetchQuestions,
      refreshQuestions,
      showAddDialog,
      editQuestion,
      deleteQuestion,
      addOption,
      removeOption,
      submitForm,
      handleSearch,
      clearAllFilters,
      handleCurrentChange,
      handleSizeChange,
      getTagType,
      getDifficultyText,
      getTypeDescription,
      handleTypeChange,
      parseOptionsForDisplay,
      
      // 图标
      Plus,
      Edit,
      Delete,
      Search,
      Refresh,
      Headset,
      ZoomIn,
      
      // 新增方法
      handleImageError
    }
  }
}
</script>

<style scoped>
.question-page {
  padding: 20px;
  height: calc(100vh - 60px);
  overflow: auto;
  box-sizing: border-box;
}

.box-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.box-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-container {
  display: flex;
  margin-bottom: 15px;
  flex-wrap: wrap;
  gap: 12px;
  flex-shrink: 0;
}

.search-input {
  max-width: 300px;
}

.el-table {
  flex: 1;
  overflow: auto;
}

.pagination-container {
  margin-top: 15px;
  padding: 10px 0;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
  border-top: 1px solid #ebeef5;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.option-label {
  width: 30px;
  text-align: center;
  font-weight: bold;
}

.level-selector {
  display: flex;
  align-items: center;
  gap: 15px;
}

.level-text {
  color: #ff9900;
  font-weight: bold;
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
</style>