<template>
  <div class="universities-page">
    <!-- 顶部横幅区域 -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">🎓</div>
        <h1 class="hero-title">中国院校推荐</h1>
        <p class="hero-subtitle">为您推荐最适合的中国大学</p>
        
        <!-- 筛选栏 -->
        <div class="filter-bar">
          <div class="filter-wrapper">
            <el-select 
              v-model="filters.region" 
              placeholder="选择地区" 
              clearable 
              @change="handleFilterChange"
              size="large"
              class="filter-select"
            >
              <el-option label="全部地区" value=""></el-option>
              <el-option label="华北" value="华北"></el-option>
              <el-option label="华东" value="华东"></el-option>
              <el-option label="华南" value="华南"></el-option>
              <el-option label="华中" value="华中"></el-option>
              <el-option label="西南" value="西南"></el-option>
              <el-option label="西北" value="西北"></el-option>
              <el-option label="东北" value="东北"></el-option>
            </el-select>
            
            <el-select 
              v-model="filters.city" 
              placeholder="选择城市" 
              clearable 
              @change="handleFilterChange"
              size="large"
              class="filter-select"
            >
              <el-option label="全部城市" value=""></el-option>
              <el-option label="北京" value="北京市"></el-option>
              <el-option label="上海" value="上海市"></el-option>
              <el-option label="广州" value="广州市"></el-option>
              <el-option label="深圳" value="深圳市"></el-option>
              <el-option label="杭州" value="杭州市"></el-option>
              <el-option label="成都" value="成都市"></el-option>
              <el-option label="重庆" value="重庆市"></el-option>
              <el-option label="武汉" value="武汉市"></el-option>
              <el-option label="西安" value="西安市"></el-option>
              <el-option label="南京" value="南京市"></el-option>
            </el-select>
            
            <el-select 
              v-model="filters.hsk_level" 
              placeholder="HSK等级" 
              clearable 
              @change="handleFilterChange"
              size="large"
              class="filter-select"
            >
              <el-option label="全部等级" value=""></el-option>
              <el-option label="HSK 1" :value="1"></el-option>
              <el-option label="HSK 2" :value="2"></el-option>
              <el-option label="HSK 3" :value="3"></el-option>
              <el-option label="HSK 4" :value="4"></el-option>
              <el-option label="HSK 5" :value="5"></el-option>
              <el-option label="HSK 6" :value="6"></el-option>
            </el-select>
            
            <el-input
              v-model="filters.search"
              placeholder="搜索大学名称"
              clearable
              @input="handleFilterChange"
              size="large"
              class="filter-input"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
          </div>
        </div>
      </div>
      
      <!-- 装饰性波浪 -->
      <div class="wave-container">
        <svg class="wave" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" class="wave-fill"></path>
        </svg>
      </div>
    </div>
    
    <!-- 统计信息栏 -->
    <div class="stats-section" v-if="!loading && filteredUniversities.length > 0">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">🏛️</div>
            <div class="stat-content">
              <div class="stat-number">{{ filteredUniversities.length }}</div>
              <div class="stat-label">推荐院校</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">📍</div>
            <div class="stat-content">
              <div class="stat-number">{{ uniqueCities.length }}</div>
              <div class="stat-label">覆盖城市</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">⭐</div>
            <div class="stat-content">
              <div class="stat-number">{{ topUniversities }}</div>
              <div class="stat-label">985/211院校</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 大学列表 -->
    <div class="container">
      <div v-loading="loading" class="university-list">
        <!-- 空状态 -->
        <div v-if="filteredUniversities.length === 0 && !loading" class="empty-state">
          <div class="empty-icon">🔍</div>
          <h3>未找到符合条件的大学</h3>
          <p>试试调整筛选条件或清除所有筛选</p>
          <el-button type="primary" @click="clearFilters" size="large">清除筛选条件</el-button>
        </div>
        
        <!-- 大学卡片网格 -->
        <div v-else class="university-grid">
          <div
            v-for="(university, index) in paginatedUniversities"
            :key="university.id"
            class="university-card"
            :style="{ animationDelay: `${index * 0.1}s` }"
            @click="viewDetail(university)"
          >
            <!-- 卡片背景装饰 -->
            <div class="card-bg-decoration"></div>
            
            <!-- 卡片头部 -->
            <div class="card-header">
              <div class="university-logo-wrapper">
                <div class="logo-circle">
                  <img v-if="university.logo_url" :src="university.logo_url" :alt="university.name" />
                  <div v-else class="logo-placeholder">
                    <span>{{ university.name.charAt(0) }}</span>
                  </div>
                </div>
                <div class="logo-glow"></div>
              </div>
              
              <div class="ranking-badge" v-if="university.ranking">
                <div class="ranking-icon">🏆</div>
                <div class="ranking-text">
                  <span class="ranking-label">综合排名</span>
                  <strong class="ranking-number">#{{ university.ranking }}</strong>
                </div>
              </div>
            </div>
            
            <!-- 卡片主体 -->
            <div class="card-body">
              <h3 class="university-name">{{ university.name }}</h3>
              <p class="university-english-name" v-if="university.english_name">
                {{ university.english_name }}
              </p>
              
              <!-- 元信息 -->
              <div class="university-meta">
                <div class="meta-item">
                  <el-icon class="meta-icon"><Location /></el-icon>
                  <span>{{ university.region }} · {{ university.city }}</span>
                </div>
                <div class="meta-item">
                  <el-icon class="meta-icon"><Document /></el-icon>
                  <span>HSK {{ university.min_hsk_level }}级及以上</span>
                </div>
              </div>
              
              <!-- 描述 -->
              <div class="university-description">
                <p>{{ getDescription(university) }}</p>
              </div>
              
              <!-- 标签 -->
              <div class="tags-wrapper" v-if="getTags(university).length > 0">
                <el-tag
                  v-for="(tag, tagIndex) in getTags(university).slice(0, 3)"
                  :key="tagIndex"
                  size="small"
                  :type="getTagType(tagIndex)"
                  effect="plain"
                  round
                >
                  {{ tag }}
                </el-tag>
              </div>
            </div>
            
            <!-- 卡片底部 -->
            <div class="card-footer">
              <div class="footer-info">
                <div class="tuition-info" v-if="university.tuition_fee">
                  <span class="tuition-label">学费</span>
                  <span class="tuition-value">¥{{ formatNumber(university.tuition_fee) }}</span>
                  <span class="tuition-unit">/年</span>
                </div>
                <div class="tuition-info" v-else>
                  <span class="tuition-label">学费</span>
                  <span class="tuition-value">咨询</span>
                </div>
              </div>
              
              <el-button 
                type="primary" 
                size="default"
                @click.stop="viewDetail(university)"
                class="detail-btn"
              >
                <span>查看详情</span>
                <el-icon class="btn-icon"><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="filteredUniversities.length > 0">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="filteredUniversities.length"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
          background
          hide-on-single-page
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Location, Document, ArrowRight } from '@element-plus/icons-vue'
import apiClient from '../api/index.js'

