// HSK详情页面 - 从后端 /api/hsk-info/ 读取数据
const app = getApp()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    level: 1, // 默认HSK级别
    loading: true,
    error: false,
    errorMsg: '',
    levelDescription: '',
    vocabularyCount: 0,
    examTime: '',
    passingScore: '',
    progressData: {
      overall: 0,
      vocabulary: 0,
      listening: 0,
      reading: 0,
      writing: 0
    },
    resources: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    if (options.level) {
      this.setData({
        level: parseInt(options.level)
      });
    }

    this.loadHskData();
  },

  /**
   * 加载HSK级别数据
   */
  loadHskData: function () {
    const level = this.data.level

    this.setData({
      loading: true,
      error: false
    })

    // 1. 获取当前级别的基本信息 /api/hsk-info/levels/{level}/
    const levelPromise = app.globalData.request({
      url: `/hsk-info/levels/${level}/`,
      method: 'GET',
      skipAuth: true
    })

    // 2. 获取该级别推荐的学习指南 /api/hsk-info/study-guides/?hsk_level={level}&is_featured=true
    const guidePromise = app.globalData.request({
      url: '/hsk-info/study-guides/',
      method: 'GET',
      data: { hsk_level: level, is_featured: true },
      skipAuth: true
    }).catch(() => [])

    Promise.all([levelPromise, guidePromise])
      .then(([levelData, guides]) => {
        if (!levelData) {
          throw new Error('未找到对应的HSK等级数据')
        }

        // 处理基础信息
        const description = levelData.description || ''
        const vocabularyCount = (levelData.vocabulary_count || 0) + '词'
        const examTime = (levelData.exam_duration || 0) + '分钟'
        const passingScore = (levelData.passing_score || 0) + '分'

        // 考试结构 exam_structure 是一个 JSON 数组，我们可以用它来简单构造进度条占比
        let progressData = this.data.progressData
        if (Array.isArray(levelData.exam_structure)) {
          const sections = levelData.exam_structure
          const totalParts = sections.length || 1
          const listening = sections.find(s => s.part?.includes('听力')) ? 1 : 0
          const reading = sections.find(s => s.part?.includes('阅读')) ? 1 : 0
          const writing = sections.find(s => s.part?.includes('写作')) ? 1 : 0

          progressData = {
            overall: 0,
            vocabulary: 0,
            listening: listening ? Math.round(100 / totalParts) : 0,
            reading: reading ? Math.round(100 / totalParts) : 0,
            writing: writing ? Math.round(100 / totalParts) : 0
          }
        }

        // 学习资源：用 StudyGuide 里的标题/内容生成卡片
        let resources = []
        if (Array.isArray(guides) && guides.length > 0) {
          resources = guides.map(item => ({
            id: item.id,
            name: item.title,
            description: (item.content || '').slice(0, 50) + (item.content && item.content.length > 50 ? '...' : ''),
            icon: '../../images/vocabulary-icon.png'
          }))
        }

        this.setData({
          levelDescription: description,
          vocabularyCount,
          examTime,
          passingScore,
          progressData,
          resources,
          loading: false
        })
      })
      .catch((err) => {
        console.error('加载HSK数据失败:', err)
        this.setData({
          error: true,
          errorMsg: err?.message || '无法获取HSK数据',
          loading: false
        })
      })
  },

  /**
   * 开始练习
   */
  startPractice: function (e) {
    const mode = e.currentTarget.dataset.mode;
    wx.navigateTo({
      url: `/pages/hsk/practice?level=${this.data.level}&mode=${mode}`
    });
  },

  /**
   * 查看学习资源
   */
  viewResource: function (e) {
    const resourceId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/hsk/resource?level=${this.data.level}&resourceId=${resourceId}`
    });
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
    this.loadHskData();
    wx.stopPullDownRefresh();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
    return {
      title: `HSK ${this.data.level}级学习`,
      path: `/pages/hsk/detail?level=${this.data.level}`
    };
  }
}); 