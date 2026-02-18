<template>
  <div class="culture-detail-page">
    <!-- 顶部导航 -->
    <div class="detail-header">
      <el-button @click="goBack" circle>
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <div class="header-actions">
        <el-switch 
          v-if="content.paragraphs && content.paragraphs.length > 0"
          v-model="showBilingual" 
          active-text="中英对照"
          inactive-text="仅中文"
        />
      </div>
    </div>

    <div class="detail-container" v-loading="loading">
      <div v-if="!loading && content.id">
        <!-- 文章头部 -->
        <div class="article-header">
          <h1 class="article-title">{{ content.title }}</h1>
          <h2 v-if="showBilingual && content.title_en" class="article-title-en">
            {{ content.title_en }}
          </h2>
          <div class="article-meta">
            <el-tag type="primary">{{ getCategoryName(content.category) }}</el-tag>
            <el-rate v-model="content.difficulty" disabled :max="5" size="small" />
            <span class="meta-item">
              <el-icon><View /></el-icon>
              {{ content.view_count || 0 }} 次浏览
            </span>
            <span class="meta-item">
              <el-icon><Clock /></el-icon>
              {{ content.duration || 10 }} 分钟
            </span>
          </div>
        </div>

        <!-- 文章内容 -->
        <div class="article-content">
          <!-- 有段落数据时显示段落 -->
          <div v-if="content.paragraphs && content.paragraphs.length > 0">
            <div 
              v-for="(paragraph, index) in content.paragraphs" 
              :key="index"
              class="paragraph-group"
            >
              <!-- 中文段落 -->
              <div class="paragraph paragraph-zh">
                <div class="paragraph-number">P{{ index + 1 }}</div>
                <div class="paragraph-text">{{ paragraph.zh }}</div>
              </div>
              
              <!-- 英文段落 -->
              <div v-if="showBilingual && paragraph.en" class="paragraph paragraph-en">
                <div class="paragraph-text">{{ paragraph.en }}</div>
              </div>
            </div>
          </div>

          <!-- 没有段落数据时显示普通内容 -->
          <div v-else class="simple-content">
            <p>{{ content.content }}</p>
            <p v-if="showBilingual && content.content_en" class="content-en">{{ content.content_en }}</p>
          </div>
        </div>

        <!-- 底部操作 -->
        <div class="article-actions">
          <el-button type="primary" size="large">
            <el-icon><Star /></el-icon>
            收藏
          </el-button>
          <el-button size="large">
            <el-icon><Share /></el-icon>
            分享
          </el-button>
        </div>
      </div>

      <el-empty v-else-if="!loading" description="内容不存在" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { ArrowLeft, View, Star, Share, Clock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'CultureDetailPage',
  components: {
    ArrowLeft,
    View,
    Star,
    Share,
    Clock
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const showBilingual = ref(true)
    const content = ref({})
    const categories = ref([])

    // 获取分类列表
    const fetchCategories = async () => {
      try {
        // axios 的 baseURL 已经是 /api，这里用相对路径即可
        const res = await axios.get('/culture/category/')
        if (res.data && res.data.results) {
          categories.value = res.data.results
        } else if (Array.isArray(res.data)) {
          categories.value = res.data
        } else {
          categories.value = []
        }
      } catch (error) {
        console.error('获取分类失败:', error)
        categories.value = []
      }
    }

    // 加载内容
    const loadContent = async () => {
      const id = route.params.id
      if (!id) {
        ElMessage.error('内容ID不存在')
        router.back()
        return
      }

      loading.value = true
      try {
        // 最终请求为 /api/culture/content/:id/
        const res = await axios.get(`/culture/content/${id}/`)
        content.value = res.data || {}
        console.log('加载的内容:', content.value)
      } catch (error) {
        console.error('加载内容失败:', error)
        ElMessage.error('加载内容失败')
        setTimeout(() => {
          router.back()
        }, 1500)
      } finally {
        loading.value = false
      }
    }

    // 获取分类名称
    const getCategoryName = (categoryId) => {
      if (!Array.isArray(categories.value) || !categoryId) {
        return ''
      }
      const cat = categories.value.find(c => c.id === categoryId)
      return cat ? cat.name : ''
    }

    // 返回上一页
    const goBack = () => {
      router.back()
    }

    onMounted(async () => {
      await fetchCategories()
      await loadContent()
    })

    return {
      loading,
      showBilingual,
      content,
      getCategoryName,
      goBack
    }
  }
}
</script>

<style scoped>
.culture-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 40px;
}

.detail-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-actions {
  display: flex;
  gap: 16px;
  align-items: center;
}

.detail-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 20px;
}

.article-header {
  background: white;
  padding: 32px;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.article-title {
  font-size: 36px;
  font-weight: bold;
  color: #303133;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.article-title-en {
  font-size: 24px;
  color: #606266;
  margin: 0 0 20px 0;
  line-height: 1.5;
  font-style: italic;
}

.article-meta {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
  font-size: 14px;
}

.article-content {
  background: white;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.paragraph-group {
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid #f0f0f0;
}

.paragraph-group:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.paragraph {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.paragraph:last-child {
  margin-bottom: 0;
}

.paragraph-number {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
}

.paragraph-text {
  flex: 1;
  font-size: 18px;
  line-height: 2;
  color: #303133;
}

.paragraph-zh .paragraph-text {
  color: #303133;
  font-weight: 500;
}

.paragraph-en {
  padding-left: 56px;
  margin-top: -8px;
}

.paragraph-en .paragraph-text {
  color: #606266;
  font-size: 16px;
  line-height: 1.8;
  font-style: italic;
  background: #f8f9fa;
  padding: 12px 16px;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.simple-content {
  font-size: 18px;
  line-height: 2;
  color: #303133;
}

.simple-content p {
  margin-bottom: 20px;
}

.content-en {
  color: #606266;
  font-style: italic;
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.article-actions {
  margin-top: 32px;
  display: flex;
  gap: 16px;
  justify-content: center;
}

.article-actions .el-button {
  min-width: 160px;
}

@media (max-width: 768px) {
  .detail-container {
    padding: 20px 12px;
  }

  .article-header,
  .article-content {
    padding: 20px;
  }

  .article-title {
    font-size: 28px;
  }

  .article-title-en {
    font-size: 20px;
  }

  .paragraph-text {
    font-size: 16px;
  }

  .paragraph-en .paragraph-text {
    font-size: 14px;
  }

  .article-actions {
    flex-direction: column;
  }

  .article-actions .el-button {
    width: 100%;
  }
}
</style>