export default {
  name: 'UniversitiesPage',
  components: {
    Search,
    Location,
    Document,
    ArrowRight
  },
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const universities = ref([])
    const currentPage = ref(1)
    const pageSize = ref(9)
    
    const filters = ref({
      region: '',
      city: '',
      hsk_level: '',
      search: ''
    })
    
    // 辅助函数：获取标签数组（兼容新旧格式）
    const getTags = (university) => {
      if (!university.tags) return []
      // 如果是数组，直接返回
      if (Array.isArray(university.tags)) return university.tags
      // 如果是对象，返回 labels 数组
      if (typeof university.tags === 'object' && university.tags.labels) {
        return university.tags.labels
      }
      return []
    }
    
    // 获取大学列表
    const fetchUniversities = async () => {
      loading.value = true
      try {
        const response = await apiClient.get('/university/')
        universities.value = Array.isArray(response.data) ? response.data : (response.data.results || [])
        console.log('获取到的大学数据：', universities.value)
      } catch (error) {
        console.error('获取大学列表失败:', error)
        ElMessage.error('获取大学列表失败，请检查网络连接')
      } finally {
        loading.value = false
      }
    }
    
    // 过滤后的大学列表
    const filteredUniversities = computed(() => {
      let result = universities.value
      
      if (filters.value.region && filters.value.region !== '') {
        result = result.filter(u => u.region === filters.value.region)
      }
      
      if (filters.value.city && filters.value.city !== '') {
        result = result.filter(u => u.city === filters.value.city)
      }
      
      if (filters.value.hsk_level && filters.value.hsk_level !== '') {
        result = result.filter(u => u.min_hsk_level && u.min_hsk_level <= filters.value.hsk_level)
      }
      
      if (filters.value.search && filters.value.search !== '') {
        const searchLower = filters.value.search.toLowerCase()
        result = result.filter(u => 
          (u.name && u.name.toLowerCase().includes(searchLower)) ||
          (u.english_name && u.english_name.toLowerCase().includes(searchLower))
        )
      }
      
      return result
    })
    
    // 分页后的大学列表
    const paginatedUniversities = computed(() => {
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      return filteredUniversities.value.slice(start, end)
    })
    
    // 统计信息
    const uniqueCities = computed(() => {
      const cities = new Set(filteredUniversities.value.map(u => u.city).filter(c => c))
      return Array.from(cities)
    })
    
    const topUniversities = computed(() => {
      return filteredUniversities.value.filter(u => 
        u.is985 || u.is211
      ).length
    })
    
    // 处理筛选变化
    const handleFilterChange = () => {
      currentPage.value = 1
    }
    
    // 清除筛选
    const clearFilters = () => {
      filters.value = {
        region: '',
        city: '',
        hsk_level: '',
        search: ''
      }
    }
    
    // 处理分页
    const handlePageChange = (page) => {
      currentPage.value = page
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
    
    // 查看详情
    const viewDetail = (university) => {
      router.push({
        name: 'UniversityDetail',
        params: { id: university.id }
      })
    }
    
    // 格式化数字
    const formatNumber = (num) => {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    }
    
    // 获取描述
    const getDescription = (university) => {
      if (university.description) {
        return university.description.length > 65
          ? university.description.substring(0, 65) + '...' 
          : university.description
      }
      return '暂无描述'
    }
    
    // 获取标签类型
    const getTagType = (index) => {
      const types = ['primary', 'success', 'warning', 'danger', 'info']
      return types[index % types.length]
    }
    
    onMounted(() => {
      fetchUniversities()
    })
    
    return {
      loading,
      universities,
      filteredUniversities,
      paginatedUniversities,
      getTags,
      currentPage,
      pageSize,
      filters,
      uniqueCities,
      topUniversities,
      handleFilterChange,
      clearFilters,
      handlePageChange,
      viewDetail,
      formatNumber,
      getDescription,
      getTagType
    }
  }
}
</script>

