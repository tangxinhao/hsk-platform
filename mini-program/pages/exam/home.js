// pages/exam/home.js
const { t, getLang } = require('../../utils/i18n')

Page({
  data: {
    currentLang: 'zh',
    pageTitle: '',
    pageSubtitle: '',
    levelSuffix: '',
    scoreSuffix: '',
    startExamText: '',
    historyTitle: '',
    exams: [
      {
        level: 1,
        emoji: '🌱',
        totalQuestions: 40,
        duration: 40,
        totalScore: 100,
        parts: {
          zh: ['听力20题', '阅读20题'],
          en: ['Listening 20', 'Reading 20']
        }
      },
      {
        level: 2,
        emoji: '🌿',
        totalQuestions: 60,
        duration: 55,
        totalScore: 100,
        parts: {
          zh: ['听力35题', '阅读25题'],
          en: ['Listening 35', 'Reading 25']
        }
      },
      {
        level: 3,
        emoji: '🌳',
        totalQuestions: 80,
        duration: 90,
        totalScore: 100,
        parts: {
          zh: ['听力40题', '阅读30题', '书写10题'],
          en: ['Listening 40', 'Reading 30', 'Writing 10']
        }
      },
      {
        level: 4,
        emoji: '🏔️',
        totalQuestions: 100,
        duration: 105,
        totalScore: 100,
        parts: {
          zh: ['听力45题', '阅读40题', '书写15题'],
          en: ['Listening 45', 'Reading 40', 'Writing 15']
        }
      },
      {
        level: 5,
        emoji: '🗻',
        totalQuestions: 100,
        duration: 125,
        totalScore: 100,
        parts: {
          zh: ['听力45题', '阅读45题', '书写10题'],
          en: ['Listening 45', 'Reading 45', 'Writing 10']
        }
      },
      {
        level: 6,
        emoji: '⛰️',
        totalQuestions: 101,
        duration: 140,
        totalScore: 100,
        parts: {
          zh: ['听力50题', '阅读50题', '书写1题'],
          en: ['Listening 50', 'Reading 50', 'Writing 1']
        }
      }
    ],
    history: []
  },

  onLoad() {
    this.updateTexts()
    this.loadHistory()
  },
  
  // 仅在用户真正要开始考试或查看考试结果时检查登录
  ensureLoginForExam(callback) {
    const token = wx.getStorageSync('token')
    if (token) {
      typeof callback === 'function' && callback()
      return
    }

    wx.showModal({
      title: '登录提示',
      content: '登录后可以保存考试记录和成绩，是否前往登录？',
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
  },
  
  updateTexts() {
    const lang = getLang()
    const examsWithText = this.data.exams.map(exam => ({
      ...exam,
      questionsText: t('exam.totalQuestions', { count: exam.totalQuestions }),
      durationText: t('exam.duration', { time: exam.duration }),
      scoreText: t('exam.totalScore', { score: exam.totalScore }),
      displayParts: exam.parts[lang]
    }))
    
    this.setData({
      currentLang: lang,
      pageTitle: t('exam.title'),
      pageSubtitle: t('exam.subtitle'),
      levelSuffix: lang === 'zh' ? '级' : '',
      scoreSuffix: t('exam.score'),
      startExamText: t('exam.start'),
      historyTitle: t('exam.history'),
      exams: examsWithText
    })
    
    wx.setNavigationBarTitle({
      title: t('exam.title')
    })
  },
  
  onLanguageChange() {
    this.updateTexts()
  },

  onShow() {
    this.loadHistory()
  },

  loadHistory() {
    const history = wx.getStorageSync('examHistory') || []
    this.setData({
      history: history.slice(0, 5)
    })
  },

  startExam(e) {
    const level = e.currentTarget.dataset.level

    // 用户点击“开始考试”时再检查登录
    this.ensureLoginForExam(() => {
      wx.showModal({
        title: '开始考试',
        content: `确定开始HSK ${level}级模拟考试吗？考试期间请保持专注。`,
        confirmText: '开始',
        cancelText: '取消',
        success: (res) => {
          if (res.confirm) {
            wx.navigateTo({
              url: `/pages/exam/exam?level=${level}`
            })
          }
        }
      })
    })
  },

  viewResult(e) {
    const id = e.currentTarget.dataset.id

    // 查看考试结果也需要登录
    this.ensureLoginForExam(() => {
      wx.navigateTo({
        url: `/pages/exam/result?id=${id}`
      })
    })
  }
})
