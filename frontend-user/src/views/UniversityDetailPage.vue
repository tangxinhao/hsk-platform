<template>
  <div class="university-detail-page">
    <!-- 顶部导航 -->
    <div class="detail-header">
      <el-button @click="goBack" circle size="large">
        <el-icon><ArrowLeft /></el-icon>
      </el-button>
      <div class="header-actions">
        <el-switch 
          v-if="hasEnglishContent"
          v-model="showBilingual" 
          active-text="中英对照"
          inactive-text="仅中文"
        />
      </div>
    </div>

    <div class="detail-container" v-loading="loading">
      <div v-if="!loading && university.id">
        <!-- 大学头部卡片 -->
        <div class="university-header">
          <div class="header-content">
            <div class="logo-section" v-if="university.logo_url">
              <img :src="university.logo_url" :alt="university.name" class="university-logo">
            </div>
            <div class="info-section">
              <h1 class="university-name">{{ university.name }}</h1>
              <p v-if="showBilingual && university.english_name" class="university-name-en">
                {{ university.english_name }}
              </p>
              <div class="meta-info">
                <el-tag type="danger" size="large" v-if="university.ranking">
                  <el-icon><Trophy /></el-icon>
                  综合排名 #{{ university.ranking }}
                </el-tag>
                <el-tag type="warning" size="large">
                  <el-icon><Location /></el-icon>
                  {{ university.region }} · {{ university.city }}
                </el-tag>
                <el-tag type="success" size="large">
                  <el-icon><Reading /></el-icon>
                  HSK {{ university.min_hsk_level }}级及以上
                </el-tag>
              </div>
              
              <div class="tag-list" v-if="getTags(university).length > 0">
                <el-tag v-for="tag in getTags(university)" :key="tag" type="info">{{ tag }}</el-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab导航 -->
        <el-tabs v-model="activeTab" class="detail-tabs">
          <!-- 学校简介 -->
          <el-tab-pane label="学校简介" name="intro">
            <div class="content-section">
              <h2>学校简介</h2>
              <p class="description-zh">{{ university.description }}</p>
              <p v-if="showBilingual && university.description_en" class="description-en">
                {{ university.description_en }}
              </p>
            </div>

            <div class="content-section" v-if="university.history">
              <h2>历史沿革</h2>
              <p class="description-zh">{{ university.history }}</p>
              <p v-if="showBilingual && university.history_en" class="description-en">
                {{ university.history_en }}
              </p>
            </div>
          </el-tab-pane>

          <!-- 学校优势 -->
          <el-tab-pane label="学校优势" name="advantages">
            <div class="content-section">
              <h2>学校特色</h2>
              <p class="description-zh">{{ university.features }}</p>
              <p v-if="showBilingual && university.features_en" class="description-en">
                {{ university.features_en }}
              </p>
            </div>

            <div class="content-section" v-if="university.advantages && university.advantages.length > 0">
              <h2>核心优势</h2>
              <div class="advantages-list">
                <div v-for="(adv, index) in university.advantages" :key="index" class="advantage-item">
                  <div class="advantage-number">{{ index + 1 }}</div>
                  <div class="advantage-content">
                    <p class="advantage-zh">{{ adv.zh }}</p>
                    <p v-if="showBilingual && adv.en" class="advantage-en">{{ adv.en }}</p>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 专业设置 -->
          <el-tab-pane label="专业设置" name="majors">
            <div class="content-section">
              <h2>热门专业</h2>
              <div class="major-grid" v-if="university.popular_majors && university.popular_majors.length > 0">
                <div v-for="major in university.popular_majors" :key="major" class="major-card popular">
                  <el-icon class="major-icon"><Star /></el-icon>
                  <span>{{ major }}</span>
                </div>
              </div>
            </div>

            <div class="content-section">
              <h2>全部专业</h2>
              <div class="major-grid" v-if="university.majors && university.majors.length > 0">
                <div v-for="major in university.majors" :key="major" class="major-card">
                  <el-icon class="major-icon"><Document /></el-icon>
                  <span>{{ major }}</span>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 申请要求 -->
          <el-tab-pane label="申请要求" name="requirements">
            <div class="content-section">
              <div class="requirement-grid">
                <div class="requirement-item">
                  <div class="req-icon">📚</div>
                  <h3>语言要求</h3>
                  <p>{{ university.language_requirements || '详见学校官网' }}</p>
                </div>
                <div class="requirement-item">
                  <div class="req-icon">💰</div>
                  <h3>学费标准</h3>
                  <p v-if="university.tuition_fee">¥{{ university.tuition_fee }}/学年</p>
                  <p v-else>详见学校官网</p>
                </div>
                <div class="requirement-item">
                  <div class="req-icon">🎓</div>
                  <h3>奖学金</h3>
                  <p>{{ university.scholarship || '详见学校官网' }}</p>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 校园生活 -->
          <el-tab-pane label="校园生活" name="campus">
            <div class="content-section" v-if="university.campus_life && university.campus_life.length > 0">
              <h2>校园生活</h2>
              <div class="campus-life-list">
                <div v-for="(life, index) in university.campus_life" :key="index" class="life-item">
                  <el-icon class="life-icon"><Check /></el-icon>
                  <div class="life-content">
                    <p class="life-zh">{{ life.zh }}</p>
                    <p v-if="showBilingual && life.en" class="life-en">{{ life.en }}</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="content-section">
              <h2>统计数据</h2>
              <div class="stats-grid">
                <div class="stat-box">
                  <div class="stat-value">{{ university.total_students || 0 }}</div>
                  <div class="stat-label">在校学生</div>
                </div>
                <div class="stat-box">
                  <div class="stat-value">{{ university.international_students || 0 }}</div>
                  <div class="stat-label">国际学生</div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 联系方式 -->
          <el-tab-pane label="联系方式" name="contact">
            <div class="content-section">
              <div class="contact-grid">
                <div class="contact-item" v-if="university.website">
                  <el-icon class="contact-icon"><Link /></el-icon>
                  <div>
                    <h3>官方网站</h3>
                    <a :href="university.website" target="_blank">{{ university.website }}</a>
                  </div>
                </div>
                <div class="contact-item" v-if="university.email">
                  <el-icon class="contact-icon"><Message /></el-icon>
                  <div>
                    <h3>联系邮箱</h3>
                    <p>{{ university.email }}</p>
                  </div>
                </div>
                <div class="contact-item" v-if="university.phone">
                  <el-icon class="contact-icon"><Phone /></el-icon>
                  <div>
                    <h3>联系电话</h3>
                    <p>{{ university.phone }}</p>
                  </div>
                </div>
                <div class="contact-item" v-if="university.address">
                  <el-icon class="contact-icon"><Location /></el-icon>
                  <div>
                    <h3>学校地址</h3>
                    <p>{{ university.address }}</p>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>

        <!-- 底部操作按钮 -->
        <div class="action-buttons">
          <el-button type="primary" size="large" v-if="university.website">
            <el-icon><Link /></el-icon>
            访问官网
          </el-button>
          <el-button size="large">
            <el-icon><Star /></el-icon>
            收藏
          </el-button>
          <el-button size="large">
            <el-icon><Share /></el-icon>
            分享
          </el-button>
        </div>
      </div>

      <el-empty v-else-if="!loading" description="大学信息不存在" />
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { 
  ArrowLeft, Trophy, Location, Reading, Star, Document, 
  Check, Link, Message, Phone, Share 
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'UniversityDetailPage',
  components: {
    ArrowLeft, Trophy, Location, Reading, Star, Document,
    Check, Link, Message, Phone, Share
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const loading = ref(false)
    const showBilingual = ref(true)
    const activeTab = ref('intro')
    const university = ref({})

    // 辅助函数：获取标签数组（兼容新旧格式）
    const getTags = (uni) => {
      if (!uni || !uni.tags) return []
      // 如果是数组，直接返回
      if (Array.isArray(uni.tags)) return uni.tags
      // 如果是对象，返回 labels 数组
      if (typeof uni.tags === 'object' && uni.tags.labels) {
        return uni.tags.labels
      }
      return []
    }
    
    // 是否有英文内容
    const hasEnglishContent = computed(() => {
      return !!(university.value.english_name || 
                university.value.description_en || 
                university.value.history_en)
    })

    // 加载大学详情
    const loadUniversity = async () => {
      const id = route.params.id
      if (!id) {
        ElMessage.error('大学ID不存在')
        router.back()
        return
      }

      loading.value = true
      try {
        // axios 的 baseURL 是 /api，这里使用相对路径 /university/:id/
        const res = await axios.get(`/university/${id}/`)
        university.value = res.data || {}
        console.log('加载的大学:', university.value)
      } catch (error) {
        console.error('加载大学失败:', error)
        ElMessage.error('加载大学信息失败')
        setTimeout(() => {
          router.back()
        }, 1500)
      } finally {
        loading.value = false
      }
    }

    // 返回上一页
    const goBack = () => {
      router.back()
    }

    onMounted(() => {
      loadUniversity()
    })

    return {
      loading,
      showBilingual,
      activeTab,
      university,
      hasEnglishContent,
      getTags,
      goBack
    }
  }
}
</script>

