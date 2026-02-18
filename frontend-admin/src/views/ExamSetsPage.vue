<template>
  <div class="exam-sets-container">
    <div class="page-header">
      <h2>考试套卷管理</h2>
      <el-button type="primary" icon="Plus" @click="showDialog('create')">
        创建新套卷
      </el-button>
    </div>

    <!-- 筛选和搜索 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filters">
        <el-form-item label="等级">
          <el-select v-model="filters.level" placeholder="全部等级" clearable>
            <el-option label="全部" :value="null" />
            <el-option v-for="i in 6" :key="i" :label="`HSK${i}`" :value="i" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadExamSets">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 套卷列表 -->
    <el-card class="table-card">
      <el-table
        :data="examSets"
        v-loading="loading"
        style="width: 100%"
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="套卷名称" min-width="200" />
        <el-table-column label="等级" width="100">
          <template #default="{ row }">
            <el-tag type="warning">HSK{{ row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="question_count" label="题目数量" width="120">
          <template #default="{ row }">
            {{ row.question_count || 0 }} 题
          </template>
        </el-table-column>
        <el-table-column prop="time_limit" label="时间限制" width="120">
          <template #default="{ row }">
            {{ row.time_limit }} 分钟
          </template>
        </el-table-column>
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

      <div class="pagination">
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
    </el-card>

    <!-- 创建/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogMode === 'create' ? '创建考试套卷' : '编辑考试套卷'"
      width="600px"
    >
      <el-form
        :model="formData"
        :rules="formRules"
        ref="formRef"
        label-width="100px"
      >
        <el-form-item label="套卷名称" prop="title">
          <el-input v-model="formData.title" placeholder="例如：HSK3模拟试卷A" />
        </el-form-item>

        <el-form-item label="等级" prop="level">
          <el-select v-model="formData.level" placeholder="请选择HSK等级">
            <el-option v-for="i in 6" :key="i" :label="`HSK${i}`" :value="i" />
          </el-select>
        </el-form-item>

        <el-form-item label="时间限制" prop="time_limit">
          <el-input-number
            v-model="formData.time_limit"
            :min="30"
            :max="180"
            :step="10"
          />
          <span style="margin-left: 10px">分钟</span>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入套卷描述信息"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ dialogMode === 'create' ? '创建' : '保存' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { apiService } from '../api/index.js'

const router = useRouter()
const loading = ref(false)
const examSets = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const filters = reactive({
  level: null
})

const dialogVisible = ref(false)
const dialogMode = ref('create')
const formRef = ref(null)
const submitting = ref(false)

const formData = reactive({
  title: '',
  level: 1,
  time_limit: 60,
  description: '',
  question_count: 0
})

const formRules = {
  title: [
    { required: true, message: '请输入套卷名称', trigger: 'blur' }
  ],
  level: [
    { required: true, message: '请选择等级', trigger: 'change' }
  ],
  time_limit: [
    { required: true, message: '请设置时间限制', trigger: 'blur' }
  ]
}

const loadExamSets = async () => {
  loading.value = true
  try {
    const params = { page_size: 10000 }
    if (filters.level) params.level = filters.level

    const response = await apiService.getExamSets(params)
    console.log('套卷API响应:', response.data)
    // 处理分页响应
    const data = response.data.results || response.data || []
    examSets.value = data
    total.value = response.data.count || data.length || 0
    console.log(`成功加载 ${examSets.value.length} 个套卷`)
  } catch (error) {
    console.error('加载套卷失败:', error)
    console.error('错误详情:', error.response)
    ElMessage.error(`加载套卷失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.level = null
  loadExamSets()
}

const showDialog = (mode, row = null) => {
  dialogMode.value = mode
  if (mode === 'create') {
    Object.assign(formData, {
      title: '',
      level: 1,
      time_limit: 60,
      description: '',
      question_count: 0
    })
  } else {
    Object.assign(formData, {
      id: row.id,
      title: row.title,
      level: row.level,
      time_limit: row.time_limit,
      description: row.description,
      question_count: row.question_count
    })
  }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
    submitting.value = true

    if (dialogMode.value === 'create') {
      await apiService.createExamSet(formData)
      ElMessage.success('创建成功')
    } else {
      await apiService.updateExamSet(formData.id, formData)
      ElMessage.success('保存成功')
    }

    dialogVisible.value = false
    loadExamSets()
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error(dialogMode.value === 'create' ? '创建失败' : '保存失败')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除套卷"${row.title}"吗？删除后无法恢复！`,
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

const manageQuestions = (row) => {
  router.push(`/questions?exam_set_id=${row.id}`)
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleString('zh-CN')
}

onMounted(() => {
  loadExamSets()
})
</script>

<style scoped>
.exam-sets-container {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.filter-card {
  margin-bottom: 16px;
}

.table-card {
  border-radius: 8px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
