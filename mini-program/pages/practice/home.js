// pages/practice/home.js
const app = getApp()
const { t, getLang } = require('../../utils/i18n')

Page({
  data: {
    levels: [
      { level: 1, emoji: '🌱', count: 0, progress: 0 },
      { level: 2, emoji: '🌿', count: 0, progress: 0 },
      { level: 3, emoji: '🌳', count: 0, progress: 0 },
      { level: 4, emoji: '🏔️', count: 0, progress: 0 },
      { level: 5, emoji: '🗻', count: 0, progress: 0 },
      { level: 6, emoji: '⛰️', count: 0, progress: 0 }
    ],
    weekStats: {
      questions: 0,
      accuracy: 0,
      time: '0分钟'
    },
    // 国际化文本
    pageTitle: '',
    pageSubtitle: '',
    questionsText: '',
    progressText: '',
    startText: '',
    weekStatsTitle: '',
    practiceCountLabel: '',
    accuracyLabel: '',
    studyTimeLabel: ''
  },

  onLoad() {
    this.updateTexts()
    this.fetchLevelStats()
    this.fetchWeekStats()
  },
  
  // 仅在用户真正要开始练习时检查登录，避免一进入页面就被打断
  ensureLoginBeforePractice(callback) {
    const token = wx.getStorageSync('token')
    if (token) {
      typeof callback === 'function' && callback()
      return
    }

    wx.showModal({
      title: '登录提示',
      content: '登录后可以记录练习进度和错题本，是否前往登录？',
      confirmText: '去登录',
      cancelText: '暂不登录',
      success(res) {
        if (res.confirm) {
          wx.navigateTo({
            url: '/pages/user/login'
          })
        }
      }
    })
  },

  onShow() {
    this.updateTexts()
    // 每次显示时更新统计
    this.fetchLevelStats()
  },
  
  updateTexts() {
    this.setData({
      pageTitle: t('practice.title'),
      pageSubtitle: t('practice.subtitle'),
      questionsText: t('practice.questions'),
      progressText: t('practice.progress') + ': ',
      startText: t('practice.start'),
      weekStatsTitle: t('practice.weekStats'),
      practiceCountLabel: t('practice.practiceCount'),
      accuracyLabel: t('practice.correctRate'),
      studyTimeLabel: t('practice.studyTime')
    })
    
    wx.setNavigationBarTitle({
      title: t('practice.title')
    })
  },
  
  onLanguageChange() {
    this.updateTexts()
  },

  // 获取各等级题目统计
  fetchLevelStats() {
    const { request } = require('../../utils/request')
    const levels = this.data.levels

    // 先获取后端统计的各等级进度
    const app = getApp()
    app.globalData.request({
      url: '/user/progress/level/',
      method: 'GET'
    }).then(levelStats => {
      const progressMap = {}
      if (Array.isArray(levelStats)) {
        levelStats.forEach(item => {
          progressMap[item.level] = item.progress || 0
        })
      }

      // 再为每个等级获取题目总数，并填充进度
      levels.forEach((level, index) => {
        request({
          url: '/question/questions/',
          data: { level: level.level, page_size: 1 }
        })
          .then((res) => {
            const count = res.count || (res.results ? res.results.length : 0)
            levels[index].count = count

            levels[index].progress = progressMap[level.level] || 0
            this.setData({ levels })
          })
          .catch((err) => {
            console.error(`获取HSK${level.level}级题目数失败:`, err)
            levels[index].count = 0
            levels[index].progress = progressMap[level.level] || 0
            this.setData({ levels })
          })
      })
    }).catch(err => {
      console.error('获取等级进度失败:', err)
      // 如果进度接口失败，至少填充题目数量
      levels.forEach((level, index) => {
        request({
          url: '/question/questions/',
          data: { level: level.level, page_size: 1 }
        })
          .then((res) => {
            const count = res.count || (res.results ? res.results.length : 0)
            levels[index].count = count
            levels[index].progress = 0
            this.setData({ levels })
          })
          .catch(e => {
            console.error(`获取HSK${level.level}级题目数失败:`, e)
          })
      })
    })
  },

  // 获取本周学习统计
  fetchWeekStats() {
    const token = wx.getStorageSync('token')
    if (!token) {
      this.setData({
        weekStats: {
          questions: 0,
          accuracy: 0,
          time: getLang() === 'zh' ? '0分钟' : '0 min'
        }
      })
      return
    }

    const app = getApp()
    // 使用学习概览接口近似表示本周统计，确保与其他页面一致
    app.globalData.request({
      url: '/user/progress/overview/',
      method: 'GET'
    }).then(res => {
      const lang = getLang()
      this.setData({
        weekStats: {
          questions: res.total_practices || 0,
          accuracy: res.correct_rate || 0,
          time: lang === 'zh' ? '—' : '--'
        }
      })
    }).catch(err => {
      console.error('获取本周学习统计失败:', err)
      const lang = getLang()
      this.setData({
        weekStats: {
          questions: 0,
          accuracy: 0,
          time: lang === 'zh' ? '0分钟' : '0 min'
        }
      })
    })
  },

  // 选择等级
  selectLevel(e) {
    const level = e.currentTarget.dataset.level

    // 用户点击开始某一级别练习时，再检查登录
    this.ensureLoginBeforePractice(() => {
      wx.navigateTo({
        url: `/pages/practice/list?level=${level}`
      })
    })
  }
})