<style scoped>
.university-detail-page {
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 20px;
}

.university-header {
  background: #CCFFFF;
  color: #333333;
  border-radius: 16px;
  padding: 40px;
  margin-bottom: 24px;
  color: white;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.header-content {
  display: flex;
  gap: 32px;
  align-items: center;
}

.logo-section {
  flex-shrink: 0;
}

.university-logo {
  width: 120px;
  height: 120px;
  object-fit: contain;
  background: white;
  border-radius: 16px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.info-section {
  flex: 1;
}

.university-name {
  font-size: 42px;
  font-weight: bold;
  margin: 0 0 12px 0;
}

.university-name-en {
  font-size: 24px;
  opacity: 0.9;
  font-style: italic;
  margin: 0 0 20px 0;
}

.meta-info {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.tag-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.detail-tabs {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
}

.content-section {
  margin-bottom: 32px;
}

.content-section h2 {
  font-size: 24px;
  color: #333333;
  margin-bottom: 16px;
  padding-left: 12px;
  border-left: 4px solid #667eea;
}

.description-zh, .advantage-zh, .life-zh {
  font-size: 16px;
  line-height: 1.8;
  color: #333333;
  margin-bottom: 12px;
}

.description-en, .advantage-en, .life-en {
  font-size: 15px;
  line-height: 1.7;
  color: #606266;
  font-style: italic;
  padding: 12px;
  background: #FFFFFF;
  border: 1px solid #CCFFFF;
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.advantages-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.advantage-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: #FFFFFF;
  border: 1px solid #CCFFFF;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.advantage-item:hover {
  background: #FFFFCC;
  transform: translateX(8px);
}

.advantage-number {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  background: #CCFFFF;
  color: #333333;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
}

.advantage-content {
  flex: 1;
}

.major-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
}

.major-card {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.major-card:hover {
  background: #e4e7ed;
  transform: translateY(-2px);
}

.major-card.popular {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border: 2px solid #ff9800;
}

.major-icon {
  font-size: 20px;
  color: #667eea;
}

.requirement-grid, .contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.requirement-item, .contact-item {
  padding: 24px;
  background: #FFFFFF;
  border: 1px solid #CCFFFF;
  border-radius: 12px;
  text-align: center;
}

.req-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.requirement-item h3, .contact-item h3 {
  font-size: 18px;
  color: #333333;
  margin-bottom: 8px;
}

.contact-icon {
  font-size: 32px;
  color: #667eea;
  margin-bottom: 12px;
}

.campus-life-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.life-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  background: #FFFFFF;
  border: 1px solid #CCFFFF;
  border-radius: 8px;
}

.life-icon {
  flex-shrink: 0;
  font-size: 24px;
  color: #67c23a;
}

.life-content {
  flex: 1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.stat-box {
  padding: 24px;
  background: #CCFFFF;
  color: #333333;
  border-radius: 12px;
  text-align: center;
  color: white;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  opacity: 0.9;
}

.action-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  min-width: 160px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }

  .university-name {
    font-size: 32px;
  }

  .major-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
  }
}
</style>
