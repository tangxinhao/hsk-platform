<template>
  <div class="culture-page">
    <div class="page-header">
      <h1>文化学习</h1>
      <p>探索中华文化的博大精深</p>
    </div>

    <!-- 分类筛选 -->
    <div class="categories-section" v-if="categories.length > 0">
      <el-scrollbar>
        <div class="categories-list">
          <div
            v-for="cat in categories"
            :key="cat.id"
            class="category-item"
            :class="{ active: selectedCategory === cat.id }"
            @click="selectCategory(cat.id)"
          >
            <span class="category-icon">{{ getCategoryIcon(cat.name) }}</span>
            <span class="category-name">{{ cat.name }}</span>
            <el-tag :type="getDifficultyType(cat.level)" size="small">{{ cat.level }}</el-tag>
          </div>
        </div>
      </el-scrollbar>
    </div>

    <!-- 内容列表 -->
    <div class="content-section">
      <el-row :gutter="20" v-loading="loading">
        <el-col
          v-for="item in filteredContents"
          :key="item.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="6"
        >
          <el-card class="content-card" shadow="hover" @click="viewDetail(item)">
            <div class="card-image">
              <img v-if="item.cover_image" :src="item.cover_image" :alt="item.title" />
              <div v-else class="image-placeholder">
                {{ getCategoryIcon(getCategoryNameById(item.category)) }}
              </div>
              <div class="card-overlay">
                <el-button type="primary" circle>
                  <el-icon><View /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="card-content">
              <h3>{{ item.title }}</h3>
              <p v-if="item.title_en" class="title-en">{{ item.title_en }}</p>
              <div class="card-meta">
                <span>
                  <el-icon><Clock /></el-icon>
                  {{ item.duration || 10 }}分钟
                </span>
                <span>
                  <el-icon><View /></el-icon>
                  {{ item.view_count || 0 }}
                </span>
                <el-rate v-model="item.difficulty" disabled :max="5" size="small" />
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-empty v-if="!loading && filteredContents.length === 0" description="暂无内容" />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { View, Clock } from '@element-plus/icons-vue'

export default {
  name: 'CulturePage',
  components: {
    View,
    Clock
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const categories = ref([])
    const contents = ref([])
    const selectedCategory = ref(null)

    // 获取分类
    const fetchCategories = async () => {
      try {
        // axios 在 main.js 中已经将 baseURL 设置为 /api
        // 这里使用相对路径，最终请求为 /api/culture/category/
        const res = await axios.get('/culture/category/')
        // 处理Django REST Framework分页响应
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
        categories.value = []
        ElMessage.error('获取分类失败')
      }
    }

    // 获取内容
    const fetchContents = async () => {
      loading.value = true
      try {
        // 最终请求为 /api/culture/content/
        const res = await axios.get('/culture/content/')
        // 处理Django REST Framework分页响应
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
        contents.value = []
        ElMessage.error('获取内容失败')
      } finally {
        loading.value = false
      }
    }

    // 过滤内容
    const filteredContents = computed(() => {
      if (!Array.isArray(contents.value)) {
        return []
      }
      if (!selectedCategory.value) {
        return contents.value
      }
      return contents.value.filter(item => item.category === selectedCategory.value)
    })

    // 选择分类
    const selectCategory = (categoryId) => {
      selectedCategory.value = selectedCategory.value === categoryId ? null : categoryId
    }

    // 获取分类名称
    const getCategoryNameById = (categoryId) => {
      if (!Array.isArray(categories.value)) {
        return ''
      }
      const cat = categories.value.find(c => c.id === categoryId)
      return cat ? cat.name : ''
    }

    // 获取分类图标
    const getCategoryIcon = (categoryName) => {
      const iconMap = {
        '饮食文化': '🍜',
        '中国节日': '🏮',
        '中国美食': '🥘',
        '中国历史': '📜',
        '中国文学': '📚',
        '中国艺术': '🎨',
        '传统节日': '🎊',
        '茶文化': '🍵',
        '书法': '✍️'
      }
      return iconMap[categoryName] || '📖'
    }

    // 获取难度类型
    const getDifficultyType = (level) => {
      const typeMap = {
        '初级': 'success',
        '中级': 'warning',
        '高级': 'danger'
      }
      return typeMap[level] || 'info'
    }

    // 查看详情
    const viewDetail = (item) => {
      router.push({
        name: 'CultureDetail',
        params: { id: item.id }
      })
    }

    onMounted(async () => {
      await fetchCategories()
      await fetchContents()
    })

    return {
      loading,
      categories,
      contents,
      selectedCategory,
      filteredContents,
      selectCategory,
      getCategoryNameById,
      getCategoryIcon,
      getDifficultyType,
      viewDetail
    }
  }
}
</script>

<style scoped>
.culture-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  color: #333333;
  padding: 30px 20px;
}

.page-header {
  text-align: center;
  color: white;
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 38px;
  margin: 0 0 10px 0;
}

.page-header p {
  font-size: 17px;
  opacity: 0.9;
  margin: 0;
}

.categories-section {
  max-width: 1200px;
  margin: 0 auto 24px;
  background: rgba(255, 255, 255, 0.95);
  padding: 14px 20px;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.categories-list {
  display: flex;
  gap: 8px;
  padding: 0;
  justify-content: center;
  flex-wrap: wrap;
}

.category-item {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #FFFFCC;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.category-item:hover {
  background: #FFFFFF;
  border: 1px solid #CCFFFF;
  transform: translateY(-2px);
}

.category-item.active {
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  color: #333333;
  color: white;
  border-color: #CCFFFF;
}

.category-icon {
  font-size: 20px;
}

.category-name {
  font-weight: 500;
  font-size: 14px;
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.content-card {
  cursor: pointer;
  margin-bottom: 16px;
  transition: all 0.3s ease;
  border-radius: 14px;
  overflow: hidden;
}

.content-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}

.card-image {
  position: relative;
  width: 100%;
  height: 160px;
  overflow: hidden;
  background: linear-gradient(to bottom, #CCFFFF 0%, #FFFFCC 100%);
  color: #333333;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  font-size: 64px;
  color: rgba(255, 255, 255, 0.9);
}

.card-overlay {
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
  transition: opacity 0.3s ease;
}

.content-card:hover .card-overlay {
  opacity: 1;
}

.card-content {
  padding: 14px 16px;
}

.card-content h3 {
  margin: 0 0 6px 0;
  font-size: 16px;
  color: #333333;
  line-height: 1.4;
}

.title-en {
  font-size: 12px;
  color: #909399;
  font-style: italic;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 12px;
  color: #909399;
}

.card-meta span {
  display: flex;
  align-items: center;
  gap: 3px;
}
</style>
