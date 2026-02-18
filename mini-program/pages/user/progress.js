// pages/user/progress.js
Page({
  data: {
    totalDays: 0,
    totalQuestions: 0,
    accuracy: 0,
    levelProgress: [
      { level: 1, completed: 0, total: 100, percent: 0 },
      { level: 2, completed: 0, total: 150, percent: 0 },
      { level: 3, completed: 0, total: 200, percent: 0 },
      { level: 4, completed: 0, total: 250, percent: 0 },
      { level: 5, completed: 0, total: 200, percent: 0 },
      { level: 6, completed: 0, total: 180, percent: 0 }
    ],
    activities: []
  },

  onLoad() {
    this.loadStatistics()
    this.loadLevelProgress()
    this.loadActivities()
  },

  onShow() {
    this.loadStatistics()
    this.loadLevelProgress()
    this.loadActivities()
  },

  loadStatistics() {
    const app = getApp()
    const token = wx.getStorageSync('token')
    
    if (!token) {
      this.setData({
        totalDays: 0,
        totalQuestions: 0,
        accuracy: 0
      })
      return
    }
    
    // 优先使用后端的学习概览接口
    app.globalData.request({
      url: '/user/progress/overview/',
      method: 'GET'
    }).then(res => {
      this.setData({
        totalDays: res.study_days || 0,
        totalQuestions: res.total_practices || 0,
        accuracy: res.correct_rate || 0
      })
    }).catch(err => {
      console.error('获取学习概览失败:', err)
      this.setData({
        totalDays: 0,
        totalQuestions: 0,
        accuracy: 0
      })
    })
  },

  loadLevelProgress() {
    const app = getApp()
    const token = wx.getStorageSync('token')
    
    if (!token) {
      this.setData({ levelProgress: this.data.levelProgress })
      return
    }
    
    // 先获取答题记录，统计各级别已完成题数
    app.globalData.request({
      url: '/question/answer-records/',
      data: { page_size: 1000 }
    }).then(res => {
      const records = res.results || []
      const completedByLevel = {}
      
      records.forEach(record => {
        const level = record.question?.level
        const qid = record.question?.id
        if (!level || !qid) return
        if (!completedByLevel[level]) completedByLevel[level] = new Set()
        completedByLevel[level].add(qid)
      })
      
      const levelProgress = this.data.levelProgress
      
      // 使用API获取每个等级的总题目数和已完成数
      levelProgress.forEach((level, index) => {
        app.globalData.request({
          url: '/question/questions/',
          data: { level: level.level, page_size: 1 }
        })
          .then((res) => {
            const total = res.count || level.total
            const completed = completedByLevel[level.level]?.size || 0
            const percent = total > 0 ? Math.round((completed / total) * 100) : 0
            
            levelProgress[index] = {
              ...level,
              completed: completed,
              total: total,
              percent: percent
            }
            
            this.setData({ levelProgress })
          })
          .catch(err => {
            console.error(`加载HSK${level.level}级进度失败:`, err)
          })
      })
    }).catch(err => {
      console.error('获取答题记录失败:', err)
      // 出错时不再从本地读取，只保留当前进度为 0
      this.setData({ levelProgress: this.data.levelProgress })
    })
  },

  loadActivities() {
    const app = getApp()
    const token = wx.getStorageSync('token')
    if (!token) {
      this.setData({ activities: [] })
      return
    }

    app.globalData.request({
      url: '/user/progress/activities/',
      method: 'GET'
    }).then(res => {
      const activities = (res || []).map((item, index) => ({
        id: `${item.type || 'activity'}-${index}`,
        icon: item.type === 'exam' ? '📝' : '📌',
        text: item.title || '',
        time: item.time || ''
      }))
      this.setData({ activities })
    }).catch(err => {
      console.error('加载学习活动失败:', err)
      this.setData({ activities: [] })
    })
  },

  formatTime(timestamp) {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = Math.floor((now - date) / 1000 / 60)
    
    if (diff < 1) return '刚刚'
    if (diff < 60) return `${diff}分钟前`
    if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
    return date.toLocaleDateString()
  }
})
