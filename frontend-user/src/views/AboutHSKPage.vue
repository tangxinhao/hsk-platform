<template>
  <div class="about-hsk-page">
    <!-- 顶部横幅 -->
    <div class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">📚</div>
        <h1 class="hero-title">HSK介绍</h1>
        <p class="hero-subtitle">了解汉语水平考试（HSK）</p>
      </div>
      <div class="wave-container">
        <svg class="wave" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z" class="wave-fill"></path>
        </svg>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="container">
      <!-- HSK简介 -->
      <section class="intro-section">
        <div class="section-header">
          <h2>什么是HSK？</h2>
          <div class="header-line"></div>
        </div>
        <div class="intro-content">
          <div class="intro-card">
            <div class="card-icon">🎓</div>
            <h3>官方考试</h3>
            <p>HSK（汉语水平考试）是中国教育部直属的国际汉语教育机构——中国国际中文教育基金会主办的国际汉语能力标准化考试。</p>
          </div>
          <div class="intro-card">
            <div class="card-icon">🌍</div>
            <h3>国际认可</h3>
            <p>HSK证书是外国学生进入中国院校学习的通行证，也是申请来华留学奖学金的必备条件之一。</p>
          </div>
          <div class="intro-card">
            <div class="card-icon">⭐</div>
            <h3>能力标准</h3>
            <p>HSK考试遵循"考教结合"的原则，考试设计与当前国际汉语教学现状、使用教材紧密结合。</p>
          </div>
        </div>
      </section>

      <!-- HSK等级 -->
      <section class="levels-section">
        <div class="section-header">
          <h2>HSK等级体系</h2>
          <div class="header-line"></div>
        </div>
        <div class="levels-grid">
          <div v-for="level in hskLevels" :key="level.level" class="level-card" :class="`level-${level.level}`">
            <div class="level-badge">
              <span class="level-number">{{ level.level }}</span>
            </div>
            <h3 class="level-title">HSK {{ level.level }}级</h3>
            <div class="level-stats">
              <div class="stat-item">
                <div class="stat-label">词汇量</div>
                <div class="stat-value">{{ level.vocabulary }}</div>
              </div>
              <div class="stat-item">
                <div class="stat-label">考试时长</div>
                <div class="stat-value">{{ level.duration }}分钟</div>
              </div>
            </div>
            <div class="level-description">
              <p>{{ level.description }}</p>
            </div>
            <div class="level-content">
              <h4>考试内容：</h4>
              <ul>
                <li v-for="(part, index) in level.parts" :key="index">{{ part }}</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- 考试须知 -->
      <section class="notice-section">
        <div class="section-header">
          <h2>考试须知</h2>
          <div class="header-line"></div>
        </div>
        <div class="notice-grid">
          <div class="notice-card">
            <div class="notice-icon">📝</div>
            <h3>报名方式</h3>
            <ul>
              <li>网上报名：访问官方网站注册账号</li>
              <li>考点报名：前往指定考点现场报名</li>
              <li>提前报名：建议提前1-2个月报名</li>
              <li>准备材料：身份证或护照复印件</li>
            </ul>
          </div>
          <div class="notice-card">
            <div class="notice-icon">📅</div>
            <h3>考试时间</h3>
            <ul>
              <li>每月均有考试安排</li>
              <li>具体日期请查看官方公告</li>
              <li>考试当天提前30分钟到达考场</li>
              <li>迟到15分钟不得入场</li>
            </ul>
          </div>
          <div class="notice-card">
            <div class="notice-icon">💰</div>
            <h3>考试费用</h3>
            <ul>
              <li>HSK 1-3级：约150-200元人民币</li>
              <li>HSK 4-6级：约250-350元人民币</li>
              <li>不同地区费用略有差异</li>
              <li>支持在线支付</li>
            </ul>
          </div>
          <div class="notice-card">
            <div class="notice-icon">📜</div>
            <h3>成绩查询</h3>
            <ul>
              <li>考试后约30天公布成绩</li>
              <li>官网查询或考点领取</li>
              <li>成绩有效期为2年</li>
              <li>可申请成绩复核</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- 学习建议 -->
      <section class="tips-section">
        <div class="section-header">
          <h2>学习建议</h2>
          <div class="header-line"></div>
        </div>
        <div class="tips-content">
          <div class="tip-card">
            <div class="tip-number">1</div>
            <h3>制定学习计划</h3>
            <p>根据自己的汉语水平选择合适的HSK等级，制定长期学习计划，每天保持1-2小时的学习时间。</p>
          </div>
          <div class="tip-card">
            <div class="tip-number">2</div>
            <h3>重视词汇积累</h3>
            <p>词汇是HSK考试的基础，建议使用词卡、APP等工具进行系统化记忆，注重高频词汇的掌握。</p>
          </div>
          <div class="tip-card">
            <div class="tip-number">3</div>
            <h3>加强听力训练</h3>
            <p>每天坚持听力练习，可以通过看中文电视、听中文歌曲、与中国人交流等方式提高听力水平。</p>
          </div>
          <div class="tip-card">
            <div class="tip-number">4</div>
            <h3>多做真题练习</h3>
            <p>熟悉考试题型和时间分配，通过做真题找到自己的薄弱环节，有针对性地进行强化练习。</p>
          </div>
          <div class="tip-card">
            <div class="tip-number">5</div>
            <h3>注重实际应用</h3>
            <p>学以致用，在日常生活中多使用汉语，提高语言的实际运用能力，这也是HSK考试的核心目标。</p>
          </div>
          <div class="tip-card">
            <div class="tip-number">6</div>
            <h3>保持学习热情</h3>
            <p>学习语言是一个长期过程，保持积极的学习态度，设定阶段性目标，及时给自己正向反馈。</p>
          </div>
        </div>
      </section>

      <!-- CTA区域 -->
      <section class="cta-section">
        <div class="cta-card">
          <h2>准备开始HSK学习之旅？</h2>
          <p>立即开始练习，提升您的汉语水平</p>
          <div class="cta-buttons">
            <el-button type="primary" size="large" @click="goToPractice">
              <el-icon><Document /></el-icon>
              开始练习
            </el-button>
            <el-button size="large" @click="goToExam">
              <el-icon><Edit /></el-icon>
              模拟考试
            </el-button>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Document, Edit } from '@element-plus/icons-vue'

