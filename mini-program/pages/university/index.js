Page({
  data: {
    universities: []
  },
  onLoad() {
    wx.request({
      url: 'http://127.0.0.1:8000/api/university/',
      method: 'GET',
      success: (res) => {
        this.setData({ universities: res.data });
      },
      fail: (err) => {
        wx.showToast({ title: '接口请求失败', icon: 'none' });
      }
    });
  }
}); 