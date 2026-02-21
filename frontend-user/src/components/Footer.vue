<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <!-- 左侧 -->
        <div class="footer-left">
          <div class="logo">
            <span class="logo-icon">🎓</span>
            <span>HSK学习平台</span>
          </div>
          <p class="desc">专业的汉语水平考试备考平台</p>
        </div>
        
        <!-- 中间 -->
        <div class="footer-links">
          <div class="link-group">
            <h4>学习资源</h4>
            <router-link to="/practice">题目练习</router-link>
            <router-link to="/exam">模拟考试</router-link>
            <router-link to="/culture">文化学习</router-link>
          </div>
          
          <div class="link-group">
            <h4>关于我们</h4>
            <router-link to="/about-hsk">HSK介绍</router-link>
            <router-link to="/universities">院校推荐</router-link>
            <a href="#">联系我们</a>
          </div>
        </div>
        
        <!-- 右侧 -->
        <div class="footer-right">
          <p>© 2026 HSK学习平台</p>
          <p>All Rights Reserved</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #FFFFFF;
  color: #2C3E50;
  padding: 40px 0 20px;
  margin-top: 80px;
  border-top: 1px solid #E5E7EB;
}

.footer-content {
  display: grid;
  grid-template-columns: 2fr 2fr 1fr;
  gap: 40px;
}

.footer-left .logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

.logo-icon {
  font-size: 28px;
}

.desc {
  color: #64748B;
  font-size: 14px;
}

.footer-links {
  display: flex;
  gap: 60px;
}

.link-group h4 {
  margin-bottom: 15px;
  font-size: 16px;
}

.link-group a {
  display: block;
  color: #64748B;
  text-decoration: none;
  margin-bottom: 10px;
  font-size: 14px;
  transition: color 0.3s;
}

.link-group a:hover {
  color: #6699CC;
  text-decoration: underline;
}

.footer-right {
  text-align: right;
  color: #64748B;
  font-size: 14px;
}

.footer-right p {
  margin-bottom: 5px;
}

@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .footer-links {
    justify-content: center;
  }
  
  .footer-right {
    text-align: center;
  }
}
</style>
