// 问题列表页面
const app = getApp()

Page({
  data: {
    questions: [],
    loading: true,
    searchQuery: '',
    levels: [
      { id: '', label: '全部等级' },
      { id: '1', label: 'HSK 1级' },
      { id: '2', label: 'HSK 2级' },
      { id: '3', label: 'HSK 3级' },
      { id: '4', label: 'HSK 4级' },
      { id: '5', label: 'HSK 5级' },
      { id: '6', label: 'HSK 6级' }
    ],
    questionTypes: [
      { id: '', label: '全部类型' },
      { id: 'listening', label: '听力题' },
      { id: 'reading', label: '阅读题' },
      { id: 'fill', label: '填空题' },
      { id: 'writing', label: '书写题' },
      { id: 'single', label: '单选题' }
    ],
    levelIndex: 0,
    typeIndex: 0,
    selectedLevel: '',
    selectedType: '',
    currentPage: 1,
    pageSize: 10,
    hasMoreData: true,
    totalCount: 0,
    optionLabels: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
  },

  onLoad: function (options) {
    // 如果有传入的筛选参数，设置初始值
    if (options.level) {
      const levelIndex = this.data.levels.findIndex(item => item.id === options.level)
      if (levelIndex !== -1) {
        this.setData({
          levelIndex,
          selectedLevel: this.data.levels[levelIndex].label
        })
      }
    }

    if (options.type) {
      const typeIndex = this.data.questionTypes.findIndex(item => item.id === options.type)
      if (typeIndex !== -1) {
        this.setData({
          typeIndex,
          selectedType: this.data.questionTypes[typeIndex].label
        })
      }
    }

    this.fetchQuestions()
  },

  onPullDownRefresh: function () {
    this.setData({
      questions: [],
      currentPage: 1,
      hasMoreData: true
    })
    this.fetchQuestions()
  },

  fetchQuestions: function () {
    const { currentPage, pageSize, searchQuery, selectedLevel, selectedType } = this.data

    this.setData({ loading: true })

    // 构建查询参数
    const params = {
      page: currentPage,
      page_size: pageSize,
      content: searchQuery || undefined
    }

    if (selectedLevel) {
      params.level = selectedLevel.replace('HSK ', '').replace('级', '')
    }

    if (selectedType) {
      params.type = selectedType
    }

    // 调用API获取问题列表
    const { request } = require('../../utils/request')
    request({
      url: '/question/questions/',
      method: 'GET',
      data: {
        page: currentPage,
        page_size: pageSize,
        level: params.level,
        type: params.type
      }
    }).then((res) => {
      let newData = []
      if (res.results) {
        newData = res.results
        this.setData({
          totalCount: res.count || 0,
          hasMoreData: newData.length === pageSize
        })
      } else if (Array.isArray(res)) {
        newData = res
        this.setData({
          hasMoreData: newData.length === pageSize
        })
      }

      // 处理选项数据，确保它们是数组
      newData = newData.map(question => {
        if (question.options && typeof question.options === 'string') {
          try {
            question.options = JSON.parse(question.options)
          } catch (e) {
            question.options = []
          }
        }
        return question
      })

      // 如果是第一页，直接设置数据，否则追加数据
      if (this.data.currentPage === 1) {
        this.setData({
          questions: newData
        })
      } else {
        this.setData({
          questions: [...this.data.questions, ...newData]
        })
      }
    }).catch(() => {
      wx.showToast({
        title: '获取题目列表失败',
        icon: 'none'
      })
    }).finally(() => {
      this.setData({ loading: false })
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
      questions: []
    })
    this.fetchQuestions()
  },

  onLevelChange: function (e) {
    const index = e.detail.value
    const level = this.data.levels[index]

    this.setData({
      levelIndex: index,
      selectedLevel: level.label === '全部等级' ? '' : level.label,
      currentPage: 1,
      questions: []
    })

    this.fetchQuestions()
  },

  onTypeChange: function (e) {
    const index = e.detail.value
    const type = this.data.questionTypes[index]

    this.setData({
      typeIndex: index,
      selectedType: type.label === '全部类型' ? '' : type.label,
      currentPage: 1,
      questions: []
    })

    this.fetchQuestions()
  },

  loadMore: function () {
    if (this.data.hasMoreData) {
      this.setData({
        currentPage: this.data.currentPage + 1
      })
      this.fetchQuestions()
    }
  },

  navigateToDetail: function (e) {
    const questionId = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/question/detail?id=${questionId}`
    })
  },

  // 根据题目类型获取标签颜色
  getTagColor: function (type) {
    const colorMap = {
      'single': '#67c23a',
      'multiple': '#e6a23c',
      'judge': '#409eff',
      'fill': '#f56c6c',
      'listening': '#9c27b0',
      'reading': '#00a4ff',
      'writing': '#ff9800'
    }
    return colorMap[type] || '#909399'
  }
}) 