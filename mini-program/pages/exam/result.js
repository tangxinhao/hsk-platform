// pages/exam/result.js
Page({
  data: {
    result: {},
    scoreEmoji: '🎉'
  },

  onLoad(options) {
    const id = options.id
    this.loadResult(id)
  },

  loadResult(id) {
    const history = wx.getStorageSync('examHistory') || []
    const result = history.find(r => r.id == id)
    
    if (result) {
      let emoji = '🎉'
      if (result.score >= 90) emoji = '🏆'
      else if (result.score >= 80) emoji = '🎖️'
      else if (result.score >= 60) emoji = '✨'
      else emoji = '💪'
      
      this.setData({
        result: result,
        scoreEmoji: emoji
      })
    } else {
      wx.showToast({
        title: '未找到考试记录',
        icon: 'none'
      })
    }
  },

  backHome() {
    wx.switchTab({
      url: '/pages/index/index'
    })
  },

  retryExam() {
    const { result } = this.data
    wx.redirectTo({
      url: `/pages/exam/exam?level=${result.level}`
    })
  }
})
