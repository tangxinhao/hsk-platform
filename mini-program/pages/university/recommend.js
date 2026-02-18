const app = getApp()

Page({
  data: {
    recommendations: [],
    loading: true,
    error: false,
    errorMsg: '',
    // 用户偏好设置
    userPreferences: {
      hskLevel: 4,
      region: '',
      major: '',
      budget: 50000
    },
    showPreferenceDialog: false,
    regions: ['北京', '上海', '广东', '江苏', '浙江', '四川', '湖北', '陕西'],
    selectedRegion: ''
  },

  onLoad() {
    this.loadUserPreferences()
    this.loadRecommendations()
  },

  onPullDownRefresh() {
    this.loadRecommendations()
  },

  // 加载用户偏好
  loadUserPreferences() {
    const preferences = wx.getStorageSync('universityPreferences')
    if (preferences) {
      this.setData({ userPreferences: preferences })
    }
  },

  // 保存用户偏好
  saveUserPreferences() {
    wx.setStorageSync('universityPreferences', this.data.userPreferences)
  },

  // 加载推荐院校
  loadRecommendations() {
    this.setData({ loading: true, error: false })

    // 尝试从API获取推荐（全部从后端返回，不再使用本地示例数据）
    wx.request({
      url: `${app.globalData.apiBaseUrl}/university/recommend/`,
      method: 'GET',
      data: this.data.userPreferences,
      success: (res) => {
        if (res.statusCode === 200) {
          let recommendations = res.data.results || res.data || []

          // 计算匹配分数和推荐理由（基于后端返回的数据）
          recommendations = recommendations.map(item => ({
            ...item,
            match_score: this.calculateMatchScore(item),
            match_reasons: this.getMatchReasons(item)
          }))

          // 按匹配分数排序
          recommendations.sort((a, b) => b.match_score - a.match_score)

          this.setData({ 
            recommendations,
            loading: false 
          })
        } else {
          this.setData({
            loading: false,
            error: true,
            errorMsg: res.data?.detail || '获取推荐院校失败'
          })
          wx.showToast({
            title: '获取推荐院校失败',
            icon: 'none'
          })
        }
      },
      fail: (err) => {
        console.error('获取推荐失败:', err)
        this.setData({ 
          recommendations: [],
          loading: false,
          error: true,
          errorMsg: '获取推荐院校失败，请稍后重试'
        })
        wx.showToast({
          title: '获取推荐院校失败，请稍后重试',
          icon: 'none'
        })
      },
      complete: () => {
        wx.stopPullDownRefresh()
      }
    })
  },

  // 以前用于筛选本地推荐数据的函数已不再使用，所有推荐都来自后端数据库

  // 计算匹配分数
  calculateMatchScore(university) {
    const { userPreferences } = this.data
    let score = 0
    
    // HSK等级匹配（40分）
    if (userPreferences.hskLevel >= university.min_hsk_level) {
      score += 40
    } else {
      score += Math.max(0, 40 - (university.min_hsk_level - userPreferences.hskLevel) * 10)
    }
    
    // 地区匹配（30分）
    if (userPreferences.region && university.region === userPreferences.region) {
      score += 30
    }
    
    // 学校排名（30分）
    if (university.ranking <= 10) {
      score += 30
    } else if (university.ranking <= 50) {
      score += 20
    } else {
      score += 10
    }
    
    return Math.min(100, score)
  },

  // 获取匹配原因
  getMatchReasons(university) {
    const { userPreferences } = this.data
    const reasons = []
    
    if (userPreferences.hskLevel >= university.min_hsk_level) {
      reasons.push('HSK水平符合要求')
    }
    
    if (userPreferences.region === university.region) {
      reasons.push('在您偏好的地区')
    }
    
    if (university.ranking <= 20) {
      reasons.push('排名靠前')
    }
    
    if (university.tags && university.tags.includes('双一流')) {
      reasons.push('双一流高校')
    }
    
    return reasons.length > 0 ? reasons : ['综合评估推荐']
  },

  // 显示偏好设置对话框
  showPreferences() {
    this.setData({ showPreferenceDialog: true })
  },

  // 关闭偏好设置对话框
  closePreferences() {
    this.setData({ showPreferenceDialog: false })
  },

  // HSK等级改变
  onHSKLevelChange(e) {
    this.setData({
      'userPreferences.hskLevel': parseInt(e.detail.value)
    })
  },

  // 地区选择改变
  onRegionChange(e) {
    const index = e.detail.value
    this.setData({
      'userPreferences.region': this.data.regions[index]
    })
  },

  // 应用偏好设置
  applyPreferences() {
    this.saveUserPreferences()
    this.closePreferences()
    this.loadRecommendations()
    wx.showToast({
      title: '偏好已更新',
      icon: 'success'
    })
  },

  // 查看院校详情
  navigateToDetail(e) {
    const id = e.currentTarget.dataset.id
    
    // 判断是否是本地数据
    if (String(id).startsWith('local_')) {
      wx.showToast({
        title: '这是示例数据',
        icon: 'none'
      })
      return
    }
    
    wx.navigateTo({
      url: `/pages/university/detail?id=${id}`
    })
  },

  // 刷新推荐
  refreshRecommendations() {
    this.loadRecommendations()
  },

  // 分享
  onShareAppMessage() {
    return {
      title: '为你推荐的优质院校',
      path: '/pages/university/recommend'
    }
  }
}) 