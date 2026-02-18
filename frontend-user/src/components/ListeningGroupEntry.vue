<template>
  <div class="listening-entry-card" @click="goToListening">
    <div class="entry-icon">
      <el-icon :size="48"><Headset /></el-icon>
    </div>
    <div class="entry-content">
      <h3>🎧 听力题组练习</h3>
      <p>专项训练：一段音频，多道题目</p>
      <el-tag type="success">{{ groupCount }}个题组</el-tag>
    </div>
    <div class="entry-arrow">
      <el-icon><ArrowRight /></el-icon>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Headset, ArrowRight } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const groupCount = ref(0)

const loadGroupCount = async () => {
  try {
    axios.defaults.baseURL = '/api'
    const response = await axios.get('/question/listening-groups/')
    groupCount.value = response.data.count || 0
  } catch (error) {
    console.error('加载题组数量失败:', error)
  }
}

const goToListening = () => {
  router.push('/listening-practice')
}

onMounted(() => {
  loadGroupCount()
})
</script>

<style scoped>
.listening-entry-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s;
  color: white;
  margin-bottom: 24px;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.listening-entry-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
}

.entry-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  margin-right: 24px;
}

.entry-content {
  flex: 1;
}

.entry-content h3 {
  font-size: 24px;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.entry-content p {
  margin: 0 0 12px 0;
  font-size: 16px;
  opacity: 0.9;
}

.entry-arrow {
  font-size: 32px;
  opacity: 0.8;
}
</style>