<style scoped>
.universities-page {
  min-height: 100vh;
  background: linear-gradient(to bottom, #f8f9fc 0%, #ffffff 100%);
}

/* 顶部横幅 */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  padding: 60px 20px 80px;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255,255,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255,255,255,0.1) 0%, transparent 50%);
  animation: float 15s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.hero-content {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  z-index: 1;
}

.hero-icon {
  font-size: 64px;
  margin-bottom: 20px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.hero-title {
  font-size: 48px;
  font-weight: 800;
  color: white;
  margin: 0 0 15px 0;
  text-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  letter-spacing: 2px;
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.95);
  margin: 0 0 40px 0;
  font-weight: 300;
}

.filter-bar {
  margin-top: 40px;
}

.filter-wrapper {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.filter-select,
.filter-input {
  min-width: 200px;
  flex: 1 1 auto;
  max-width: 280px;
}

:deep(.filter-select .el-input__wrapper),
:deep(.filter-input .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.95);
  border: 2px solid transparent;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

:deep(.filter-select .el-input__wrapper:hover),
:deep(.filter-input .el-input__wrapper:hover) {
  border-color: white;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.wave-container {
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
}

.wave {
  position: relative;
  display: block;
  width: calc(100% + 1.3px);
  height: 40px;
}

.wave-fill {
  fill: #f8f9fc;
}

/* 统计信息栏 */
.stats-section {
  margin-top: -30px;
  margin-bottom: 40px;
  position: relative;
  z-index: 10;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.stat-item {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: default;
}

.stat-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  font-size: 40px;
  line-height: 1;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

/* 容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 大学列表 */
.university-list {
  min-height: 400px;
  padding: 20px 0;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-state h3 {
  font-size: 24px;
  color: #303133;
  margin: 0 0 10px 0;
}

.empty-state p {
  font-size: 16px;
  color: #909399;
  margin: 0 0 30px 0;
}

/* 大学卡片网格 */
.university-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

/* 大学卡片 */
.university-card {
  position: relative;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  animation: fadeInUp 0.6s ease-out backwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.university-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
}

.university-card:hover .card-bg-decoration {
  opacity: 1;
}

.card-bg-decoration {
  position: absolute;
  top: 0;
  right: 0;
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-radius: 0 0 0 100%;
  opacity: 0;
  transition: opacity 0.4s ease;
}

/* 卡片头部 */
.card-header {
  position: relative;
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.card-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.1) 0%, transparent 60%);
}

.university-logo-wrapper {
  position: relative;
  z-index: 2;
}

.logo-circle {
  position: relative;
  width: 80px;
  height: 80px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.university-card:hover .logo-circle {
  transform: scale(1.1);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
}

.logo-circle img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 10px;
}

.logo-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-placeholder span {
  font-size: 36px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.university-card:hover .logo-glow {
  opacity: 1;
}

.ranking-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(255, 255, 255, 0.98);
  padding: 6px 14px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 2;
}

.ranking-icon {
  font-size: 18px;
  line-height: 1;
}

.ranking-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.ranking-label {
  font-size: 9px;
  color: #909399;
  line-height: 1;
  margin-bottom: 2px;
}

.ranking-number {
  font-size: 16px;
  font-weight: bold;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
}

/* 卡片主体 */
.card-body {
  padding: 18px 20px;
}

.university-name {
  font-size: 19px;
  font-weight: bold;
  color: #303133;
  margin: 0 0 8px 0;
  text-align: center;
  line-height: 1.3;
}

.university-english-name {
  font-size: 13px;
  color: #909399;
  text-align: center;
  margin: 0 0 12px 0;
  font-style: italic;
}

.university-meta {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #606266;
  font-size: 13px;
  padding: 5px 10px;
  background: #f5f7fa;
  border-radius: 8px;
}

.meta-icon {
  color: #667eea;
  font-size: 16px;
}

.university-description {
  margin: 12px 0;
  min-height: 48px;
}

.university-description p {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  margin: 0;
  text-align: justify;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tags-wrapper {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 12px;
}

/* 卡片底部 */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-top: 1px solid #f0f0f0;
  background: linear-gradient(to bottom, #fafbfc 0%, #ffffff 100%);
}

.footer-info {
  flex: 1;
}

.tuition-info {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.tuition-label {
  font-size: 12px;
  color: #909399;
}

.tuition-value {
  font-size: 18px;
  font-weight: bold;
  color: #f56c6c;
}

.tuition-unit {
  font-size: 12px;
  color: #909399;
}

.detail-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  border-radius: 20px;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.3s ease;
}

.detail-btn:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-icon {
  transition: transform 0.3s ease;
}

.detail-btn:hover .btn-icon {
  transform: translateX(4px);
}

/* 分页 */
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 40px 0 60px;
}

:deep(.el-pagination) {
  gap: 8px;
}

:deep(.el-pager li) {
  border-radius: 8px;
  transition: all 0.3s ease;
}

:deep(.el-pager li:hover) {
  transform: translateY(-2px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
  
  .hero-subtitle {
    font-size: 16px;
  }
  
  .filter-wrapper {
    flex-direction: column;
  }
  
  .filter-select,
  .filter-input {
    width: 100%;
    max-width: 100%;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .university-grid {
    grid-template-columns: 1fr;
  }
  
  .card-footer {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .detail-btn {
    width: 100%;
    justify-content: center;
  }
}

/* 加载动画优化 */
:deep(.el-loading-mask) {
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
}
</style>