export default {
  name: 'AboutHSKPage',
  components: {
    Document,
    Edit
  },
  setup() {
    const router = useRouter()
    
    const hskLevels = ref([
      {
        level: 1,
        vocabulary: '150词',
        duration: 35,
        description: '能理解并使用一些非常简单的汉语词语和句子，满足具体的交际需求。',
        parts: ['听力（第一部分、第二部分）', '阅读（第一部分、第二部分、第三部分、第四部分）']
      },
      {
        level: 2,
        vocabulary: '300词',
        duration: 50,
        description: '能用汉语就熟悉的日常话题进行简单而直接的交流。',
        parts: ['听力（第一部分、第二部分、第三部分、第四部分）', '阅读（第一部分、第二部分、第三部分、第四部分）']
      },
      {
        level: 3,
        vocabulary: '600词',
        duration: 90,
        description: '能用汉语完成生活、学习、工作等方面的基本交际任务。',
        parts: ['听力（第一部分、第二部分）', '阅读（第一部分、第二部分、第三部分）', '书写（第一部分、第二部分）']
      },
      {
        level: 4,
        vocabulary: '1200词',
        duration: 105,
        description: '能用汉语就较广泛领域的话题进行交谈，比较流利地与汉语为母语者进行交流。',
        parts: ['听力（第一部分、第二部分、第三部分）', '阅读（第一部分、第二部分、第三部分）', '书写（第一部分、第二部分）']
      },
      {
        level: 5,
        vocabulary: '2500词',
        duration: 125,
        description: '能阅读汉语报刊杂志，欣赏汉语影视节目，用汉语进行较为完整的演讲。',
        parts: ['听力（第一部分、第二部分）', '阅读（第一部分、第二部分、第三部分）', '书写（作文）']
      },
      {
        level: 6,
        vocabulary: '5000词',
        duration: 140,
        description: '能轻松地理解听到或读到的汉语信息，以口头或书面的形式用汉语流利地表达自己的见解。',
        parts: ['听力（第一部分、第二部分、第三部分）', '阅读（第一部分、第二部分、第三部分、第四部分）', '书写（作文）']
      }
    ])
    
    const goToPractice = () => {
      router.push('/practice')
    }
    
    const goToExam = () => {
      router.push('/exam')
    }
    
    return {
      hskLevels,
      goToPractice,
      goToExam
    }
  }
}
</script>

