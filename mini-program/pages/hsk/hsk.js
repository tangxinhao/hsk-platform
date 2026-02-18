// pages/hsk/hsk.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    levels: [
      { id: 1, name: 'HSK 1级' },
      { id: 2, name: 'HSK 2级' },
      { id: 3, name: 'HSK 3级' },
      { id: 4, name: 'HSK 4级' },
      { id: 5, name: 'HSK 5级' },
      { id: 6, name: 'HSK 6级' }
    ],
    activeLevel: 1,
    questionTypes: [
      { id: 'single', name: '单选题', icon: '../../images/tab-home.png' },
      { id: 'multiple', name: '多选题', icon: '../../images/tab-home.png' },
      { id: 'judge', name: '判断题', icon: '../../images/tab-home.png' },
      { id: 'fill', name: '填空题', icon: '../../images/tab-home.png' }
    ],
    dailyProgress: 30,
    wrongCount: 15
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  },

  switchLevel(e) {
    const level = e.currentTarget.dataset.level;
    this.setData({
      activeLevel: level
    });
  },

  startPractice(e) {
    const type = e.currentTarget.dataset.type;
    const level = this.data.activeLevel;
    wx.navigateTo({
      url: `/pages/question/practice?type=${type}&level=${level}`
    });
  },

  continueDailyPractice() {
    wx.navigateTo({
      url: '/pages/daily/daily'
    });
  },

  goToWrongBook() {
    wx.navigateTo({
      url: '/pages/wrong-book/wrong-book'
    });
  }
})