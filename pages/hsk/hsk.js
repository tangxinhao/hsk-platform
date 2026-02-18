const app = getApp()

Page({
  data: {
    currentTab: 0,
    levelList: [
      { id: 1, name: 'HSK1' },
      { id: 2, name: 'HSK2' },
      { id: 3, name: 'HSK3' },
      { id: 4, name: 'HSK4' },
      { id: 5, name: 'HSK5' },
      { id: 6, name: 'HSK6' }
    ],
    questionTypes: [
      { id: 1, name: '单选题', icon: '/images/icons/single_choice.png' },
      { id: 2, name: '多选题', icon: '/images/icons/multiple_choice.png' },
      { id: 3, name: '判断题', icon: '/images/icons/judgment.png' },
      { id: 4, name: '填空题', icon: '/images/icons/fill_blank.png' },
      { id: 5, name: '阅读理解', icon: '/images/icons/reading.png' }
    ],
    wrongBookCount: 0,
    dailyPracticeProgress: 60
  },

  onLoad: function (options) {
    // 获取错题本数量
    this.getWrongBookCount();
  },

  // 切换标签
  changeTab: function (e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      currentTab: index
    });
  },

  // 获取错题本数量
  getWrongBookCount: function () {
    // 模拟获取错题本数量
    setTimeout(() => {
      this.setData({
        wrongBookCount: 12
      });
    }, 500);
  },

  // 跳转到练习页面
  startPractice: function (e) {
    const type = e.currentTarget.dataset.type;
    const level = this.data.levelList[this.data.currentTab].id;

    wx.navigateTo({
      url: `/pages/practice/practice?type=${type}&level=${level}`
    });
  },

  // 进入错题本
  goToWrongBook: function () {
    wx.navigateTo({
      url: '/pages/wrong-book/wrong-book'
    });
  },

  // 继续每日练习
  continueDailyPractice: function () {
    wx.navigateTo({
      url: '/pages/daily-practice/daily-practice'
    });
  }
}) 