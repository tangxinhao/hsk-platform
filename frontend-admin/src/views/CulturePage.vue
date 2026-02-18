<template>
  <div class="culture-page">
    <el-tabs v-model="activeTab" type="card">
      <!-- 分类管理 -->
      <el-tab-pane label="分类管理" name="categories">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <h3>文化分类管理</h3>
              <el-button type="primary" @click="showAddCategoryDialog" :icon="Plus">新增分类</el-button>
            </div>
          </template>
          
          <div class="search-container">
            <el-input
              v-model="categorySearch"
              placeholder="搜索分类名称"
              class="search-input"
              :prefix-icon="Search"
              clearable
            ></el-input>
            <el-select v-model="levelFilter" placeholder="级别筛选" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option label="初级" value="初级"></el-option>
              <el-option label="中级" value="中级"></el-option>
              <el-option label="高级" value="高级"></el-option>
            </el-select>
          </div>
          
          <el-table
            :data="filteredCategories"
            v-loading="categoryLoading"
            border
            stripe
          >
            <el-table-column prop="id" label="ID" width="80" sortable />
            <el-table-column prop="name" label="名称" min-width="120" />
            <el-table-column prop="level" label="等级" width="100">
              <template #default="{ row }">
                <el-tag :type="row.level === '初级' ? 'success' : row.level === '中级' ? 'warning' : 'danger'">
                  {{ row.level }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="180" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" @click="editCategory(scope.row)" :icon="Edit">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteCategory(scope.row.id)" :icon="Delete">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <!-- 内容管理 -->
      <el-tab-pane label="内容管理" name="content">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <h3>文化内容管理 (中英双语)</h3>
              <el-button type="primary" @click="showAddContentDialog" :icon="Plus">新增内容</el-button>
            </div>
          </template>
          
          <div class="search-container">
            <el-input
              v-model="contentSearch"
              placeholder="搜索内容标题"
              class="search-input"
              :prefix-icon="Search"
              clearable
            ></el-input>
            <el-select v-model="categoryFilter" placeholder="分类筛选" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id"></el-option>
            </el-select>
          </div>
          
          <el-table
            :data="filteredContents"
            v-loading="contentLoading"
            border
            stripe
          >
            <el-table-column prop="id" label="ID" width="80" sortable />
            <el-table-column prop="title" label="中文标题" min-width="150" />
            <el-table-column prop="title_en" label="英文标题" min-width="150">
              <template #default="{ row }">
                <span style="font-style: italic; color: #606266;">{{ row.title_en || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="category" label="分类" width="120">
              <template #default="{ row }">
                {{ getCategoryName(row.category) }}
              </template>
            </el-table-column>
            <el-table-column prop="difficulty" label="难度" width="100">
              <template #default="{ row }">
                <el-rate v-model="row.difficulty" disabled :max="5" size="small" />
              </template>
            </el-table-column>
            <el-table-column prop="view_count" label="浏览" width="80" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="scope">
                <el-button size="small" type="primary" @click="editContent(scope.row)" :icon="Edit">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteContent(scope.row.id)" :icon="Delete">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="数据统计" name="statistics">
        <el-empty description="数据统计功能开发中...">
          <el-button type="primary">即将上线</el-button>
        </el-empty>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 分类编辑对话框 -->
    <el-dialog
      v-model="categoryDialogVisible"
      :title="categoryForm.id ? '编辑文化分类' : '新增文化分类'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="categoryForm" :rules="categoryRules" ref="categoryFormRef" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="categoryForm.name" placeholder="请输入分类名称" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="等级" prop="level">
          <el-select v-model="categoryForm.level" placeholder="请选择等级" style="width: 100%">
            <el-option label="初级" value="初级"></el-option>
            <el-option label="中级" value="中级"></el-option>
            <el-option label="高级" value="高级"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="categoryForm.description" type="textarea" :rows="4" maxlength="500" show-word-limit />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="categoryDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCategory">保存</el-button>
      </template>
    </el-dialog>
    
    <!-- 内容编辑对话框 (中英双语) -->
    <el-dialog
      v-model="contentDialogVisible"
      :title="contentForm.id ? '编辑文化内容' : '新增文化内容'"
      width="900px"
      :close-on-click-modal="false"
      destroy-on-close
    >
      <el-form :model="contentForm" :rules="contentRules" ref="contentFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="中文标题" prop="title">
              <el-input v-model="contentForm.title" placeholder="中文标题" maxlength="255" show-word-limit />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="英文标题" prop="title_en">
              <el-input v-model="contentForm.title_en" placeholder="English Title" maxlength="255" show-word-limit />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类" prop="category">
              <el-select v-model="contentForm.category" placeholder="请选择分类" style="width: 100%">
                <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="难度" prop="difficulty">
              <el-select v-model="contentForm.difficulty" placeholder="请选择难度" style="width: 100%">
                <el-option label="简单" :value="1"></el-option>
                <el-option label="较易" :value="2"></el-option>
                <el-option label="中等" :value="3"></el-option>
                <el-option label="较难" :value="4"></el-option>
                <el-option label="困难" :value="5"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">
          <span style="font-size: 16px; font-weight: bold;">📝 中英双语段落内容</span>
        </el-divider>
        
        <!-- 动态段落列表 -->
        <div class="paragraphs-container">
          <el-card 
            v-for="(para, index) in contentForm.paragraphs" 
            :key="index" 
            class="paragraph-card"
            shadow="hover"
          >
            <template #header>
              <div class="paragraph-header">
                <span>段落 {{ index + 1 }}</span>
                <el-button 
                  type="danger" 
                  size="small" 
                  :icon="Delete" 
                  @click="removeParagraph(index)"
                  circle
                ></el-button>
              </div>
            </template>
            
            <el-form-item label="中文段落" :prop="`paragraphs.${index}.zh`">
              <el-input 
                v-model="para.zh" 
                type="textarea" 
                :rows="3" 
                placeholder="请输入中文段落内容..."
              />
            </el-form-item>
            
            <el-form-item label="英文段落" :prop="`paragraphs.${index}.en`">
              <el-input 
                v-model="para.en" 
                type="textarea" 
                :rows="3" 
                placeholder="Please enter English paragraph..."
                style="font-style: italic;"
              />
            </el-form-item>
          </el-card>
          
          <el-button 
            type="primary" 
            :icon="Plus" 
            @click="addParagraph" 
            style="width: 100%; margin-top: 10px;"
            plain
          >
            添加新段落
          </el-button>
        </div>
        
        <el-divider />
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="时长(分钟)" prop="duration">
              <el-input-number v-model="contentForm.duration" :min="0" :max="120" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="封面图URL">
              <el-input v-model="contentForm.cover_image" placeholder="可选" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="contentDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitContent" :loading="contentLoading">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, Search } from '@element-plus/icons-vue'
import { apiService } from '../api/index.js'

export default {
  name: 'CulturePage',
  setup() {
    const activeTab = ref('categories')
    
    // 分类相关
    const categoryLoading = ref(false)
    const categories = ref([])
    const categoryDialogVisible = ref(false)
    const categoryFormRef = ref(null)
    const categorySearch = ref('')
    const levelFilter = ref('')
    
    const categoryForm = reactive({
      id: null,
      name: '',
      level: '初级',
      description: ''
    })
    
    const categoryRules = {
      name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
      level: [{ required: true, message: '请选择等级', trigger: 'change' }]
    }
    
    // 内容相关
    const contentLoading = ref(false)
    const contents = ref([])
    const contentDialogVisible = ref(false)
    const contentFormRef = ref(null)
    const contentSearch = ref('')
    const categoryFilter = ref('')
    
    const contentForm = reactive({
      id: null,
      title: '',
      title_en: '',
      category: null,
      difficulty: 3,
      duration: 10,
      cover_image: '',
      content: '',
      content_en: '',
      paragraphs: [
        { zh: '', en: '' }
      ]
    })
    
    const contentRules = {
      title: [{ required: true, message: '请输入中文标题', trigger: 'blur' }],
      category: [{ required: true, message: '请选择分类', trigger: 'change' }]
    }
    
    // 计算属性
    const filteredCategories = computed(() => {
      let result = categories.value
      if (categorySearch.value) {
        result = result.filter(item => 
          item.name.toLowerCase().includes(categorySearch.value.toLowerCase())
        )
      }
      if (levelFilter.value) {
        result = result.filter(item => item.level === levelFilter.value)
      }
      return result
    })
    
    const filteredContents = computed(() => {
      let result = contents.value
      if (contentSearch.value) {
        result = result.filter(item => 
          item.title.toLowerCase().includes(contentSearch.value.toLowerCase()) ||
          (item.title_en && item.title_en.toLowerCase().includes(contentSearch.value.toLowerCase()))
        )
      }
      if (categoryFilter.value) {
        result = result.filter(item => item.category === Number(categoryFilter.value))
      }
      return result
    })
    
    // 获取分类名称
    const getCategoryName = (categoryId) => {
      const cat = categories.value.find(c => c.id === categoryId)
      return cat ? cat.name : '-'
    }
    
    // ===== 分类管理方法 =====
    const fetchCategories = async () => {
      categoryLoading.value = true
      try {
        const res = await apiService.get('/culture/category/?page_size=100')
        // 处理分页响应
        if (res.data && res.data.results) {
          categories.value = res.data.results
        } else if (Array.isArray(res.data)) {
          categories.value = res.data
        } else {
          categories.value = []
        }
        console.log('获取到的分类:', categories.value)
      } catch (error) {
        console.error('获取分类失败:', error)
        ElMessage.error('获取分类列表失败')
        categories.value = []
      } finally {
        categoryLoading.value = false
      }
    }
    
    const showAddCategoryDialog = () => {
      Object.assign(categoryForm, { id: null, name: '', level: '初级', description: '' })
      categoryDialogVisible.value = true
    }
    
    const editCategory = (row) => {
      Object.assign(categoryForm, row)
      categoryDialogVisible.value = true
    }
    
    const deleteCategory = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除该分类吗？', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await apiService.delete(`/culture/category/${id}/`)
        ElMessage.success('删除成功')
        await fetchCategories()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }
    
    const submitCategory = async () => {
      if (!categoryFormRef.value) return
      try {
        await categoryFormRef.value.validate()
        const data = {
          name: categoryForm.name,
          level: categoryForm.level,
          description: categoryForm.description
        }
        
        if (categoryForm.id) {
          await apiService.put(`/culture/category/${categoryForm.id}/`, data)
          ElMessage.success('更新成功')
        } else {
          await apiService.post('/culture/category/', data)
          ElMessage.success('创建成功')
        }
        
        categoryDialogVisible.value = false
        await fetchCategories()
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败')
      }
    }
    
    // ===== 内容管理方法 =====
    const fetchContents = async () => {
      contentLoading.value = true
      try {
        const res = await apiService.get('/culture/content/?page_size=100')
        // 处理分页响应
        if (res.data && res.data.results) {
          contents.value = res.data.results
        } else if (Array.isArray(res.data)) {
          contents.value = res.data
        } else {
          contents.value = []
        }
        console.log('获取到的内容:', contents.value)
      } catch (error) {
        console.error('获取内容失败:', error)
        ElMessage.error('获取内容列表失败')
        contents.value = []
      } finally {
        contentLoading.value = false
      }
    }
    
    const showAddContentDialog = () => {
      Object.assign(contentForm, {
        id: null,
        title: '',
        title_en: '',
        category: null,
        difficulty: 3,
        duration: 10,
        cover_image: '',
        content: '',
        content_en: '',
        paragraphs: [{ zh: '', en: '' }]
      })
      contentDialogVisible.value = true
    }
    
    const editContent = (row) => {
      Object.assign(contentForm, {
        id: row.id,
        title: row.title,
        title_en: row.title_en || '',
        category: row.category,
        difficulty: row.difficulty,
        duration: row.duration,
        cover_image: row.cover_image || '',
        content: row.content,
        content_en: row.content_en || '',
        paragraphs: row.paragraphs && row.paragraphs.length > 0 ? row.paragraphs : [{ zh: '', en: '' }]
      })
      contentDialogVisible.value = true
    }
    
    const deleteContent = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除该内容吗？', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        await apiService.delete(`/culture/content/${id}/`)
        ElMessage.success('删除成功')
        await fetchContents()
      } catch (error) {
        if (error !== 'cancel') {
          console.error('删除失败:', error)
          ElMessage.error('删除失败')
        }
      }
    }
    
    const addParagraph = () => {
      contentForm.paragraphs.push({ zh: '', en: '' })
    }
    
    const removeParagraph = (index) => {
      if (contentForm.paragraphs.length > 1) {
        contentForm.paragraphs.splice(index, 1)
      } else {
        ElMessage.warning('至少保留一个段落')
      }
    }
    
    const submitContent = async () => {
      if (!contentFormRef.value) return
      try {
        await contentFormRef.value.validate()
        
        // 构建content和content_en（从paragraphs中生成）
        const zhParagraphs = contentForm.paragraphs.map(p => p.zh).filter(Boolean)
        const enParagraphs = contentForm.paragraphs.map(p => p.en).filter(Boolean)
        
        const data = {
          title: contentForm.title,
          title_en: contentForm.title_en || '',
          category: contentForm.category,
          difficulty: contentForm.difficulty,
          duration: contentForm.duration,
          cover_image: contentForm.cover_image || '',
          content: zhParagraphs.join('\n\n'),
          content_en: enParagraphs.join('\n\n'),
          paragraphs: contentForm.paragraphs,
          content_type: 'article'
        }
        
        contentLoading.value = true
        
        if (contentForm.id) {
          await apiService.put(`/culture/content/${contentForm.id}/`, data)
          ElMessage.success('更新成功')
        } else {
          await apiService.post('/culture/content/', data)
          ElMessage.success('创建成功')
        }
        
        contentDialogVisible.value = false
        await fetchContents()
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败')
      } finally {
        contentLoading.value = false
      }
    }
    
    // 生命周期
    onMounted(() => {
      fetchCategories()
      fetchContents()
    })
    
    return {
      activeTab,
      
      // 分类
      categoryLoading,
      categories,
      filteredCategories,
      categoryDialogVisible,
      categoryForm,
      categoryRules,
      categoryFormRef,
      categorySearch,
      levelFilter,
      showAddCategoryDialog,
      editCategory,
      deleteCategory,
      submitCategory,
      
      // 内容
      contentLoading,
      contents,
      filteredContents,
      contentDialogVisible,
      contentForm,
      contentRules,
      contentFormRef,
      contentSearch,
      categoryFilter,
      showAddContentDialog,
      editContent,
      deleteContent,
      addParagraph,
      removeParagraph,
      submitContent,
      getCategoryName,
      
      // 图标
      Plus,
      Edit,
      Delete,
      Search
    }
  }
}
</script>

<style scoped>
.culture-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-container {
  display: flex;
  margin-bottom: 20px;
  gap: 15px;
}

.search-input {
  max-width: 300px;
}

.paragraphs-container {
  max-height: 500px;
  overflow-y: auto;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 8px;
}

.paragraph-card {
  margin-bottom: 15px;
}

.paragraph-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.el-form-item {
  margin-bottom: 18px;
}

:deep(.el-rate) {
  height: 20px;
}
</style>
