// pages/user/dashboard/dashboard.js
import * as echarts from '../../../components/ec-canvas/echarts';

Page({
  data: {
    userInfo: {},
    studyGoal: null,
    basicStats: {
      total_practice: 0,
      accuracy_rate: 0,
      study_days: 0,
      total_study_time: 0
    },
    categoryPerformance: [],
    recentActivities: [],
    wrongCount: 0,
    selectedDays: 7,
    practiceChart: {
      onInit: null
    }
  },

  onLoad() {
    this.loadUserInfo();
    this.loadDashboardData();
    this.initChart();
  },

  onShow() {
    // 每次显示页面时刷新数据
    this.loadDashboardData();
  },

  loadUserInfo() {
    // 从本地存储或全局数据获取用户信息
    const userInfo = wx.getStorageSync('userInfo');
    if (userInfo) {
      this.setData({ userInfo });
    }
  },

  loadDashboardData() {
    wx.showLoading({ title: '加载中...' });
    
    // 验证token
    const token = wx.getStorageSync('token');
    if (!token) {
      wx.hideLoading();
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      setTimeout(() => {
        wx.navigateTo({
          url: '/pages/login/login'
        });
      }, 1500);
      return;
    }
    
    // 验证API地址
    const apiBaseUrl = getApp().globalData.apiBaseUrl;
    if (!apiBaseUrl) {
      wx.hideLoading();
      wx.showToast({
        title: '系统配置错误',
        icon: 'none'
      });
      return;
    }
    
    wx.request({
      url: `${apiBaseUrl}/user/dashboard/`,
      method: 'GET',
      header: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      data: {
        days: this.data.selectedDays
      },
      timeout: 15000,  // 15秒超时
      success: (res) => {
        if (res.statusCode === 200) {
          // 验证响应数据
          if (!res.data || typeof res.data !== 'object') {
            wx.showToast({
              title: '数据格式错误',
              icon: 'none'
            });
            return;
          }
          
          const data = res.data;
          
          // 安全地设置数据，提供默认值
          this.setData({
            studyGoal: data.study_goal || null,
            basicStats: data.basic_stats || {
              total_practice: 0,
              accuracy_rate: 0,
              study_days: 0,
              total_study_time: 0
            },
            categoryPerformance: Array.isArray(data.category_performance) ? data.category_performance : [],
            recentActivities: Array.isArray(data.recent_activities) ? data.recent_activities : [],
            wrongCount: data.wrong_count || 0
          });
          
          // 更新图表
          if (data.trends) {
            this.updateChart(data.trends);
          }
        } else if (res.statusCode === 401) {
          wx.showToast({
            title: '登录已过期',
            icon: 'none'
          });
          setTimeout(() => {
            wx.navigateTo({
              url: '/pages/login/login'
            });
          }, 1500);
        } else {
          wx.showToast({
            title: '加载失败',
            icon: 'none'
          });
        }
      },
      fail: (err) => {
        console.error('加载Dashboard数据失败:', err);
        wx.showToast({
          title: '网络错误',
          icon: 'none'
        });
      },
      complete: () => {
        wx.hideLoading();
      }
    });
  },

  initChart() {
    this.setData({
      practiceChart: {
        onInit: this.initPracticeChart
      }
    });
  },

  initPracticeChart(canvas, width, height, dpr) {
    const chart = echarts.init(canvas, null, {
      width: width,
      height: height,
      devicePixelRatio: dpr
    });
    
    canvas.setChart(chart);
    
    // 初始空数据
    const option = {
      tooltip: {
        trigger: 'axis',
        confine: true
      },
      legend: {
        data: ['练习次数', '正确率'],
        top: 10
      },
      grid: {
        top: 50,
        left: 40,
        right: 30,
        bottom: 30
      },
      xAxis: {
        type: 'category',
        data: [],
        axisLabel: {
          fontSize: 10
        }
      },
      yAxis: [
        {
          type: 'value',
          name: '次数',
          axisLabel: {
            fontSize: 10
          }
        },
        {
          type: 'value',
          name: '正确率(%)',
          axisLabel: {
            fontSize: 10
          }
        }
      ],
      series: [
        {
          name: '练习次数',
          type: 'bar',
          data: [],
          itemStyle: {
            color: '#409EFF'
          }
        },
        {
          name: '正确率',
          type: 'line',
          yAxisIndex: 1,
          data: [],
          smooth: true,
          itemStyle: {
            color: '#67C23A'
          }
        }
      ]
    };
    
    chart.setOption(option);
    
    return chart;
  },

  updateChart(trends) {
    // 验证trends数据
    if (!trends || typeof trends !== 'object') {
      console.warn('trends数据无效');
      return;
    }
    
    // 验证必要字段
    if (!Array.isArray(trends.dates) || 
        !Array.isArray(trends.practice_count) || 
        !Array.isArray(trends.accuracy_rate)) {
      console.warn('trends数据格式不正确');
      return;
    }
    
    const chart = this.selectComponent('#practice-chart');
    if (chart && chart.chart) {
      try {
        chart.chart.setOption({
          xAxis: {
            data: trends.dates
          },
          series: [
            {
              data: trends.practice_count
            },
            {
              data: trends.accuracy_rate
            }
          ]
        });
      } catch (error) {
        console.error('更新图表失败:', error);
      }
    }
  },

  changeDays(e) {
    const days = parseInt(e.currentTarget.dataset.days);
    this.setData({ selectedDays: days });
    this.loadDashboardData();
  },

  navigateToSetGoal() {
    wx.navigateTo({
      url: '/pages/user/set-goal/set-goal'
    });
  },

  navigateTo(e) {
    const url = e.currentTarget.dataset.url;
    wx.navigateTo({ url });
  },

  formatTime(timeStr) {
    // 验证输入
    if (!timeStr) {
      return '';
    }
    
    try {
      const date = new Date(timeStr);
      
      // 验证日期是否有效
      if (isNaN(date.getTime())) {
        return '';
      }
      
      const now = new Date();
      const diff = now - date;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (minutes < 1) {
      return '刚刚';
    } else if (minutes < 60) {
      return `${minutes}分钟前`;
    } else if (hours < 24) {
      return `${hours}小时前`;
    } else if (days < 7) {
      return `${days}天前`;
    } else {
      return `${date.getMonth() + 1}-${date.getDate()}`;
    }
    } catch (error) {
      console.error('格式化时间失败:', error);
      return '';
    }
  },

  onShareAppMessage() {
    return {
      title: 'HSK学习助手 - 我的学习Dashboard',
      path: '/pages/index/index'
    };
  }
});
