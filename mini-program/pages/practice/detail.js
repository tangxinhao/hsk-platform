// pages/practice/detail.js
const app = getApp()

Page({
  data: {
    questionId: null,
    level: 1,
    currentIndex: 0,
    total: 1,
    question: {},
    options: [],
    userAnswer: null,
    submitted: false,
    isCorrect: false,
    loading: false,
    // 音频相关
    audioContext: null,
    isPlaying: false
  },

  onLoad(options) {
    const { id, level, index } = options
    this.setData({
      questionId: parseInt(id),
      level: parseInt(level) || 1,
      currentIndex: parseInt(index) || 0
    })
    this.loadQuestion()
    this.initAudio()
  },
  
  onUnload() {
    // 清理音频资源
    if (this.data.audioContext) {
      this.data.audioContext.stop()
      this.data.audioContext.destroy()
    }
  },

  // 加载题目
  loadQuestion() {
    const { questionId } = this.data
    
    this.setData({ loading: true })
    
    app.globalData.request({
      url: `/question/questions/${questionId}/`
    })
      .then((res) => {
        // 解析选项
        let options = []
        if (res.options) {
          try {
            // options可能是数组/字符串/对象
            let rawOptions = Array.isArray(res.options) ? res.options : 
                            (typeof res.options === 'string' ? JSON.parse(res.options) : res.options)
            rawOptions = Array.isArray(rawOptions) ? rawOptions : (rawOptions?.options || [])
            
            const baseUrl = app.globalData.apiBaseUrl.replace('/api', '')
            const optionType = res.option_type
            
            // 转换选项为对象格式，包含值和类型标记
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
            console.error('解析选项失败:', e, res.options)
            options = []
          }
        }
        
        // 如果题目内容包含图片URL，也需要处理
        if (res.image_url && !res.image_url.startsWith('http')) {
          const baseUrl = app.globalData.apiBaseUrl.replace('/api', '')
          res.image_url = `${baseUrl}${res.image_url}`
        }
        
        this.setData({
          question: res,
          options: options,
          loading: false,
          userAnswer: null,
          submitted: false
        })
        
        // 预加载图片选项，避免外链图片无法显示
        this.preloadOptionImages(options)
        
        // 如果有音频，设置音频源
        if (res.audio_url) {
          this.setAudioSrc(res.audio_url)
        }
      })
      .catch((err) => {
        console.error('加载题目失败:', err)
        this.setData({ loading: false })
      })
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
              const filePath = `${wx.env.USER_DATA_PATH}/opt_${this.data.questionId || 'q'}_${index}${ext}`
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

  // 初始化音频
  initAudio() {
    const audioContext = wx.createInnerAudioContext()
    
    audioContext.onPlay(() => {
      this.setData({ isPlaying: true })
    })
    
    audioContext.onPause(() => {
      this.setData({ isPlaying: false })
    })
    
    audioContext.onEnded(() => {
      this.setData({ isPlaying: false })
    })
    
    audioContext.onError((err) => {
      console.error('音频播放失败:', err)
      wx.showToast({
        title: '音频播放失败',
        icon: 'none'
      })
    })
    
    this.setData({ audioContext })
  },

  // 设置音频源
  setAudioSrc(url) {
    const { audioContext } = this.data
    const app = getApp()
    if (audioContext && url) {
      // 如果是相对路径，拼接完整URL
      const baseUrl = app.globalData.apiBaseUrl.replace('/api', '')
      const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url}`
      audioContext.src = fullUrl
    }
  },

  // 播放/暂停音频
  toggleAudio() {
    const { audioContext, isPlaying } = this.data
    if (!audioContext) return
    
    if (isPlaying) {
      audioContext.pause()
    } else {
      audioContext.play()
    }
  },

  // 判断是否是图片URL
  isImageUrl(str) {
    if (!str || typeof str !== 'string') return false
    // 检查是否是图片URL（http开头、/media/开头、或以图片扩展名结尾）
    return str.startsWith('http') || str.startsWith('/media/') || 
           str.match(/\.(jpg|jpeg|png|gif|webp|bmp)$/i)
  },

  // 选择选项
  selectOption(e) {
    if (this.data.submitted) return
    
    const { value, letter } = e.currentTarget.dataset
    // 对于图片选项，保存选项字母（A/B/C/D），而不是URL
    const { options } = this.data
    if (options.length > 0 && options[0].isImage) {
      // 图片选项，保存字母
      this.setData({ userAnswer: letter })
    } else {
      // 文字选项，保存内容
      this.setData({ userAnswer: value })
    }
  },

  // 输入答案（填空题、写作题）
  onAnswerInput(e) {
    this.setData({ userAnswer: e.detail.value })
  },

  // 提交答案
  submitAnswer() {
    const { userAnswer, question } = this.data
    
    if (!userAnswer || (typeof userAnswer === 'string' && !userAnswer.trim())) {
      wx.showToast({
        title: '请输入或选择答案',
        icon: 'none'
      })
      return
    }
    
    // 对于填空题和写作题，进行简单的答案比对（去除首尾空格）
    const normalizedUserAnswer = typeof userAnswer === 'string' ? userAnswer.trim() : userAnswer
    const normalizedCorrectAnswer = typeof question.answer === 'string' ? question.answer.trim() : question.answer
    const isCorrect = normalizedUserAnswer === normalizedCorrectAnswer
    
    this.setData({
      submitted: true,
      isCorrect: isCorrect
    })
    
    // 提交答案到服务器
    this.submitToServer(userAnswer, isCorrect)
    
    // 保存到本地统计（作为备份）
    this.saveStatistics(isCorrect)
    
    // 如果答错，加入错题本
    if (!isCorrect) {
      this.addToWrongBook()
    }
  },
  
  // 提交答案到服务器
  submitToServer(userAnswer, isCorrect) {
    const { question } = this.data
    const token = wx.getStorageSync('token')
    
    // 只有登录用户才提交到服务器
    if (!token) return
    
    app.globalData.request({
      url: '/question/answer/',
      method: 'POST',
      data: {
        question_id: question.id,
        user_answer: userAnswer
      }
    }).then(res => {
      console.log('答案已保存到服务器')
    }).catch(err => {
      console.error('保存答案失败:', err)
      // 服务器保存失败不影响本地使用
    })
  },

  // 保存统计
  saveStatistics(isCorrect) {
    // 统计相关数据全部由后端 AnswerRecord 维护，这里不再使用本地存储，避免与服务器统计不一致
    // 保留此函数以便后续扩展（例如本地动画、成就提示等）
  },

  // 加入错题本
  addToWrongBook() {
    const { question } = this.data
    const wrongBook = wx.getStorageSync('wrongBook') || []
    
    // 避免重复添加
    if (!wrongBook.find(q => q.id === question.id)) {
      wrongBook.unshift({
        id: question.id,
        content: question.content,
        type: question.type_display,
        level: question.level,
        wrongTime: new Date().getTime()
      })
      wx.setStorageSync('wrongBook', wrongBook)
    }
  },

  // 上一题
  prevQuestion() {
    const { currentIndex } = this.data
    if (currentIndex > 0) {
      // 这里应该从列表页传入所有题目ID，然后切换
      wx.navigateBack()
    }
  },

  // 下一题
  nextQuestion() {
    const { currentIndex, total } = this.data
    if (currentIndex < total - 1) {
      // 加载下一题
      wx.navigateBack()
    } else {
      // 完成练习
      wx.showModal({
        title: '练习完成',
        content: '恭喜完成本次练习！',
        showCancel: false,
        success: () => {
          wx.navigateBack({ delta: 2 })
        }
      })
    }
  },

  // 预览图片
  previewImage() {
    const { question } = this.data
    const app = getApp()
    if (question.image_url) {
      const baseUrl = app.globalData.apiBaseUrl.replace('/api', '')
      const url = question.image_url.startsWith('http') 
        ? question.image_url 
        : `${baseUrl}${question.image_url}`
      
      wx.previewImage({
        urls: [url],
        current: url
      })
    }
  },

  // 获取选项字母
  getLetter(index) {
    return String.fromCharCode(65 + index)
  }
})
