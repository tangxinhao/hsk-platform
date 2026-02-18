const { request } = require('../../utils/request')
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    loading: false
  },

  onShow() {
    // 如果已有 token，直接返回上一页
    const token = wx.getStorageSync('token')
    if (token) {
      wx.showToast({ title: '已登录', icon: 'none' })
      wx.navigateBack({ delta: 1 })
    }
  },

  onInput(e) {
    const { field } = e.currentTarget.dataset
    this.setData({ [field]: e.detail.value })
  },

  async handleLogin() {
    const { username, password } = this.data
    if (!username || !password) {
      wx.showToast({ title: '请输入账号和密码', icon: 'none' })
      return
    }
    this.setData({ loading: true })
    try {
      const res = await app.globalData.request({
        url: '/user/login/',
        method: 'POST',
        data: { username, password }
      })
      // 假设返回 { access, refresh, user }
      const token = res.access || res.token
      if (token) {
        wx.setStorageSync('token', token)
        app.globalData.token = token
      }
      if (res.user) {
        wx.setStorageSync('userInfo', res.user)
        app.globalData.userInfo = res.user
      }
      wx.showToast({ title: '登录成功', icon: 'success' })
      setTimeout(() => {
        wx.navigateBack({ delta: 1 })
      }, 500)
    } catch (err) {
      // 错误已在 request 中提示
    } finally {
      this.setData({ loading: false })
    }
  }
})
