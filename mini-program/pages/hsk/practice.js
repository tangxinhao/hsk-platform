// HSK练习页面
Page({
  /**
   * 页面的初始数据
   */
  data: {
    level: 1, // HSK级别
    mode: 'vocabulary', // 练习模式
    loading: true,
    error: false,
    errorMsg: '',
    questions: [],
    currentIndex: 0,
    userAnswer: null,
    showResult: false,
    completed: false,
    isPlaying: false,
    optionLetters: ['A', 'B', 'C', 'D', 'E', 'F'],
    stats: {
      totalQuestions: 0,
      correctCount: 0,
      wrongCount: 0,
      accuracy: 0
    },
    wrongQuestions: []
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

    if (options.mode) {
      this.setData({
        mode: options.mode
      });
    }

    this.loadQuestions();
  },

  /**
   * 加载练习题目（改为调用后端）
   */
  loadQuestions: function () {
    this.setData({
      loading: true,
      error: false,
      currentIndex: 0,
      userAnswer: null,
      showResult: false,
      completed: false
    });

    const { request } = require('../../utils/request')
    request({
      url: '/question/questions/',
      method: 'GET',
      data: {
        level: this.data.level,
        page: 1,
        page_size: 20
      }
    }).then(res => {
      const raw = res.results || res || []
      const questions = raw.map(q => {
        let opts = []
        if (q.options) {
          try {
            opts = typeof q.options === 'string' ? JSON.parse(q.options) : q.options
          } catch (e) {
            opts = []
          }
        }
        // 转换为 {text, correct} 结构便于校验
        const mappedOptions = Array.isArray(opts) ? opts.map(opt => ({
          text: opt,
          correct: (opt === q.answer)
        })) : []
        return {
          id: q.id,
          type: q.type || '单选题',
          question: q.content || '',
          options: mappedOptions,
          answer: q.answer,
          audio: q.audio_url,
          audio_duration: q.audio_duration,
          image: q.image_url,
          explanation: q.explanation || ''
        }
      })

      if (questions.length > 0) {
        this.setData({
          questions,
          loading: false,
          stats: {
            totalQuestions: questions.length,
            correctCount: 0,
            wrongCount: 0,
            accuracy: 0
          }
        });
      } else {
        this.setData({
          error: true,
          errorMsg: '暂无题目',
          loading: false
        });
      }
    }).catch(err => {
      console.error('获取题目失败', err)
      this.setData({
        error: true,
        errorMsg: '加载失败，请稍后再试',
        loading: false
      });
    });
  },

  // 删除所有模拟数据函数，改为后端数据

  /**
   * 选择选项
   */
  selectOption: function (e) {
    if (this.data.showResult) return; // 已显示结果时不允许更改选择

    const index = e.currentTarget.dataset.index;
    this.setData({
      userAnswer: index
    });
  },

  /**
   * 输入答案（填空题）
   */
  onInputAnswer: function (e) {
    this.setData({
      userAnswer: e.detail.value
    });
  },

  /**
   * 播放音频
   */
  playAudio: function () {
    // 实际项目中，这里应该使用wx.createInnerAudioContext()播放音频
    console.log('播放音频：', this.data.questions[this.data.currentIndex].audio);

    this.setData({
      isPlaying: true
    });

    // 模拟音频播放结束
    setTimeout(() => {
      this.setData({
        isPlaying: false
      });
    }, 3000);
  },

  /**
   * 检查答案
   */
  checkAnswer: function () {
    const currentQuestion = this.data.questions[this.data.currentIndex];
    let isCorrect = false;

    if (currentQuestion.type === '填空题') {
      // 填空题答案检查
      isCorrect = this.data.userAnswer === currentQuestion.answer;
    } else {
      // 选择题答案检查
      isCorrect = currentQuestion.options[this.data.userAnswer].correct;
    }

    // 更新统计数据
    const stats = { ...this.data.stats };
    if (isCorrect) {
      stats.correctCount++;
    } else {
      stats.wrongCount++;
      // 记录错题
      const wrongQuestions = [...this.data.wrongQuestions];
      wrongQuestions.push(this.data.currentIndex);
      this.setData({
        wrongQuestions: wrongQuestions
      });
    }

    // 计算正确率
    stats.accuracy = Math.round((stats.correctCount / (stats.correctCount + stats.wrongCount)) * 100);

    this.setData({
      showResult: true,
      stats: stats
    });
  },

  /**
   * 下一题
   */
  nextQuestion: function () {
    if (this.data.currentIndex < this.data.questions.length - 1) {
      // 还有下一题
      this.setData({
        currentIndex: this.data.currentIndex + 1,
        userAnswer: null,
        showResult: false
      });
    } else {
      // 已完成所有题目
      this.setData({
        completed: true
      });
    }
  },

  /**
   * 复习错题
   */
  reviewWrongAnswers: function () {
    // 实际项目中，这里应该跳转到错题复习页面
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    });
  },

  /**
   * 重新练习
   */
  retryPractice: function () {
    this.loadQuestions();
  },

  /**
   * 返回HSK详情页
   */
  backToDetail: function () {
    wx.navigateBack();
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
      title: `HSK ${this.data.level}级${this.getModeText()}练习`,
      path: `/pages/hsk/practice?level=${this.data.level}&mode=${this.data.mode}`
    };
  },

  /**
   * 获取练习模式文本
   */
  getModeText: function () {
    const modeTexts = {
      vocabulary: '词汇',
      listening: '听力',
      reading: '阅读',
      writing: '写作',
      mock: '模拟考试',
      random: '随机'
    };

    return modeTexts[this.data.mode] || '';
  }
}); 