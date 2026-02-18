/**
 * 统一请求封装（小程序端）
 * - 自动拼接 baseURL
 * - 自动附带 token
 * - 401 时跳转登录页
 */
const app = getApp()

const request = ({ url, method = 'GET', data = {}, header = {}, skipAuth = false }) => {
  return new Promise((resolve, reject) => {
    // 获取baseURL，如果app未初始化则使用默认值
    const appInstance = getApp()
    // 默认兜底也使用服务器公网IP，避免域名未配置时请求失败
    const baseURL = (appInstance?.globalData?.apiBaseUrl || 'http://118.190.106.159/api').replace(/\/$/, '')
    
    // 构建完整URL
    const fullUrl = url.startsWith('http') ? url : `${baseURL}${url}`

    const token = wx.getStorageSync('token')
    const headers = {
      'Content-Type': 'application/json',
      ...header
    }
    if (token && !skipAuth) {
      headers['Authorization'] = `Bearer ${token}`
    }

    console.log('发起请求:', method, fullUrl, data)
    
    wx.request({
      url: fullUrl,
      method,
      data,
      header: headers,
      timeout: 30000,
      success: (res) => {
        console.log('请求响应:', fullUrl, 'Status:', res.statusCode, 'Data:', res.data)
        
        if (res.statusCode === 401) {
          // 未登录：只做提醒和清理，不强制自动跳转，避免用户在浏览时被频繁打断
          wx.removeStorageSync('token')
          wx.showToast({ title: '请先登录', icon: 'none' })
          reject(res)
          return
        }
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          console.error('请求失败:', fullUrl, 'Status:', res.statusCode, 'Data:', res.data)
          let errorMsg = '请求失败'
          
          if (res.statusCode === 400) {
            errorMsg = res.data?.detail || '请求参数错误'
          } else if (res.statusCode === 502) {
            errorMsg = '服务器连接失败，请检查网络'
          } else if (res.data?.detail) {
            errorMsg = res.data.detail
          }
          
          wx.showToast({ title: errorMsg, icon: 'none', duration: 2000 })
          reject(res)
        }
      },
      fail: (err) => {
        console.error('请求fail回调:', fullUrl, 'Error:', err)
        wx.showToast({ title: '网络连接失败', icon: 'none', duration: 2000 })
        reject(err)
      }
    })
  })
}

module.exports = {
  request
}
