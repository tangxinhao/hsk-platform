// pages/practice/list.js
const app = getApp()

Page({
  data: {
    level: 1,
    questions: [],
    types: [
      { value: '', label: '全部类型' },
      { value: 'listening', label: '听力题' },
      { value: 'reading', label: '阅读题' },
      { value: 'writing', label: '书写题' },
      { value: 'fill', label: '填空题' },
      { value: 'single', label: '单选题' }
    ],
    typeIndex: 0,
    selectedType: '',
    loading: false,
    hasMore: true,
    page: 1,
    pageSize: 20
  },

  onLoad(options) {
    if (options.level) {
      this.setData({ level: parseInt(options.level) })
    }
    wx.setNavigationBarTitle({
      title: `HSK ${this.data.level}级练习`
    })
    this.loadQuestions()
  },
  
  onShow() {
    // 每次显示时刷新完成状态
    this.updateQuestionStatus()
  },

  onPullDownRefresh() {
    this.setData({ page: 1, questions: [] })
    this.loadQuestions()
  },

  loadQuestions() {
    const { level, selectedType, page, pageSize } = this.data
    
    this.setData({ loading: true })
    
    const params = {
      level: level,
      page: page,
      page_size: pageSize
    }
    
    if (selectedType) {
      params.type = selectedType
    }
    
    app.globalData.request({
      url: '/question/questions/',
      data: params
    })
      .then((res) => {
        const newQuestions = res.results || res || []
        
        // 合并数据
        const questions = page === 1 ? newQuestions : [...this.data.questions, ...newQuestions]
        
        // 标记已完成的题目
        const markedQuestions = this.markCompletedQuestionsSync(questions)
        
        this.setData({
          questions: markedQuestions,
          hasMore: !!res.next || newQuestions.length === pageSize,
          loading: false
        })
        
        wx.stopPullDownRefresh()
      })
      .catch((err) => {
        console.error('加载题目失败:', err)
        this.setData({ loading: false })
        wx.stopPullDownRefresh()
        wx.showToast({
          title: '加载失败，请重试',
          icon: 'none'
        })
      })
  },

  // 标记已完成的题目（同步版本，返回标记后的数组）
  markCompletedQuestionsSync(questions) {
    const completedQuestions = wx.getStorageSync('completedQuestions') || {}
    return questions.map(q => ({
      ...q,
      done: !!completedQuestions[q.id]
    }))
  },

  // 标记已完成的题目（原地修改版本）
  markCompletedQuestions(questions) {
    const completedQuestions = wx.getStorageSync('completedQuestions') || {}
    questions.forEach(q => {
      q.done = !!completedQuestions[q.id]
    })
  },

  // 更新题目完成状态
  updateQuestionStatus() {
    const questions = this.data.questions
    if (questions.length > 0) {
      const markedQuestions = this.markCompletedQuestionsSync(questions)
      this.setData({ questions: markedQuestions })
    }
  },

  onTypeChange(e) {
    const index = e.detail.value
    const type = this.data.types[index]
    
    this.setData({
      typeIndex: index,
      selectedType: type.value,
      page: 1,
      questions: []
    })
    
    this.loadQuestions()
  },

  loadMore() {
    if (!this.data.hasMore || this.data.loading) return
    
    this.setData({ page: this.data.page + 1 })
    this.loadQuestions()
  },

  goToQuestion(e) {
    const { id, index } = e.currentTarget.dataset
    wx.navigateTo({
      url: `/pages/practice/detail?id=${id}&level=${this.data.level}&index=${index}`
    })
  }
})
