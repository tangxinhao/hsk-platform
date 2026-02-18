// 中国文化列表页面
const app = getApp()
const { t, getField, getLang } = require('../../utils/i18n')

Page({
  data: {
    categories: [],
    currentCategory: { id: 'all', name: '全部' },
    contentList: [],
    loading: true,
    currentPage: 1,
    pageSize: 10,
    hasMoreData: true,
    totalCount: 0,
    // 国际化文本
    pageTitle: '',
    loadingText: '',
    emptyText: '',
    loadMoreText: '',
    noMoreText: ''
  },

  onLoad: function (options) {
    // 如果有传入的分类ID，设置初始值
    if (options.categoryId) {
      this.setData({
        currentCategory: { id: options.categoryId, name: options.categoryName || '分类' }
      })
    }

    this.updateTexts()
    this.fetchCategories()
  },
  
  // 更新界面文本
  updateTexts() {
    this.setData({
      pageTitle: t('culture.title'),
      loadingText: t('common.loading'),
      emptyText: t('culture.noContent'),
      loadMoreText: t('common.loadMore'),
      noMoreText: t('common.noMore')
    })
    
    // 更新导航栏标题
    wx.setNavigationBarTitle({
      title: t('culture.title')
    })
  },
  
  // 语言切换回调
  onLanguageChange() {
    this.updateTexts()
    // 重新加载数据以显示对应语言的内容
    this.setData({
      contentList: [],
      currentPage: 1
    })
    this.fetchCategories()
  },

  onPullDownRefresh: function () {
    this.setData({
      contentList: [],
      currentPage: 1,
      hasMoreData: true
    })
    this.fetchContentList()
    wx.stopPullDownRefresh()
  },

  fetchCategories: function () {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/category/`,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          let categories = [{ 
            id: 'all', 
            name: t('common.all'),
            name_en: 'All'
          }]

          let data = res.data.results || res.data || []
          
          // 处理分类数据，添加显示名称
          data = data.map(cat => ({
            ...cat,
            displayName: getField(cat, 'name')
          }))
          
          categories = categories.concat(data)

          this.setData({
            categories
          })

          // 获取内容列表
          this.fetchContentList()
        } else {
          wx.showToast({
            title: t('error.loadFailed'),
            icon: 'none'
          })
          this.setData({ loading: false })
        }
      },
      fail: (err) => {
        console.error('获取分类失败:', err)
        wx.showToast({
          title: t('error.network'),
          icon: 'none'
        })
        this.setData({ loading: false })
        this.fetchContentList()
      }
    })
  },

  fetchContentList: function () {
    const { currentCategory, currentPage, pageSize } = this.data

    this.setData({ loading: true })

    // 构建查询参数
    const params = {
      page: currentPage,
      page_size: pageSize  // 修复：使用下划线命名
    }

    if (currentCategory.id !== 'all') {
      params.category = currentCategory.id
    }

    // 调用API获取文化内容列表
    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/content/`,  // 修复：使用正确的路径
      method: 'GET',
      data: params,
      success: (res) => {
        let newData = []

        if (res.statusCode === 200) {
          if (res.data.results) {
            newData = res.data.results.map(item => ({
              ...item,
              created_at: this.formatDate(item.created_at || item.createdAt),
              displayTitle: getField(item, 'title'),
              displayDesc: getField(item, 'description') || getField(item, 'content')?.substring(0, 100) || t('culture.noContent'),
              displayDifficulty: item.difficulty_display || t(`difficulty.${['easy','simple','medium','hard','difficult'][item.difficulty-1] || 'medium'}`)
            }))
            this.setData({
              totalCount: res.data.count || 0,
              hasMoreData: newData.length === pageSize
            })
          } else if (Array.isArray(res.data)) {
            newData = res.data.map(item => ({
              ...item,
              created_at: this.formatDate(item.created_at || item.createdAt),
              displayTitle: getField(item, 'title'),
              displayDesc: getField(item, 'description') || getField(item, 'content')?.substring(0, 100) || t('culture.noContent'),
              displayDifficulty: item.difficulty_display || t(`difficulty.${['easy','simple','medium','hard','difficult'][item.difficulty-1] || 'medium'}`)
            }))
            this.setData({
              hasMoreData: newData.length === pageSize
            })
          }

          // 如果是第一页，直接设置数据，否则追加数据
          if (this.data.currentPage === 1) {
            this.setData({
              contentList: newData
            })
          } else {
            this.setData({
              contentList: [...this.data.contentList, ...newData]
            })
          }
        } else {
          wx.showToast({
            title: '获取内容列表失败',
            icon: 'none'
          })
        }
      },
      fail: (err) => {
        console.error('获取内容列表失败:', err)
        wx.showToast({
          title: '网络错误，请稍后重试',
          icon: 'none'
        })
      },
      complete: () => {
        this.setData({ loading: false })
      }
    })
  },

  switchCategory: function (e) {
    const { id, name } = e.currentTarget.dataset
    
    console.log('切换分类:', id, name)

    this.setData({
      currentCategory: { id, name },
      contentList: [],
      currentPage: 1,
      hasMoreData: true
    })

    this.fetchContentList()
  },

  loadMore: function () {
    if (this.data.hasMoreData) {
      this.setData({
        currentPage: this.data.currentPage + 1
      })
      this.fetchContentList()
    }
  },

  navigateToDetail: function (e) {
    const contentId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/culture/detail?id=${contentId}`
    })
  },

  formatDate: function (dateString) {
    if (!dateString) return ''

    const date = new Date(dateString)
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')

    return `${year}-${month}-${day}`
  }
})