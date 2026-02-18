// pages/user/user.js
const app = getApp()
const { t, getLang } = require('../../utils/i18n')

Page({
  data: {
    userInfo: null,
    hasUserInfo: false,
    studyStats: {
      totalDays: 0,
      totalQuestions: 0,
      correctRate: 0
    },
    wrongCount: 0,
    favoriteCount: 0,
    currentLang: 'zh',
    // 国际化文本
    notLoginText: '',
    loginTipText: '',
    loginText: '',
    logoutText: '',
    studyDaysText: '',
    completedQuestionsText: '',
    correctRateText: '',
    studyRecordText: '',
    progressText: '',
    wrongBookText: '',
    favoritesText: '',
    examRecordText: '',
    examHistoryText: '',
    versionText: ''
  },

  onLoad() {
    this.updateTexts()
    this.loadUserInfo()
    this.loadStatistics()
  },

  onShow() {
    this.updateTexts()
    // 每次显示时刷新数据
    this.loadUserInfo()
    this.loadStatistics()
  },
  
  updateTexts() {
    this.setData({
      currentLang: getLang(),
      notLoginText: t('user.notLogin'),
      loginTipText: t('user.loginTip'),
      loginText: t('user.login'),
      logoutText: t('user.logout'),
      studyDaysText: t('user.studyDays'),
      completedQuestionsText: t('user.completedQuestions'),
      correctRateText: t('user.correctRate'),
      studyRecordText: t('user.studyRecord'),
      progressText: t('user.progress'),
      wrongBookText: t('user.wrongBook'),
      favoritesText: t('user.favorites'),
      examRecordText: t('user.examRecord'),
      examHistoryText: t('user.examHistory'),
      versionText: t('user.version')
    })
    
    wx.setNavigationBarTitle({
      title: t('user.title')
    })
  },
  
  onLanguageChange() {
    this.updateTexts()
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = wx.getStorageSync('userInfo')
    const token = wx.getStorageSync('token')
    
    this.setData({
      userInfo: userInfo,
      hasUserInfo: !!(userInfo && token)
    })
  },

  // 加载真实统计数据
  loadStatistics() {
    const token = wx.getStorageSync('token')
    if (!token) {
      // 未登录时显示 0
      this.setData({
        studyStats: {
          totalDays: 0,
          totalQuestions: 0,
          correctRate: 0
        },
        wrongCount: 0,
        favoriteCount: 0
      })
      return
    }

    const app = getApp()

    // 1. 学习概览：总练习数、正确率、学习天数、错题数
    app.globalData.request({
      url: '/user/progress/overview/',
      method: 'GET'
    }).then(res => {
      this.setData({
        studyStats: {
          totalDays: res.study_days || 0,
          totalQuestions: res.total_practices || 0,
          correctRate: res.correct_rate || 0
        },
        wrongCount: res.wrong_count || 0
      })
    }).catch(err => {
      console.error('加载学习概览失败:', err)
      this.setData({
        studyStats: {
          totalDays: 0,
          totalQuestions: 0,
          correctRate: 0
        },
        wrongCount: 0
      })
    })

    // 2. 收藏数量（当前后端暂无专门统计接口，统一显示 0，避免 404 报错）
    this.setData({
      favoriteCount: 0
    })
  },

  // 跳转页面
  gotoPage(e) {
    const url = e.currentTarget.dataset.url
    if (url) {
      wx.navigateTo({
        url: url,
        fail: () => {
          // 如果是tab页面，使用switchTab
          wx.switchTab({
            url: url,
            fail: () => {
              wx.showToast({
                title: '页面不存在',
                icon: 'none'
              })
            }
          })
        }
      })
    }
  },

  // 去登录
  handleLogin() {
    wx.navigateTo({
      url: '/pages/user/login'
    })
  },

  // 退出登录
  handleLogout() {
    wx.showModal({
      title: '退出登录',
      content: '确定要退出登录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清除用户信息和token
          wx.removeStorageSync('userInfo')
          wx.removeStorageSync('token')
          app.globalData.userInfo = null
          app.globalData.token = null
          
          this.setData({
            userInfo: null,
            hasUserInfo: false
          })
          
          wx.showToast({
            title: '已退出登录',
            icon: 'success'
          })
        }
      }
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
