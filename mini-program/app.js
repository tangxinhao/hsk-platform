// app.js
const { request } = require('./utils/request.js')

App({
  onLaunch: function () {
    // 初始化日志
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 读取本地 token / 用户信息（不再使用 mock）
    const storedToken = wx.getStorageSync('token')
    const storedUser = wx.getStorageSync('userInfo')
    if (storedToken) this.globalData.token = storedToken
    if (storedUser) this.globalData.userInfo = storedUser

    // 获取系统信息（使用新API）
    const systemInfo = wx.getWindowInfo()
    this.globalData.systemInfo = systemInfo

    // 计算安全区域
    const menuButtonInfo = wx.getMenuButtonBoundingClientRect()
    this.globalData.navBarHeight = menuButtonInfo.bottom + 8
    this.globalData.statusBarHeight = systemInfo.statusBarHeight

    // 初始化用户配置
    this.initUserSettings()
  },

  initUserSettings: function () {
    // 从本地存储获取用户设置
    const settings = wx.getStorageSync('userSettings') || {
      theme: 'light',
      fontSize: 'medium',
      dailyGoal: 10
    }

    this.globalData.userSettings = settings
  },

  updateUserSettings: function (newSettings) {
    this.globalData.userSettings = {
      ...this.globalData.userSettings,
      ...newSettings
    }

    // 保存到本地存储
    wx.setStorageSync('userSettings', this.globalData.userSettings)
  },

  globalData: {
    userInfo: null,
    token: null,
    systemInfo: null,
    navBarHeight: 0,
    statusBarHeight: 0,
    userSettings: null,
    language: 'zh', // 默认语言：中文
    // 【重要】API 地址配置说明
    // ⚠️ 微信小程序正式版要求：
    // 1. 必须使用已备案的域名（不能使用 IP 地址）
    // 2. 必须使用 HTTPS（不能使用 HTTP）
    // 
    // 当前配置（仅开发工具测试）：
    // - 使用 IP 地址：http://118.190.106.159/api
    // - 需要在微信开发者工具中勾选"不校验合法域名"才能测试
    //
    // 域名备案完成后，请修改为：
    // apiBaseUrl: 'https://tangxinhao.online/api',
    // 并在微信后台添加 https://tangxinhao.online 到 request合法域名
    // 配置 HTTPS 后，使用以下地址：
    // apiBaseUrl: 'https://www.tangxinhao.online/api',
    // 临时配置（仅开发工具可用，需勾选"不校验合法域名"）
    apiBaseUrl: 'http://118.190.106.159/api', // ⚠️ 临时配置，仅开发工具可用
    // 统一请求方法
    request: request
  },
  
  // 切换语言
  switchLanguage(lang) {
    const { setLang } = require('./utils/i18n')
    setLang(lang)
    this.globalData.language = lang
    
    // 触发所有已打开页面的更新
    const pages = getCurrentPages()
    pages.forEach(page => {
      if (page.onLanguageChange && typeof page.onLanguageChange === 'function') {
        page.onLanguageChange()
      }
    })
    
    // 显示切换提示
    wx.showToast({
      title: lang === 'zh' ? '已切换到中文' : 'Switched to English',
      icon: 'success',
      duration: 1500
    })
    
    // 显示提示
    wx.showToast({
      title: lang === 'zh' ? '已切换到中文' : 'Switched to English',
      icon: 'success'
    })
  }
})