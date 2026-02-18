// pages/index/index.js
const app = getApp()
const { t, getLang } = require('../../utils/i18n')

Page({
  data: {
    userInfo: null,
    todayProgress: 0,
    completedQuestions: 0,
    totalQuestions: 20,
    totalStudyDays: 0,
    accuracy: 0,
    currentLang: 'zh',
    // 国际化文本
    greeting: '',
    studyTip: '',
    todayStudyText: '',
    completedText: '',
    questionsText: '',
    continuePracticeText: '',
    mockExamText: '',
    wrongBookText: '',
    studyProgressText: '',
    studyStatsText: '',
    studyDaysText: '',
    totalQuestionsText: '',
    accuracyText: '',
    hskLevelText: ''
  },

  onLoad() {
    this.updateTexts()
    this.loadUserInfo()
    this.loadTodayProgress()
    this.loadStatistics()
  },

  onShow() {
    this.updateTexts()
    this.loadUserInfo()
    this.loadTodayProgress()
  },
  
  updateTexts() {
    const lang = getLang()
    this.setData({
      currentLang: lang,
      greeting: t('home.welcome'),
      studyTip: lang === 'zh' ? '今天也要加油哦 💪' : 'Keep going! 💪',
      todayStudyText: t('home.todayProgress'),
      completedText: t('home.completed'),
      questionsText: t('home.questions'),
      continuePracticeText: t('home.continuePractice'),
      mockExamText: t('home.mockExam'),
      wrongBookText: t('home.wrongBook'),
      studyProgressText: t('home.studyProgress'),
      studyStatsText: t('home.studyStats'),
      studyDaysText: t('home.studyDays'),
      totalQuestionsText: t('home.totalQuestions'),
      accuracyText: t('home.accuracy'),
      hskLevelText: t('home.hskLevel')
    })
    
    wx.setNavigationBarTitle({
      title: t('app.name')
    })
  },
  
  onLanguageChange() {
    this.updateTexts()
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = wx.getStorageSync('userInfo')
    this.setData({ userInfo })
  },

  // 加载今日进度
  loadTodayProgress() {
    const token = wx.getStorageSync('token')
    if (!token) {
      this.setData({
        todayProgress: 0,
        completedQuestions: 0,
        totalQuestions: 20
      })
      return
    }

    const app = getApp()

    // 使用后端学习趋势接口，获取今天已完成题目数量
    app.globalData.request({
      url: '/user/progress/trend/',
      method: 'GET',
      data: { days: 1 }
    }).then(res => {
      const list = Array.isArray(res) ? res : []
      const todayCount = list.length > 0 ? (list[0].count || 0) : 0
      const total = 20  // 目标每日练习题数，可以后续做成可配置
      const percent = total > 0 ? Math.min(100, Math.round(todayCount / total * 100)) : 0

      this.setData({
        todayProgress: percent,
        completedQuestions: todayCount,
        totalQuestions: total
      })
    }).catch(err => {
      console.error('加载今日进度失败:', err)
      this.setData({
        todayProgress: 0,
        completedQuestions: 0,
        totalQuestions: 20
      })
    })
  },

  // 加载统计数据
  loadStatistics() {
    const token = wx.getStorageSync('token')
    if (!token) {
      this.setData({
        totalStudyDays: 0,
        totalQuestions: 0,
        accuracy: 0
      })
      return
    }

    const app = getApp()

    // 使用与用户页面一致的学习概览接口
    app.globalData.request({
      url: '/user/progress/overview/',
      method: 'GET'
    }).then(res => {
      this.setData({
        totalStudyDays: res.study_days || 0,
        totalQuestions: res.total_practices || 0,
        accuracy: res.correct_rate || 0
      })
    }).catch(err => {
      console.error('加载学习统计失败:', err)
      this.setData({
        totalStudyDays: 0,
        totalQuestions: 0,
        accuracy: 0
      })
    })
  },

  // 快速入口
  gotoPractice() {
    wx.switchTab({ url: '/pages/practice/home' })
  },

  gotoExam() {
    wx.navigateTo({ url: '/pages/exam/home' })
  },

  gotoWrongBook() {
    wx.navigateTo({ url: '/pages/user/wrong' })
  },

  gotoProgress() {
    wx.navigateTo({ url: '/pages/user/progress' })
  },

  // 选择等级
  selectLevel(e) {
    const level = e.currentTarget.dataset.level
    wx.navigateTo({
      url: `/pages/practice/list?level=${level}`
    })
  },

  // 分享
  onShareAppMessage() {
    return {
      title: 'HSK学习助手 - 一起学习HSK吧！',
      path: '/pages/index/index'
    }
  }
})
