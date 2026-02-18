const { request } = require('../../utils/request')
const app = getApp()

Page({
  data: {
    username: '',
    password: '',
    loading: false
  },

  onInput(e) {
    const { field } = e.currentTarget.dataset
    this.setData({ [field]: e.detail.value })
  },

  async handleRegister() {
    const { username, password } = this.data
    if (!username || !password) {
      wx.showToast({ title: '请输入账号和密码', icon: 'none' })
      return
    }
    this.setData({ loading: true })
    try {
      await app.globalData.request({
        url: '/user/register/',
        method: 'POST',
        data: { username, password }
      })
      wx.showToast({ title: '注册成功', icon: 'success' })
      // 注册成功后直接登录
      const res = await app.globalData.request({
        url: '/user/login/',
        method: 'POST',
        data: { username, password }
      })
      const token = res.access || res.token
      if (token) {
        wx.setStorageSync('token', token)
        app.globalData.token = token
      }
      if (res.user) {
        wx.setStorageSync('userInfo', res.user)
        app.globalData.userInfo = res.user
      }
      wx.navigateBack({ delta: 1 })
    } catch (err) {
      // request 已提示
    } finally {
      this.setData({ loading: false })
    }
  }
})
