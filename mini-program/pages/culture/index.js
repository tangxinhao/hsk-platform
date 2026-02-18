// pages/culture/index.js
const app = getApp()
const { t, getLang } = require('../../utils/i18n')

Page({
  data: {
    categories: [],
    loading: false,
    currentLang: 'zh',
    // 国际化文本
    pageTitle: '',
    pageSubtitle: '',
    cuisinesTitle: '',
    viewAllText: '',
    categoriesTitle: '',
    recommendedTitle: '',
    loadingText: '',
    // 中国八大菜系
    cuisines: [
      { 
        key: 'lu',
        name: '鲁菜', 
        emoji: '🥘', 
        color: '#FF6B6B',
        desc: '北方菜系之首',
        region: '山东',
        image: '/images/default-culture.png'  // 使用本地默认图片
      },
      { 
        key: 'chuan',
        name: '川菜', 
        emoji: '🌶️', 
        color: '#FF4757',
        desc: '麻辣鲜香',
        region: '四川',
        image: '/images/default-culture.png'
      },
      { 
        key: 'yue',
        name: '粤菜', 
        emoji: '🦐', 
        color: '#FFA502',
        desc: '清淡鲜美',
        region: '广东',
        image: '/images/default-culture.png'
      },
      { 
        key: 'su',
        name: '苏菜', 
        emoji: '🥟', 
        color: '#2ED573',
        desc: '清鲜平和',
        region: '江苏',
        image: '/images/default-culture.png'
      },
      { 
        key: 'min',
        name: '闽菜', 
        emoji: '🦀', 
        color: '#1E90FF',
        desc: '重视汤鲜',
        region: '福建',
        image: '/images/default-culture.png'
      },
      { 
        key: 'zhe',
        name: '浙菜', 
        emoji: '🐟', 
        color: '#5F27CD',
        desc: '鲜嫩软滑',
        region: '浙江',
        image: '/images/default-culture.png'
      },
      { 
        key: 'xiang',
        name: '湘菜', 
        emoji: '🔥', 
        color: '#EE5A6F',
        desc: '香辣酸咸',
        region: '湖南',
        image: '/images/default-culture.png'
      },
      { 
        key: 'hui',
        name: '徽菜', 
        emoji: '🍲', 
        color: '#00D2D3',
        desc: '重油重色',
        region: '安徽',
        image: '/images/default-culture.png'
      }
    ],
    // 推荐内容
    recommendedContent: []
  },

  onLoad(options) {
    this.updateTexts()
    this.updateCuisines()
    this.loadCategories()
    this.loadRecommendedContent()
  },

  onShow() {
    this.updateTexts()
    this.updateCuisines()
  },

  onPullDownRefresh() {
    this.loadCategories()
    this.loadRecommendedContent()
  },
  
  updateTexts() {
    const lang = getLang()
    this.setData({
      currentLang: lang,
      pageTitle: t('culture.title'),
      pageSubtitle: t('culture.subtitle'),
      cuisinesTitle: t('culture.cuisinesTitle'),
      viewAllText: t('culture.viewAll'),
      categoriesTitle: t('culture.categoriesTitle'),
      recommendedTitle: t('culture.recommendedTitle'),
      loadingText: t('culture.loading')
    })
    
    wx.setNavigationBarTitle({
      title: t('culture.title')
    })
  },
  
  updateCuisines() {
    const lang = getLang()
    const updatedCuisines = this.data.cuisines.map(cuisine => ({
      ...cuisine,
      displayName: t(`culture.cuisines.${cuisine.key}.name`),
      displayDesc: t(`culture.cuisines.${cuisine.key}.desc`),
      displayRegion: t(`culture.cuisines.${cuisine.key}.region`)
    }))
    this.setData({ cuisines: updatedCuisines })
  },
  
  onLanguageChange() {
    this.updateTexts()
    this.updateCuisines()
    this.loadCategories()
    this.loadRecommendedContent()
  },

  // 获取分类图标
  getCategoryIcon(name) {
    const iconMap = {
      '历史': '🏛️', 'History': '🏛️',
      '艺术': '🎨', 'Arts': '🎨', 
      '文学': '📖', 'Literature': '📖',
      '哲学': '💭', 'Philosophy': '💭',
      '饮食': '🍜', 'Cuisine': '🍜',
      '节日': '🎊', 'Festival': '🎊',
      '戏曲': '🎭', 'Opera': '🎭'
    }
    
    for (let key in iconMap) {
      if (name.includes(key)) {
        return iconMap[key]
      }
    }
    return '📌'
  },
  
  // 加载分类
  loadCategories() {
    this.setData({ loading: true })
    const lang = getLang()
    
    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/category/`,
      method: 'GET',
      success: (res) => {
        let categories = Array.isArray(res.data) ? res.data : (res.data.results || [])
        
        // 添加国际化显示名称和图标
        categories = categories.map(cat => ({
          ...cat,
          displayName: lang === 'zh' ? cat.name : (cat.name_en || cat.name),
          displayLevel: cat.level || (lang === 'zh' ? '中级' : 'Medium'),
          icon: this.getCategoryIcon(cat.name)
        }))
        
        this.setData({ categories })
      },
      fail: (err) => {
        console.error('加载分类失败:', err)
        // 不再使用本地模拟数据，直接置为空
        this.setData({ categories: [] })
      },
      complete: () => {
        this.setData({ loading: false })
        wx.stopPullDownRefresh()
      }
    })
  },

  // 加载推荐内容
  loadRecommendedContent() {
    const lang = getLang()
    
    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/content/`,
      method: 'GET',
      data: {
        page: 1,
        page_size: 4,
        lang: lang
      },
      success: (res) => {
        let content = res.data.results || res.data || []
        
        // 添加国际化显示字段
        content = content.map(item => ({
          ...item,
          displayTitle: lang === 'zh' ? item.title : (item.title_en || item.title),
          categoryName: item.category ? (lang === 'zh' ? item.category.name : (item.category.name_en || item.category.name)) : (lang === 'zh' ? '文化' : 'Culture'),
          displayDifficulty: this.getDifficultyText(item.difficulty, lang)
        }))
        
        this.setData({ recommendedContent: content })
      },
      fail: (err) => {
        console.error('加载推荐内容失败:', err)
        // 失败时不显示推荐内容，八大菜系仍可用
      }
    })
  },
  
  // 获取难度文本
  getDifficultyText(difficulty, lang) {
    const difficultyMap = {
      'easy': lang === 'zh' ? '简单' : 'Easy',
      'medium': lang === 'zh' ? '中等' : 'Medium',
      'hard': lang === 'zh' ? '困难' : 'Hard'
    }
    return difficultyMap[difficulty] || (lang === 'zh' ? '中等' : 'Medium')
  },

  // 点击菜系卡片 - 改为通过ID访问
  navigateToCuisine(e) {
    const cuisineName = e.currentTarget.dataset.cuisine
    
    // 从API搜索菜系ID
    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/content/`,
      method: 'GET',
      data: {
        search: cuisineName,
        page_size: 1
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data.results && res.data.results.length > 0) {
          const contentId = res.data.results[0].id
          wx.navigateTo({
            url: `/pages/culture/detail?id=${contentId}`
          })
        } else {
          // 降级方案：使用菜系名称
          wx.navigateTo({
            url: `/pages/culture/detail?cuisine=${cuisineName}`
          })
        }
      },
      fail: () => {
        // 失败时使用菜系名称
        wx.navigateTo({
          url: `/pages/culture/detail?cuisine=${cuisineName}`
        })
      }
    })
  },

  // 查看所有分类
  navigateToList(e) {
    const categoryId = e.currentTarget.dataset.id
    const categoryName = e.currentTarget.dataset.name
    
    wx.navigateTo({
      url: `/pages/culture/list?categoryId=${categoryId}&categoryName=${categoryName}`
    })
  },

  // 查看所有菜系
  viewAllCuisines() {
    const lang = getLang()
    const title = lang === 'zh' ? '中国八大菜系' : 'Eight Major Cuisines'
    const content = lang === 'zh' 
      ? '鲁菜、川菜、粤菜、苏菜、闽菜、浙菜、湘菜、徽菜'
      : 'Lu, Sichuan, Cantonese, Jiangsu, Fujian, Zhejiang, Hunan, Anhui'
    const confirmText = lang === 'zh' ? '查看列表' : 'View List'
    
    wx.showModal({
      title: title,
      content: content,
      confirmText: confirmText,
      success: (res) => {
        if (res.confirm) {
          wx.navigateTo({
            url: '/pages/culture/list?categoryId=cuisine'
          })
        }
      }
    })
  },

  // 查看推荐内容详情
  navigateToDetail(e) {
    const contentId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/culture/detail?id=${contentId}`
    })
  }
})