<style scoped>
.about-hsk-page {
  min-height: 100vh;
  background: #f5f7fa;
}

/* 顶部横幅 */
.hero-section {
  position: relative;
  background: #CCFFFF;
  color: #333333;
  padding: 60px 20px 80px;
  overflow: hidden;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
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
}

.hero-subtitle {
  font-size: 20px;
  color: rgba(255, 255, 255, 0.95);
  margin: 0;
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
  fill: #f5f7fa;
}

/* 容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 通用区块 */
section {
  margin-bottom: 80px;
}

.section-header {
  text-align: center;
  margin-bottom: 50px;
}

.section-header h2 {
  font-size: 36px;
  font-weight: bold;
  color: #333333;
  margin: 0 0 15px 0;
}

.header-line {
  width: 80px;
  height: 4px;
  background: #CCFFFF;
  color: #333333;
  margin: 0 auto;
  border-radius: 2px;
}

/* HSK简介 */
.intro-section {
  padding: 60px 0;
}

.intro-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.intro-card {
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: all 0.3s ease;
}

.intro-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
}

.card-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.intro-card h3 {
  font-size: 24px;
  color: #333333;
  margin: 0 0 15px 0;
}

.intro-card p {
  font-size: 15px;
  color: #606266;
  line-height: 1.8;
  margin: 0;
}

/* HSK等级 */
.levels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
}

.level-card {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.level-card::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 150px;
  height: 150px;
  border-radius: 0 0 0 100%;
  opacity: 0.1;
}

.level-card.level-1::before { background: #CCFFFF; }
.level-card.level-2::before { background: #FFCCCC; }
.level-card.level-3::before { background: #FFFFCC; }
.level-card.level-4::before { background: #43e97b; }
.level-card.level-5::before { background: #fa709a; }
.level-card.level-6::before { background: #feca57; }

.level-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
}

.level-badge {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #CCFFFF;
  color: #333333;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.level-number {
  font-size: 28px;
  font-weight: bold;
  color: white;
}

.level-title {
  font-size: 24px;
  font-weight: bold;
  color: #333333;
  margin: 0 0 20px 0;
}

.level-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.stat-item {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 12px;
  text-align: center;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 18px;
  font-weight: bold;
  color: #667eea;
}

.level-description {
  margin-bottom: 20px;
}

.level-description p {
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
  margin: 0;
}

.level-content h4 {
  font-size: 16px;
  color: #333333;
  margin: 0 0 10px 0;
}

.level-content ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.level-content li {
  font-size: 14px;
  color: #606266;
  padding: 8px 0 8px 24px;
  position: relative;
}

.level-content li::before {
  content: '•';
  position: absolute;
  left: 8px;
  color: #667eea;
  font-weight: bold;
}

/* 考试须知 */
.notice-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 25px;
}

.notice-card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.notice-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
}

.notice-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.notice-card h3 {
  font-size: 20px;
  color: #333333;
  margin: 0 0 15px 0;
}

.notice-card ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notice-card li {
  font-size: 14px;
  color: #606266;
  line-height: 2;
  padding-left: 20px;
  position: relative;
}

.notice-card li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #67c23a;
  font-weight: bold;
}

/* 学习建议 */
.tips-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 30px;
}

.tip-card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
  transition: all 0.3s ease;
}

.tip-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
}

.tip-number {
  position: absolute;
  top: -15px;
  left: 30px;
  width: 40px;
  height: 40px;
  background: #CCFFFF;
  color: #333333;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.tip-card h3 {
  font-size: 20px;
  color: #333333;
  margin: 15px 0 15px 0;
}

.tip-card p {
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
  margin: 0;
}

/* CTA区域 */
.cta-section {
  padding: 60px 0;
}

.cta-card {
  background: #CCFFFF;
  color: #333333;
  padding: 60px 40px;
  border-radius: 24px;
  text-align: center;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
}

.cta-card h2 {
  font-size: 32px;
  color: white;
  margin: 0 0 15px 0;
}

.cta-card p {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 30px 0;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-title {
    font-size: 36px;
  }
  
  .section-header h2 {
    font-size: 28px;
  }
  
  .intro-content,
  .levels-grid,
  .notice-grid,
  .tips-content {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons {
    flex-direction: column;
    align-items: stretch;
  }
}
</style>
