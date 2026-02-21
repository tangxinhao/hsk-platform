<template>
  <div id="app">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 
               'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
  background: #F8F9FA;
  color: #2C3E50;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 60px; /* 为固定导航栏留空间 */
}

/* 通用容器 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 通用按钮 */
.btn-primary {
  background: #6699CC;
  color: #FFFFFF;
  border: none;
  padding: 12px 30px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(102, 153, 204, 0.3);
}

.btn-primary:hover {
  background: #5A8AB8;
  box-shadow: 0 4px 12px rgba(102, 153, 204, 0.4);
  transform: translateY(-1px);
}

/* 卡片样式 */
.card {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border: 1px solid #E5E7EB;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  border-color: #D1D5DB;
  transform: translateY(-2px);
}
</style>
