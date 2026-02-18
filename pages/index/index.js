const app = getApp()

Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),

    // 轮播图
    bannerList: [
      {
        id: 1,
        image: '/images/banner/banner1.jpg',
        url: '/pages/hsk/hsk',
        title: 'HSK考试备考'
      },
      {
        id: 2,
        image: '/images/banner/banner2.jpg',
        url: '/pages/culture/culture',
        title: '探索中国文化'
      },
      {
        id: 3,
        image: '/images/banner/banner3.jpg',
        url: '/pages/university/university',
        title: '留学院校推荐'
      }
    ],

    // 功能入口
    entranceList: [
      {
        id: 1,
        title: 'HSK练习',
        url: '/pages/hsk/hsk'
      },
      {
        id: 2,
        title: '中国文化',
        url: '/pages/culture/culture'
      },
      {
        id: 3,
        title: '院校推荐',
        url: '/pages/university/university'
      },
      {
        id: 4,
        title: '词汇学习',
        url: '/pages/hsk/hsk'
      },
      {
        id: 5,
        title: '听力练习',
        url: '/pages/hsk/hsk'
      },
      {
        id: 6,
        title: '写作练习',
        url: '/pages/hsk/hsk'
      }
    ],

    // 最近学习
    recentLearning: [],

    // 学习统计
    learningStats: {
      totalTime: 0,
      daysStreak: 0,
      wordsLearned: 0,
      exercisesCompleted: 0
    },

    // 推荐内容
    recommendedContent: [],

    // 学习提示
    studyTips: [
      "每天坚持学习30分钟，比一次学习3小时效果更好",
      "复习是记忆的关键，每周至少复习一次学过的内容",
      "结合实际场景使用汉语，加深记忆和理解",
      "听力练习时，先理解大意，再关注细节",
      "写汉字时注意笔顺，有助于记忆和书写美观"
    ],
    currentTip: 0,

    // 今日目标
    dailyGoal: {
      minutes: 30,
      completed: 0,
      percentage: 0
    }
  },

  onLoad: function () {
    console.log("首页加载中...");

    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    }

    // 获取最近学习数据
    this.getRecentLearning();

    // 获取学习统计
    this.getLearningStats();

    // 获取推荐内容
    this.getRecommendedContent();

    // 获取今日目标
    this.getDailyGoal();

    // 定时切换学习提示
    this.startTipInterval();
  },

  onShow: function () {
    console.log("首页显示，已应用新的样式和布局");
  },

  getUserInfo: function (e) {
    console.log("获取用户信息", e);
    if (e.detail.userInfo) {
      app.globalData.userInfo = e.detail.userInfo
      this.setData({
        userInfo: e.detail.userInfo,
        hasUserInfo: true
      })
    }
  },

  getRecentLearning: function () {
    // 模拟获取最近学习数据
    setTimeout(() => {
      this.setData({
        recentLearning: [
          {
            id: 1,
            title: 'HSK3级词汇练习',
            progress: 60,
            lastTime: '2025-06-29'
          },
          {
            id: 2,
            title: '中国传统节日',
            progress: 40,
            lastTime: '2025-06-28'
          },
          {
            id: 3,
            title: '听力理解训练',
            progress: 25,
            lastTime: '2025-06-27'
          }
        ]
      });
      console.log("已加载最近学习数据");
    }, 500);
  },

  getLearningStats: function () {
    // 模拟获取学习统计数据
    setTimeout(() => {
      this.setData({
        learningStats: {
          totalTime: 12.5, // 小时
          daysStreak: 7,
          wordsLearned: 320,
          exercisesCompleted: 48
        }
      });
      console.log("已加载学习统计数据");
    }, 600);
  },

  getRecommendedContent: function () {
    // 模拟获取推荐内容
    setTimeout(() => {
      this.setData({
        recommendedContent: [
          {
            id: 1,
            title: 'HSK4级常见语法点总结',
            type: '学习资料',
            image: '/images/content/grammar.jpg',
            url: '/pages/article/article?id=1'
          },
          {
            id: 2,
            title: '中国茶文化探索',
            type: '文化知识',
            image: '/images/content/tea.jpg',
            url: '/pages/culture/detail?id=5'
          },
          {
            id: 3,
            title: '北京语言大学介绍',
            type: '院校推荐',
            image: '/images/content/blcu.jpg',
            url: '/pages/university/detail?id=10'
          }
        ]
      });
    }, 700);
  },

  getDailyGoal: function () {
    // 模拟获取今日目标
    setTimeout(() => {
      const completed = 18; // 已完成的分钟数
      const minutes = 30; // 目标分钟数
      const percentage = Math.min(Math.round((completed / minutes) * 100), 100);

      this.setData({
        dailyGoal: {
          minutes: minutes,
          completed: completed,
          percentage: percentage
        }
      });
      console.log("已加载今日目标数据");
    }, 800);
  },

  startTipInterval: function () {
    // 每8秒切换一次学习提示
    this.tipInterval = setInterval(() => {
      let nextTip = this.data.currentTip + 1;
      if (nextTip >= this.data.studyTips.length) {
        nextTip = 0;
      }

      this.setData({
        currentTip: nextTip
      });
    }, 8000);
    console.log("已启动学习提示轮播");
  },

  onUnload: function () {
    // 清除定时器
    if (this.tipInterval) {
      clearInterval(this.tipInterval);
    }
  },

  navigateTo: function (e) {
    const url = e.currentTarget.dataset.url;
    console.log("跳转到", url);
    wx.navigateTo({
      url: url
    })
  },

  viewAllLearning: function () {
    console.log("查看全部学习记录");
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    });
  },

  viewAllRecommended: function () {
    wx.navigateTo({
      url: '/pages/recommended/list'
    })
  }
}) 