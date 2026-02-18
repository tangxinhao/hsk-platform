<template>
  <div class="mock-exam-container">
    <div class="page-header">
      <h2>模拟考试题目管理</h2>
      <el-button type="primary" icon="Plus" @click="showDialog('create')">
        创建新模拟考试
      </el-button>
    </div>

    <!-- HSK等级选择器 -->
    <el-card class="level-selector-card">
      <el-radio-group v-model="selectedLevel" size="large" @change="loadExamSets">
        <el-radio-button :value="0">全部等级</el-radio-button>
        <el-radio-button v-for="i in 6" :key="i" :value="i">
          HSK {{ i }}级
        </el-radio-button>
      </el-radio-group>
      
      <div class="stats-info" v-if="selectedLevel">
        <el-tag type="info" size="large">
          当前显示: HSK{{ selectedLevel }}级 模拟考试 ({{ total }} 套)
        </el-tag>
      </div>
    </el-card>

    <!-- 模拟考试列表 -->
    <el-card class="table-card">
      <el-table
        :data="examSets"
        v-loading="loading"
        style="width: 100%"
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="考试名称" min-width="250">
          <template #default="{ row }">
            <div class="exam-title">
              <el-tag type="warning" size="small" style="margin-right: 8px">
                HSK{{ row.level }}
              </el-tag>
              <span>{{ row.title }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="考试类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getExamTypeColor(row.exam_type)">
              {{ getExamTypeLabel(row.exam_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="question_count" label="题目数量" width="120">
          <template #default="{ row }">
            <el-icon><Document /></el-icon>
            {{ row.question_count || 0 }} 题
          </template>
        </el-table-column>
        <el-table-column prop="time_limit" label="时间限制" width="120">
          <template #default="{ row }">
            <el-icon><Clock /></el-icon>
            {{ row.time_limit }} 分钟
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="showDialog('edit', row)">
              编辑
            </el-button>
            <el-button size="small" type="info" @click="manageQuestions(row)">
              管理题目
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          @current-change="loadExamSets"
          @size-change="loadExamSets"
        />
      </div>

      <el-empty v-if="!loading && examSets.length === 0" description="暂无模拟考试题目" />
    </el-card>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '创建模拟考试' : '编辑模拟考试'"
      width="600px"
    >
      <el-form
        :model="formData"
        :rules="formRules"
        ref="formRef"
        label-width="100px"
      >
        <el-form-item label="考试名称" prop="title">
          <el-input 
            v-model="formData.title" 
            placeholder="例如：HSK3真题试卷 (H31550)"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="HSK等级" prop="level">
          <el-select v-model="formData.level" placeholder="请选择HSK等级">
            <el-option v-for="i in 6" :key="i" :label="`HSK ${i}级`" :value="i" />
          </el-select>
        </el-form-item>

        <el-form-item label="考试类型" prop="exam_type">
          <el-select v-model="formData.exam_type" placeholder="请选择考试类型">
            <el-option label="真题" value="real" />
            <el-option label="模拟题" value="mock" />
            <el-option label="样卷" value="sample" />
            <el-option label="练习题" value="practice" />
          </el-select>
        </el-form-item>

        <el-form-item label="时间限制" prop="time_limit">
          <el-input-number 
            v-model="formData.time_limit" 
            :min="10" 
            :max="300" 
            :step="5"
          />
          <span style="margin-left: 10px;">分钟</span>
        </el-form-item>

        <el-form-item label="题目数量" prop="question_count">
          <el-input-number 
            v-model="formData.question_count" 
            :min="1" 
            :max="200" 
            :step="1"
          />
          <span style="margin-left: 10px;">题</span>
        </el-form-item>

        <el-form-item label="描述">
          <el-input 
            v-model="formData.description" 
            type="textarea" 
            :rows="4"
            placeholder="请输入考试描述"
            maxlength="500"
            show-word-limit
          />
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Clock, Plus } from '@element-plus/icons-vue'
import { apiService } from '../api/index.js'

const router = useRouter()

// 数据定义
const selectedLevel = ref(0) // 0表示全部等级
const loading = ref(false)
const submitting = ref(false)
const dialogVisible = ref(false)
const dialogMode = ref('create') // 'create' | 'edit'
const formRef = ref(null)

const examSets = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const formData = reactive({
  id: null,
  title: '',
  level: 1,
  exam_type: 'mock',
  time_limit: 120,
  question_count: 30,
  description: ''
})

const formRules = {
  title: [
    { required: true, message: '请输入考试名称', trigger: 'blur' },
    { min: 2, max: 200, message: '长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  level: [
    { required: true, message: '请选择HSK等级', trigger: 'change' }
  ],
  exam_type: [
    { required: true, message: '请选择考试类型', trigger: 'change' }
  ],
  time_limit: [
    { required: true, message: '请输入时间限制', trigger: 'blur' }
  ],
  question_count: [
    { required: true, message: '请输入题目数量', trigger: 'blur' }
  ]
}

// 加载考试套卷列表
const loadExamSets = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    // 如果选择了具体等级，添加等级过滤
    if (selectedLevel.value > 0) {
      params.level = selectedLevel.value
    }
    
    const response = await apiService.getExamSets(params)
    
    if (response.data.results) {
      examSets.value = response.data.results
      total.value = response.data.count
    } else if (Array.isArray(response.data)) {
      examSets.value = response.data
      total.value = response.data.length
    }
    
    console.log('加载模拟考试列表:', examSets.value.length, '套')
  } catch (error) {
    console.error('加载模拟考试列表失败:', error)
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

// 显示对话框
const showDialog = (mode, row = null) => {
  dialogMode.value = mode
  
  if (mode === 'create') {
    Object.assign(formData, {
      id: null,
      title: '',
      level: selectedLevel.value > 0 ? selectedLevel.value : 1,
      exam_type: 'mock',
      time_limit: 120,
      question_count: 30,
      description: ''
    })
  } else {
    Object.assign(formData, {
      id: row.id,
      title: row.title,
      level: row.level,
      exam_type: row.exam_type || 'mock',
      time_limit: row.time_limit,
      question_count: row.question_count,
      description: row.description || ''
    })
  }
  
  dialogVisible.value = true
  
  // 清除验证
  setTimeout(() => {
    formRef.value?.clearValidate()
  }, 0)
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    submitting.value = true
    
    const data = {
      title: formData.title,
      level: formData.level,
      exam_type: formData.exam_type,
      time_limit: formData.time_limit,
      question_count: formData.question_count,
      description: formData.description
    }
    
    if (dialogMode.value === 'create') {
      await apiService.createExamSet(data)
      ElMessage.success('创建成功')
    } else {
      await apiService.updateExamSet(formData.id, data)
      ElMessage.success('更新成功')
    }
    
    dialogVisible.value = false
    loadExamSets()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('提交失败:', error)
      ElMessage.error('操作失败')
    }
  } finally {
    submitting.value = false
  }
}

// 删除套卷
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除"${row.title}"吗？删除后无法恢复！`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await apiService.deleteExamSet(row.id)
    ElMessage.success('删除成功')
    loadExamSets()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 管理题目
const manageQuestions = (row) => {
  router.push(`/exam-set/${row.id}/questions`)
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 获取考试类型颜色
const getExamTypeColor = (type) => {
  const colorMap = {
    'real': 'danger',
    'mock': 'warning',
    'sample': 'success',
    'practice': 'info'
  }
  return colorMap[type] || 'info'
}

// 获取考试类型标签
const getExamTypeLabel = (type) => {
  const labelMap = {
    'real': '真题',
    'mock': '模拟题',
    'sample': '样卷',
    'practice': '练习题'
  }
  return labelMap[type] || '未知'
}

// 页面加载时获取数据
onMounted(() => {
  loadExamSets()
})
</script>

<style scoped>
.mock-exam-container {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.level-selector-card {
  margin-bottom: 20px;
}

.stats-info {
  margin-top: 15px;
}

.table-card {
  margin-bottom: 20px;
}

.exam-title {
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

:deep(.el-radio-group) {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

:deep(.el-radio-button) {
  margin: 0;
}
</style>
