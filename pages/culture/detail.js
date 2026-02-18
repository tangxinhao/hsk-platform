Page({
  data: {
    articleId: null,
    article: null,
    loading: true,
    comments: [],
    showComments: false,
    userComment: '',
    isCollected: false,
    relatedArticles: []
  },

  onLoad: function (options) {
    if (options.id) {
      this.setData({
        articleId: options.id,
        loading: true
      })
      this.fetchArticleDetail(options.id)
      this.checkIfCollected(options.id)
      this.fetchRelatedArticles(options.id)
    }
  },

  fetchArticleDetail: function (id) {
    // 模拟API请求
    setTimeout(() => {
      // 模拟数据
      const article = {
        id: id,
        title: "中国传统节日 - 春节",
        author: "文化研究员",
        publishDate: "2023-05-15",
        viewCount: 1254,
        content: "春节，即中国农历新年，是中国最重要的传统节日之一。春节历史悠久，起源于殷商时期年头岁尾的祭神祭祖活动。按照中国农历，正月初一是新年的开始，人们认为新的一年开启了新的开始，寄托了美好的期望。\n\n春节的习俗包括贴春联、贴窗花、贴年画、守岁、吃年夜饭、燃放爆竹、拜年、发红包等。这些习俗寄托了中国人对新一年的期许和祝福。\n\n在现代社会，虽然春节的某些习俗已经发生了变化，但其核心精神仍然是团圆、和睦、祥和，表达了人们对美好生活的向往和追求。每年春节，无论身在何处，中国人都会想方设法回家团聚，共度新春佳节。",
        coverImage: "/images/culture/spring_festival.jpg",
        tags: ["传统节日", "民俗文化", "春节"],
        level: "初级"
      }

      this.setData({
        article: article,
        loading: false
      })

      // 模拟获取评论
      this.fetchComments(id)
    }, 1000)
  },

  fetchComments: function (id) {
    // 模拟API请求
    setTimeout(() => {
      // 模拟评论数据
      const comments = [
        {
          id: 1,
          user: {
            name: "李明",
            avatar: "/images/avatars/user1.png"
          },
          content: "写得非常好，让我了解了很多关于春节的习俗！",
          time: "2023-05-16 14:30"
        },
        {
          id: 2,
          user: {
            name: "张华",
            avatar: "/images/avatars/user2.png"
          },
          content: "作为一个外国留学生，这篇文章帮我理解了为什么春节对中国人如此重要",
          time: "2023-05-16 15:45"
        }
      ]

      this.setData({
        comments: comments
      })
    }, 1500)
  },

  fetchRelatedArticles: function (currentId) {
    // 模拟API请求
    setTimeout(() => {
      // 模拟相关文章
      const relatedArticles = [
        {
          id: parseInt(currentId) + 1,
          title: "中国传统节日 - 中秋节",
          coverImage: "/images/culture/mid_autumn.jpg",
          summary: "中秋节，是中国传统的重要节日之一，为每年的农历八月十五..."
        },
        {
          id: parseInt(currentId) + 2,
          title: "中国传统节日 - 端午节",
          coverImage: "/images/culture/dragon_boat.jpg",
          summary: "端午节是中国古老的传统节日之一，起源于中国先秦时期..."
        }
      ]

      this.setData({
        relatedArticles: relatedArticles
      })
    }, 1800)
  },

  toggleComments: function () {
    this.setData({
      showComments: !this.data.showComments
    })
  },

  inputComment: function (e) {
    this.setData({
      userComment: e.detail.value
    })
  },

  submitComment: function () {
    if (!this.data.userComment.trim()) {
      wx.showToast({
        title: '评论不能为空',
        icon: 'none'
      })
      return
    }

    // 模拟提交评论
    wx.showLoading({
      title: '提交中...',
    })

    setTimeout(() => {
      // 创建新评论
      const newComment = {
        id: this.data.comments.length + 1,
        user: {
          name: "我",
          avatar: "/images/avatars/default.png"
        },
        content: this.data.userComment,
        time: new Date().toLocaleString()
      }

      // 更新评论列表
      this.setData({
        comments: [newComment, ...this.data.comments],
        userComment: ''
      })

      wx.hideLoading()
      wx.showToast({
        title: '评论成功',
      })
    }, 500)
  },

  toggleCollect: function () {
    const isCollected = !this.data.isCollected
    this.setData({ isCollected })

    if (isCollected) {
      wx.showToast({
        title: '收藏成功',
        icon: 'success'
      })
      // 这里可以调用API保存收藏状态
    } else {
      wx.showToast({
        title: '取消收藏',
        icon: 'none'
      })
      // 这里可以调用API删除收藏
    }
  },

  checkIfCollected: function (id) {
    // 模拟检查是否已收藏
    // 实际应用中应从本地存储或服务器获取数据
    this.setData({
      isCollected: Math.random() > 0.5
    })
  },

  viewRelatedArticle: function (e) {
    const id = e.currentTarget.dataset.id
    wx.redirectTo({
      url: `/pages/culture/detail?id=${id}`
    })
  },

  onShareAppMessage: function () {
    return {
      title: this.data.article?.title || '中国文化精选文章',
      path: `/pages/culture/detail?id=${this.data.articleId}`
    }
  }
}) 