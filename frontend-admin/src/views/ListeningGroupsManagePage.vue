<template>
  <div class="listening-groups-page">
    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <h3>听力题组管理</h3>
          <div class="header-actions">
            <el-button type="success" @click="fetchGroups" :icon="Refresh">刷新</el-button>
            <el-button type="primary" @click="$router.push('/listening-group/add')" :icon="Plus">
              批量添加题组
            </el-button>
          </div>
        </div>
      </template>

      <!-- 筛选区域 -->
      <div class="filter-container">
        <el-select v-model="levelFilter" placeholder="HSK等级" clearable @change="fetchGroups">
          <el-option label="全部" value=""></el-option>
          <el-option v-for="i in 6" :key="i" :label="`HSK ${i}级`" :value="i" />
        </el-select>
      </div>

      <!-- 题组列表 -->
      <el-table 
        :data="listeningGroups" 
        v-loading="loading"
        border
        style="width: 100%"
      >
        <el-table-column prop="material_group" label="题组ID" width="200" show-overflow-tooltip />
        
        <el-table-column prop="title" label="材料标题" min-width="200" show-overflow-tooltip />
        
        <el-table-column prop="level" label="HSK等级" width="100" align="center">
          <template #default="scope">
            <el-tag :type="getLevelType(scope.row.level)">
              HSK {{ scope.row.level }}级
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="question_count" label="题目数量" width="100" align="center">
          <template #default="scope">
            <el-tag v-if="scope.row.question_count > 0" type="success">
              {{ scope.row.question_count }} 题
            </el-tag>
            <el-tag v-else type="info">0 题</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="音频信息" width="180" align="center">
          <template #default="scope">
            <div class="audio-info-cell">
              <div>
                <el-icon><Clock /></el-icon>
                {{ formatDuration(scope.row.audio_duration) }}
              </div>
              <div>
                <el-icon><Headset /></el-icon>
                播放 {{ scope.row.play_times }} 次
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="180" align="center">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="280" fixed="right" align="center">
          <template #default="scope">
            <el-button-group>
              <el-button 
                size="small" 
                type="primary" 
                @click="viewDetail(scope.row)"
                :icon="View"
              >
                查看
              </el-button>
              <el-button 
                size="small" 
                type="warning" 
                @click="editGroup(scope.row)"
                :icon="Edit"
              >
                编辑
              </el-button>
              <el-popconfirm
                title="确定删除该题组吗？"
                @confirm="deleteGroup(scope.row.material_group)"
                width="200"
              >
                <template #reference>
                  <el-button size="small" type="danger" :icon="Delete">
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="!loading && (!listeningGroups || listeningGroups.length === 0)" class="empty-container">
        <el-empty description="暂无听力题组数据">
          <el-button type="primary" @click="$router.push('/listening-group/add')">
            添加第一个题组
          </el-button>
        </el-empty>
      </div>

      <div v-if="listeningGroups && listeningGroups.length > 0" class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="handlePageChange"
          background
        />
      </div>
    </el-card>


    <!-- 题组详情对话框 -->
    <el-dialog v-model="detailDialogVisible" title="题组详情" width="80%">
      <div v-loading="detailLoading">
        <div v-if="selectedGroup && selectedGroup.material">
          <h4>材料信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="标题">{{ selectedGroup.material.title || '-' }}</el-descriptions-item>
            <el-descriptions-item label="HSK等级">HSK {{ selectedGroup.material.level || '-' }}级</el-descriptions-item>
            <el-descriptions-item label="音频时长">{{ formatDuration(selectedGroup.material.audio_duration || 0) }}</el-descriptions-item>
            <el-descriptions-item label="播放次数">{{ selectedGroup.material.play_times || 0 }} 次</el-descriptions-item>
            <el-descriptions-item label="题目数量">{{ (selectedGroup.questions && selectedGroup.questions.length) || 0 }} 道</el-descriptions-item>
          </el-descriptions>

          <h4 style="margin-top: 20px;">题目列表</h4>
          <el-table :data="selectedGroup.questions || []" border>
            <el-table-column prop="question_number" label="题号" width="80" align="center" />
            <el-table-column prop="content" label="题目内容" min-width="200" show-overflow-tooltip />
            <el-table-column prop="type" label="题型" width="100" align="center">
              <template #default="scope">
                {{ getTypeLabel(scope.row.type) }}
              </template>
            </el-table-column>
            <el-table-column label="选项数量" width="100" align="center">
              <template #default="scope">
                {{ getOptionsCount(scope.row.options) }} 个
              </template>
            </el-table-column>
            <el-table-column label="选项类型" width="100" align="center">
              <template #default="scope">
                {{ getOptionTypeLabel(scope.row.options) }}
              </template>
            </el-table-column>
            <el-table-column prop="answer" label="答案" width="80" align="center">
              <template #default="scope">
                <el-tag type="success">{{ scope.row.answer }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="120" align="center">
              <template #default="scope">
                <el-rate v-if="scope.row.difficulty" v-model="scope.row.difficulty" disabled :max="5" size="small" />
                <span v-else>-</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else style="padding: 40px; text-align: center;">
          <el-empty description="无法加载题组详情" />
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Refresh, Plus, View, Edit, Delete, Clock, Headset
} from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'ListeningGroupsManagePage',
  components: {
    Refresh, Plus, View, Edit, Delete, Clock, Headset
  },
  setup() {
    // 确保axios使用正确的baseURL
    if (!axios.defaults.baseURL) {
      axios.defaults.baseURL = '/api'
      console.log('已设置axios.defaults.baseURL = /api')
    }
    const router = useRouter()
    const loading = ref(false)
    const detailLoading = ref(false)
    const listeningGroups = ref([])
    const levelFilter = ref('')
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    
    const detailDialogVisible = ref(false)
    const selectedGroup = ref(null)

    const fetchGroups = async () => {
      loading.value = true
      try {
        const params = {}
        if (levelFilter.value) {
          params.level = levelFilter.value
        }
        
        console.log('正在请求API: /question/listening-groups/', params)
        const response = await axios.get('/question/listening-groups/', { params })
        console.log('API完整响应:', response.data)
        
        // 确保正确获取数据 - 先初始化为空数组
        listeningGroups.value = []
        
        if (response.data) {
          let results = []
          
          if (Array.isArray(response.data.results)) {
            results = response.data.results
          } else if (Array.isArray(response.data)) {
            results = response.data
          }
          
          // 确保每个元素都有必要的属性
          listeningGroups.value = results.map(item => {
            if (!item || typeof item !== 'object') {
              return {
                material_group: '',
                title: '',
                level: 0,
                question_count: 0,
                audio_duration: 0,
                play_times: 0,
                audio_url: ''
              }
            }
            return {
              material_group: item.material_group || '',
              title: item.title || '',
              level: item.level || 0,
              question_count: item.question_count || 0,
              audio_duration: item.audio_duration || 0,
              play_times: item.play_times || 0,
              audio_url: item.audio_url || '',
              created_at: item.created_at || ''
            }
          })
          
          total.value = response.data.count || listeningGroups.value.length
        } else {
          total.value = 0
        }
        
        console.log('解析后的题组列表:', listeningGroups.value.length, '个')
        console.log('题组数据:', listeningGroups.value)
      } catch (error) {
        console.error('获取题组列表失败:', error)
        console.error('错误详情:', error.response?.data)
        ElMessage.error('获取题组列表失败: ' + (error.response?.data?.detail || error.message))
        listeningGroups.value = [] // 确保错误时也是空数组
        total.value = 0
      } finally {
        loading.value = false
      }
    }

    const viewDetail = async (group) => {
      if (!group || !group.material_group) {
        ElMessage.error('无效的题组数据')
        return
      }
      
      detailDialogVisible.value = true
      detailLoading.value = true
      selectedGroup.value = null
      
      try {
        console.log('正在获取题组详情:', group.material_group)
        const response = await axios.get(`/question/listening-group/${group.material_group}/`)
        console.log('题组详情:', response.data)
        
        // 确保数据结构完整
        selectedGroup.value = {
          material: response.data.material || {},
          questions: Array.isArray(response.data.questions) ? response.data.questions : []
        }
      } catch (error) {
        console.error('获取题组详情失败:', error)
        console.error('错误详情:', error.response?.data)
        ElMessage.error('获取题组详情失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        detailLoading.value = false
      }
    }

    const editGroup = (group) => {
      router.push(`/listening-group/edit/${group.material_group}`)
    }

    const deleteGroup = async (materialGroup) => {
      try {
        console.log('正在删除题组:', materialGroup)
        await axios.delete(`/question/listening-group/${materialGroup}/delete/`)
        ElMessage.success('删除成功')
        fetchGroups()
      } catch (error) {
        console.error('删除失败:', error)
        console.error('错误详情:', error.response?.data)
        ElMessage.error('删除失败: ' + (error.response?.data?.detail || error.message))
      }
    }

    const formatDuration = (seconds) => {
      if (!seconds) return '未知'
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins}:${secs.toString().padStart(2, '0')}`
    }

    const formatDate = (dateStr) => {
      if (!dateStr) return '-'
      try {
        const date = new Date(dateStr)
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
      } catch (e) {
        console.error('日期格式化错误:', e, dateStr)
        return '-'
      }
    }

    const getLevelType = (level) => {
      const types = ['', 'success', 'success', 'warning', 'warning', 'danger', 'danger']
      return types[level] || 'info'
    }

    const getTypeLabel = (type) => {
      const labels = {
        'single': '单选题',
        'multiple': '多选题',
        'judge': '判断题'
      }
      return labels[type] || type
    }

    const getOptionsCount = (options) => {
      try {
        const parsed = typeof options === 'string' ? JSON.parse(options) : options
        if (parsed?.options && Array.isArray(parsed.options)) {
          return parsed.options.length
        }
        if (Array.isArray(parsed)) {
          return parsed.length
        }
        return 0
      } catch {
        return 0
      }
    }

    const getOptionTypeLabel = (options) => {
      try {
        const parsed = typeof options === 'string' ? JSON.parse(options) : options
        const type = parsed?.option_type || 'text'
        const labels = {
          'text': '文字',
          'image': '图片',
          'mixed': '图文'
        }
        return labels[type] || '文字'
      } catch (e) {
        console.error('解析选项类型失败:', e, options)
        return '文字'
      }
    }

    const handlePageChange = (page) => {
      currentPage.value = page
    }

    onMounted(() => {
      fetchGroups()
    })

    return {
      loading,
      detailLoading,
      listeningGroups,
      levelFilter,
      currentPage,
      pageSize,
      total,
      detailDialogVisible,
      selectedGroup,
      fetchGroups,
      viewDetail,
      editGroup,
      deleteGroup,
      formatDuration,
      formatDate,
      getLevelType,
      getTypeLabel,
      getOptionsCount,
      getOptionTypeLabel,
      handlePageChange,
      Refresh,
      Plus,
      View,
      Edit,
      Delete
    }
  }
}
</script>

<style scoped>
.listening-groups-page {
  padding: 20px;
  height: calc(100vh - 80px);
  overflow-y: auto;
  overflow-x: hidden;
  box-sizing: border-box;
}

.box-card {
  min-height: calc(100vh - 120px);
  display: flex;
  flex-direction: column;
}

.box-card :deep(.el-card__body) {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
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

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-container {
  flex-shrink: 0;
  margin-bottom: 15px;
  display: flex;
  gap: 10px;
}

.el-table {
  flex: 1;
  overflow-x: auto;
  margin-bottom: 20px;
}

.el-table :deep(.el-table__header-wrapper) {
  overflow-x: hidden;
}

.pagination-container {
  flex-shrink: 0;
  margin-top: 20px;
  padding: 15px 0;
  text-align: center;
  border-top: 1px solid #ebeef5;
}

.audio-info-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
}

.audio-info-cell > div {
  display: flex;
  align-items: center;
  gap: 4px;
  justify-content: center;
}
</style>
