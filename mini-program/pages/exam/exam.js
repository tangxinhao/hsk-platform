// pages/exam/exam.js
const app = getApp()

Page({
  data: {
    level: 1,
    questions: [],
    currentIndex: 0,
    currentQuestion: null,
    options: [],
    answers: {},
    totalQuestions: 0,
    startTime: null,
    remainingTime: '00:00',
    timer: null,
    duration: 40, // 分钟
    audioContext: null,
    isPlaying: false,
    currentAnswerText: '',
    currentAnswerLength: 0
  },

  onLoad(options) {
    const level = parseInt(options.level) || 1
    this.setData({ level })
    this.loadExamQuestions()
    this.initAudio()
  },
  
  onUnload() {
    if (this.data.timer) clearInterval(this.data.timer)
    if (this.data.audioContext) {
      this.data.audioContext.stop()
      this.data.audioContext.destroy()
    }
  },

  // 加载考试题目
  loadExamQuestions() {
    const { level } = this.data
    
    wx.showLoading({ title: '加载中...' })
    
    app.globalData.request({
      url: '/question/questions/',
      data: {
        level: level,
        page_size: 100  // 获取足够数量的题目
      }
    })
      .then((res) => {
        const questions = res.results || res || []
        
        if (questions.length === 0) {
          wx.showModal({
            title: '提示',
            content: '暂无可用题目',
            showCancel: false,
            success: () => wx.navigateBack()
          })
          return
        }
        
        this.setData({
          questions: questions,
          totalQuestions: questions.length,
          startTime: Date.now()
        })
        
        this.loadQuestion(0)
        this.startTimer()
        wx.hideLoading()
      })
      .catch((err) => {
        console.error('加载题目失败:', err)
        wx.hideLoading()
        wx.navigateBack()
      })
  },

  // 判断是否是图片URL
  isImageUrl(str) {
    if (!str || typeof str !== 'string') return false
    return str.startsWith('http') || str.startsWith('/media/') || 
           str.match(/\.(jpg|jpeg|png|gif|webp)$/i)
  },

  // 加载指定题目
  loadQuestion(index) {
    const question = this.data.questions[index]
    let options = []
    
    if (question.options) {
      try {
        // options可能是数组/字符串/对象
        let rawOptions = Array.isArray(question.options) ? question.options : 
                        (typeof question.options === 'string' ? JSON.parse(question.options) : question.options)
        rawOptions = Array.isArray(rawOptions) ? rawOptions : (rawOptions?.options || [])
        const baseUrl = app.globalData.apiBaseUrl.replace('/api', '')
        
        // 转换选项为对象格式，包含值和类型标记
        const optionType = question.option_type
        options = rawOptions.map((opt, idx) => {
          const letter = String.fromCharCode(65 + idx)
          const value = typeof opt === 'string'
            ? opt
            : (opt?.value || opt?.url || opt?.text || opt?.label || '')
          
          const isImage = optionType === 'image' || this.isImageUrl(value)
          const finalValue = isImage && value && !value.startsWith('http')
            ? `${baseUrl}${value}`
            : value
          
          return {
            value: finalValue,
            isImage: isImage,
            letter
          }
        })
      } catch (e) {
        console.error('解析选项失败:', e)
        options = []
      }
    }
    
    // 如果题目内容包含图片URL，也需要处理
    if (question.image_url && !question.image_url.startsWith('http')) {
      const baseUrl = app.globalData.apiBaseUrl.replace('/api', '')
      question.image_url = `${baseUrl}${question.image_url}`
    }
    
    // 获取当前题目的已输入答案
    const currentAnswer = this.data.answers[index] || ''
    
    this.setData({
      currentIndex: index,
      currentQuestion: question,
      options: options,
      currentAnswerText: currentAnswer,
      currentAnswerLength: currentAnswer.length || 0
    })
    
    // 预加载图片选项，避免外链图片无法显示
    this.preloadOptionImages(options)
  },

  // 预加载图片选项，失败则保留原URL
  preloadOptionImages(options) {
    const imageOptions = options
      .map((opt, index) => ({ opt, index }))
      .filter(item => item.opt.isImage && item.opt.value)
    
    if (imageOptions.length === 0) return
    
    const fs = wx.getFileSystemManager()
    const tasks = imageOptions.map(({ opt, index }) => {
      return new Promise((resolve) => {
        wx.downloadFile({
          url: opt.value,
          success: (res) => {
            if (res.statusCode === 200 && res.tempFilePath) {
              const ext = (opt.value.match(/\.(jpg|jpeg|png|gif|webp|bmp)$/i) || ['.jpg'])[0]
              const filePath = `${wx.env.USER_DATA_PATH}/opt_exam_${this.data.currentIndex || 0}_${index}${ext}`
              fs.saveFile({
                tempFilePath: res.tempFilePath,
                filePath,
                success: (saveRes) => {
                  options[index] = { ...opt, value: saveRes.savedFilePath }
                  resolve()
                },
                fail: () => {
                  options[index] = { ...opt, value: res.tempFilePath }
                  resolve()
                }
              })
              return
            }
            resolve()
          },
          fail: () => resolve()
        })
      })
    })
    
    Promise.all(tasks).then(() => {
      this.setData({ options })
    })
  },

  // 开始计时
  startTimer() {
    const { duration } = this.data
    let totalSeconds = duration * 60
    
    const timer = setInterval(() => {
      totalSeconds--
      
      if (totalSeconds <= 0) {
        clearInterval(timer)
        this.submitExam()
        return
      }
      
      const minutes = Math.floor(totalSeconds / 60)
      const seconds = totalSeconds % 60
      const timeText = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
      
      this.setData({ remainingTime: timeText })
    }, 1000)
    
    this.setData({ timer })
  },

  // 初始化音频
  initAudio() {
    const audioContext = wx.createInnerAudioContext()
    audioContext.onPlay(() => this.setData({ isPlaying: true }))
    audioContext.onPause(() => this.setData({ isPlaying: false }))
    audioContext.onEnded(() => this.setData({ isPlaying: false }))
    this.setData({ audioContext })
  },

  // 播放音频
  toggleAudio() {
    const { audioContext, currentQuestion, isPlaying } = this.data
    const app = getApp()
    if (!audioContext || !currentQuestion.audio_url) return
    
    if (isPlaying) {
      audioContext.pause()
    } else {
      const baseUrl = app.globalData.apiBaseUrl.replace('/api', '')
      const url = currentQuestion.audio_url.startsWith('http') 
        ? currentQuestion.audio_url 
        : `${baseUrl}${currentQuestion.audio_url}`
      audioContext.src = url
      audioContext.play()
    }
  },

  // 选择答案
  selectAnswer(e) {
    const { value, letter } = e.currentTarget.dataset
    const { currentIndex, answers, options } = this.data
    
    // 对于图片选项，保存选项字母（A/B/C/D），而不是URL
    if (options.length > 0 && options[0].isImage) {
      // 图片选项，保存字母
      answers[currentIndex] = letter
    } else {
      // 文字选项，保存内容
      answers[currentIndex] = value
    }
    this.setData({ answers })
  },

  // 输入答案（填空题、写作题）
  onAnswerInput(e) {
    const { currentIndex, answers } = this.data
    const value = e.detail.value
    answers[currentIndex] = value
    this.setData({ 
      answers,
      currentAnswerText: value,
      currentAnswerLength: value.length || 0
    })
  },

  // 上一题
  prevQuestion() {
    const { currentIndex } = this.data
    if (currentIndex > 0) {
      this.loadQuestion(currentIndex - 1)
    }
  },

  // 下一题
  nextQuestion() {
    const { currentIndex, totalQuestions } = this.data
    
    if (currentIndex < totalQuestions - 1) {
      this.loadQuestion(currentIndex + 1)
    } else {
      // 交卷
      wx.showModal({
        title: '确认交卷',
        content: '确定要提交试卷吗？',
        success: (res) => {
          if (res.confirm) {
            this.submitExam()
          }
        }
      })
    }
  },

  // 提交考试
  submitExam() {
    if (this.data.timer) clearInterval(this.data.timer)
    
    wx.showLoading({ title: '提交中...' })
    
    const { questions, answers, level, startTime } = this.data
    let correct = 0
    let total = 0
    
    // 计算分数
    questions.forEach((q, index) => {
      if (answers[index]) {
        total++
        if (answers[index] === q.answer) {
          correct++
        }
      }
    })
    
    const score = total > 0 ? Math.round((correct / total) * 100) : 0
    const duration = Math.floor((Date.now() - startTime) / 1000 / 60)
    
    // 保存考试记录
    const examRecord = {
      id: Date.now(),
      level: level,
      score: score,
      correct: correct,
      total: total,
      duration: duration,
      date: new Date().toLocaleString('zh-CN')
    }
    
    const history = wx.getStorageSync('examHistory') || []
    history.unshift(examRecord)
    wx.setStorageSync('examHistory', history.slice(0, 20))
    
    wx.hideLoading()
    
    // 跳转到结果页
    wx.redirectTo({
      url: `/pages/exam/result?id=${examRecord.id}`
    })
  },

  getLetter(index) {
    return String.fromCharCode(65 + index)
  }
})
