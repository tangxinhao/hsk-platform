<template>
  <div class="home-page">
    <!-- Hero区域 -->
    <section class="hero-section">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text">
            <h1 class="hero-title">
              轻松通过<span class="highlight">HSK考试</span>
            </h1>
            <p class="hero-subtitle">
              专业的中文学习平台，助您快速提升汉语水平
            </p>
            <div class="hero-actions">
              <router-link to="/practice">
                <el-button type="primary" size="large" class="btn-start">
                  <el-icon><Edit /></el-icon>
                  题目练习
                </el-button>
              </router-link>
              <router-link to="/listening-practice">
                <el-button type="warning" size="large" class="btn-listening">
                  <el-icon><Headset /></el-icon>
                  听力题组
                </el-button>
              </router-link>
              <router-link to="/about-hsk">
                <el-button size="large">
                  <el-icon><InfoFilled /></el-icon>
                  了解HSK
                </el-button>
              </router-link>
            </div>
          </div>
          <div class="hero-image">
            <div class="floating-card card-1">
              <el-icon class="card-icon"><Reading /></el-icon>
              <span>1000+ 题目</span>
            </div>
            <div class="floating-card card-2">
              <el-icon class="card-icon"><TrophyBase /></el-icon>
              <span>95% 通过率</span>
            </div>
            <div class="floating-card card-3">
              <el-icon class="card-icon"><User /></el-icon>
              <span>5000+ 学员</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 统计区域 -->
    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-number">1000+</div>
            <div class="stat-label">练习题目</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">50+</div>
            <div class="stat-label">模拟试卷</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">5000+</div>
            <div class="stat-label">活跃学员</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">95%</div>
            <div class="stat-label">考试通过率</div>
          </div>
        </div>
      </div>
    </section>

    <!-- HSK等级 -->
    <section class="levels-section">
      <div class="container">
        <h2 class="section-title">选择您的HSK等级</h2>
        <p class="section-subtitle">从入门到精通，我们为每个等级提供专业的学习资源</p>
        
        <div class="levels-grid">
          <div v-for="level in hskLevels" :key="level.id" class="level-card">
            <div class="level-badge" :style="{background: level.color}">
              HSK{{ level.id }}
            </div>
            <h3>{{ level.name }}</h3>
            <p class="level-vocab">{{ level.vocab }}</p>
            <p class="level-desc">{{ level.desc }}</p>
            <router-link :to="`/practice?level=${level.id}`">
              <el-button type="primary" text>开始学习 →</el-button>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 功能特色 -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">为什么选择我们</h2>
        
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon feature-icon--primary">
              <el-icon><Reading /></el-icon>
            </div>
            <h3>智能题库</h3>
            <p>根据HSK官方题型，精心设计的练习题目</p>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon feature-icon--accent">
              <el-icon><Mic /></el-icon>
            </div>
            <h3>听力训练</h3>
            <p>专业录音，真实还原考试听力环境</p>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon feature-icon--info">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <h3>实时反馈</h3>
            <p>即时显示答题结果，详细的题目解析</p>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon feature-icon--success">
              <el-icon><TrophyBase /></el-icon>
            </div>
            <h3>成就系统</h3>
            <p>完成目标获取勋章，让学习更有动力</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA区域 -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>准备好开始学习了吗？</h2>
          <p>立即注册，开启您的HSK学习之旅</p>
          <router-link to="/register">
            <el-button type="primary" size="large" class="cta-button">
              免费注册
            </el-button>
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Headset } from '@element-plus/icons-vue'

const hskLevels = ref([
  {
    id: 1,
    name: '入门级',
    vocab: '150个词汇',
    desc: '能理解并使用简单的中文词汇和句子',
    color: '#e0ecff'
  },
  {
    id: 2,
    name: '初级',
    vocab: '300个词汇',
    desc: '能用简单的中文进行日常交流',
    color: '#d1e4ff'
  },
  {
    id: 3,
    name: '进阶级',
    vocab: '600个词汇',
    desc: '能用中文完成生活、学习中的基本交流',
    color: '#c7e2ff'
  },
  {
    id: 4,
    name: '中级',
    vocab: '1200个词汇',
    desc: '能用中文讨论较广泛的话题',
    color: '#c0e4f5'
  },
  {
    id: 5,
    name: '高级',
    vocab: '2500个词汇',
    desc: '能阅读中文报刊杂志，欣赏中文影视节目',
    color: '#cde9e5'
  },
  {
    id: 6,
    name: '精通级',
    vocab: '5000+个词汇',
    desc: '能流利地用中文表达自己的见解',
    color: '#e4e0ff'
  }
])
</script>

