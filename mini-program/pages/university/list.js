// 高校列表页面
const app = getApp()

Page({
  data: {
    universities: [],
    filteredUniversities: [],
    loading: true,
    searchQuery: '',
    regions: [
      { id: '', label: '全部地区' },
      { id: '北京', label: '北京' },
      { id: '上海', label: '上海' },
      { id: '广东', label: '广东' },
      { id: '江苏', label: '江苏' },
      { id: '浙江', label: '浙江' },
      { id: '四川', label: '四川' },
      { id: '湖北', label: '湖北' },
      { id: '湖南', label: '湖南' },
      { id: '河北', label: '河北' },
      { id: '河南', label: '河南' },
      { id: '山东', label: '山东' },
      { id: '山西', label: '山西' },
      { id: '陕西', label: '陕西' },
      { id: '安徽', label: '安徽' },
      { id: '福建', label: '福建' },
      { id: '江西', label: '江西' },
      { id: '广西', label: '广西' },
      { id: '云南', label: '云南' },
      { id: '贵州', label: '贵州' },
      { id: '辽宁', label: '辽宁' },
      { id: '吉林', label: '吉林' },
      { id: '黑龙江', label: '黑龙江' },
      { id: '内蒙古', label: '内蒙古' },
      { id: '新疆', label: '新疆' },
      { id: '西藏', label: '西藏' },
      { id: '宁夏', label: '宁夏' },
      { id: '甘肃', label: '甘肃' },
      { id: '青海', label: '青海' },
      { id: '天津', label: '天津' },
      { id: '重庆', label: '重庆' },
      { id: '海南', label: '海南' }
    ],
    options985: [
      { id: '', label: '全部' },
      { id: 'true', label: '是' },
      { id: 'false', label: '否' }
    ],
    options211: [
      { id: '', label: '全部' },
      { id: 'true', label: '是' },
      { id: 'false', label: '否' }
    ],
    regionIndex: 0,
    index985: 0,
    index211: 0,
    selectedRegion: '',
    selected985: '',
    selected211: '',
    currentPage: 1,
    pageSize: 10,
    hasMoreData: true,
    totalCount: 0
  },

  onLoad: function (options) {
    this.fetchUniversities()
  },

  onPullDownRefresh: function () {
    this.setData({
      universities: [],
      currentPage: 1,
      hasMoreData: true
    })
    this.fetchUniversities()
  },

  fetchUniversities: function () {
    const { currentPage, pageSize, searchQuery, selectedRegion, selected985, selected211 } = this.data

    this.setData({ loading: true })

    // 构建查询参数
    const params = {
      page: currentPage,
      page_size: pageSize
    }

    if (searchQuery) {
      params.search = searchQuery
    }

    if (selectedRegion) {
      params.region = selectedRegion
    }

    if (selected985 === '是') {
      params.is985 = 'true'
    } else if (selected985 === '否') {
      params.is985 = 'false'
    }

    if (selected211 === '是') {
      params.is211 = 'true'
    } else if (selected211 === '否') {
      params.is211 = 'false'
    }

    // 使用封装的request工具
    app.globalData.request({
      url: '/university/',
      method: 'GET',
      data: params
    })
      .then((res) => {
        let newData = []
        let hasMore = false
        let total = 0

        if (res.results) {
          // 分页响应格式
          newData = res.results
          total = res.count || 0
          hasMore = !!res.next
        } else if (Array.isArray(res)) {
          // 简单数组响应格式
          newData = res
          hasMore = newData.length === pageSize
          total = newData.length
        }

        this.setData({
          universities: currentPage === 1 ? newData : [...this.data.universities, ...newData],
          loading: false,
          hasMoreData: hasMore,
          totalCount: total
        })
      })
      .catch((err) => {
        console.error('获取高校列表失败:', err)
        wx.showToast({
          title: err.data?.detail || '获取高校列表失败',
          icon: 'none'
        })
        this.setData({ loading: false })
      })
      .finally(() => {
        wx.stopPullDownRefresh()
      })
  },

  onSearchInput: function (e) {
    this.setData({
      searchQuery: e.detail.value
    })
  },

  handleSearch: function () {
    this.setData({
      currentPage: 1,
      universities: []
    })
    this.fetchUniversities()
  },

  onRegionChange: function (e) {
    const index = e.detail.value
    const region = this.data.regions[index]

    this.setData({
      regionIndex: index,
      selectedRegion: region.id,
      currentPage: 1,
      universities: []
    })

    this.fetchUniversities()
  },

  on985Change: function (e) {
    const index = e.detail.value
    const option = this.data.options985[index]

    this.setData({
      index985: index,
      selected985: option.label === '全部' ? '' : option.label,
      currentPage: 1,
      universities: []
    })

    this.fetchUniversities()
  },

  on211Change: function (e) {
    const index = e.detail.value
    const option = this.data.options211[index]

    this.setData({
      index211: index,
      selected211: option.label === '全部' ? '' : option.label,
      currentPage: 1,
      universities: []
    })

    this.fetchUniversities()
  },

  loadMore: function () {
    if (this.data.hasMoreData) {
      this.setData({
        currentPage: this.data.currentPage + 1
      })
      this.fetchUniversities()
    }
  },

  navigateToDetail: function (e) {
    const universityId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/university/detail?id=${universityId}`
    })
  }
}) 