<style scoped>
.hero-section {
  background: linear-gradient(to bottom, #FFFFCC 0%, #FFFFFF 100%);
  color: #333333;
  padding: 120px 0 80px;
  position: relative;
  overflow: hidden;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 20px;
  line-height: 1.2;
  color: #333333;
}

.highlight {
  color: #FFCCCC;
}

.hero-subtitle {
  font-size: 20px;
  margin-bottom: 40px;
  color: #666666;
  font-weight: 400;
}

.hero-actions {
  display: flex;
  gap: 20px;
}

.btn-start {
  background: #CCFFFF;
  color: #333333;
  border: 2px solid #CCFFFF;
  padding: 12px 40px;
  font-size: 18px;
  box-shadow: 0 4px 12px rgba(204, 255, 255, 0.4);
}

.btn-start:hover {
  background: #99EEFF;
  border-color: #99EEFF;
  box-shadow: 0 6px 16px rgba(204, 255, 255, 0.6);
}

/* 浮动卡片 */
.hero-image {
  position: relative;
  height: 400px;
}

.floating-card {
  position: absolute;
  background: #FFFFFF;
  padding: 20px 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(204, 255, 255, 0.4);
  border: 2px solid #CCFFFF;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #333333;
  font-weight: 500;
  animation: float 3s ease-in-out infinite;
}

.card-icon {
  font-size: 32px;
  color: #FFCCCC;
}

.card-1 {
  top: 50px;
  left: 50px;
}

.card-2 {
  top: 150px;
  right: 80px;
  animation-delay: 1s;
}

.card-3 {
  bottom: 80px;
  left: 100px;
  animation-delay: 2s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 统计区域 */
.stats-section {
  background: #FFFFFF;
  padding: 60px 0;
  margin-top: -40px;
  border-radius: 20px;
  box-shadow: 0 -10px 40px rgba(204, 255, 255, 0.3);
  border: 2px solid #CCFFFF;
  position: relative;
  z-index: 1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  text-align: center;
}

.stat-number {
  font-size: 48px;
  font-weight: 700;
  color: #FFCCCC;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 16px;
  color: #666666;
  font-weight: 500;
}

/* HSK等级 */
.levels-section {
  padding: 80px 0;
}

.section-title {
  text-align: center;
  font-size: 36px;
  font-weight: 700;
  color: #333333;
  margin-bottom: 15px;
}

.section-subtitle {
  text-align: center;
  font-size: 18px;
  color: #666666;
  margin-bottom: 50px;
  font-weight: 400;
}

.levels-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.level-card {
  background: #FFFFFF;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(204, 255, 255, 0.3);
  border: 2px solid #CCFFFF;
  text-align: center;
  transition: all 0.2s ease;
  cursor: pointer;
}

.level-card:hover {
  box-shadow: 0 4px 16px rgba(204, 255, 255, 0.5);
  border-color: #99EEFF;
  transform: translateY(-4px);
}

.level-badge {
  display: inline-block;
  padding: 10px 25px;
  border-radius: 25px;
  color: #333333;
  background: #CCFFFF;
  font-weight: 700;
  font-size: 18px;
  margin-bottom: 20px;
}

.level-vocab {
  color: #666666;
  margin: 15px 0;
  font-weight: 500;
}

.level-desc {
  color: #999999;
  font-size: 14px;
  margin-bottom: 20px;
}

/* 功能特色 */
.features-section {
  padding: 80px 0;
  background: #FFFFCC;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
}

.feature-item {
  background: #FFFFFF;
  padding: 40px 30px;
  border-radius: 12px;
  border: 2px solid #CCFFFF;
  text-align: center;
  transition: all 0.2s ease;
}

.feature-item:hover {
  box-shadow: 0 4px 16px rgba(204, 255, 255, 0.5);
  border-color: #99EEFF;
  transform: translateY(-4px);
}

.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  font-size: 36px;
  color: white;
}

.feature-icon--primary {
  background: #CCFFFF;
  color: #333333;
  }
  
  .feature-icon--accent {
    background: #FFCCCC;
    color: #333333;
  }
  
  .feature-icon--info {
    background: #FFFFCC;
    color: #333333;
  }
  
  .feature-icon--success {
    background: #CCFFFF;
    color: #333333;
  }

.feature-item h3 {
  font-size: 20px;
  margin-bottom: 12px;
}

.feature-item p {
  color: #666666;
  font-size: 14px;
  line-height: 1.6;
}

/* CTA区域 */
.cta-section {
  padding: 100px 0;
  background: linear-gradient(to bottom, #CCFFFF 0%, #99EEFF 100%);
  color: #333333;
  text-align: center;
}

.cta-content h2 {
  font-size: 42px;
  margin-bottom: 15px;
}

.cta-content p {
  font-size: 20px;
  margin-bottom: 40px;
  opacity: 0.9;
}

.cta-button {
  background: #FFFFFF;
  color: #333333;
  border: 2px solid #FFFFFF;
  padding: 15px 50px;
  font-size: 18px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.cta-button:hover {
  background: #FFFFCC;
  border-color: #FFFFCC;
  box-shadow: 0 4px 12px rgba(255, 255, 204, 0.5);
}

/* 响应式 */
@media (max-width: 1024px) {
  .hero-content {
    grid-template-columns: 1fr;
  }
  
  .hero-image {
    display: none;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .levels-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .levels-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>
