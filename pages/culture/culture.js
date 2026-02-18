Page({
  data: {
    currentTab: 0,
    categoryList: [],
    contentList: [],
    loading: true
  },

  onLoad: function (options) {
    this.fetchCategories();
  },

  // 获取文化分类
  fetchCategories: function () {
    // 模拟数据获取
    setTimeout(() => {
      const categories = [
        { id: 1, name: '传统节日', level: '初级' },
        { id: 2, name: '中国美食', level: '初级' },
        { id: 3, name: '传统服饰', level: '中级' },
        { id: 4, name: '建筑艺术', level: '中级' },
        { id: 5, name: '诗词歌赋', level: '高级' }
      ];

      this.setData({
        categoryList: categories,
        loading: false
      });

      // 默认加载第一个分类的内容
      if (categories.length > 0) {
        this.fetchContentList(categories[0].id);
      }
    }, 500);
  },

  // 获取分类下的内容列表
  fetchContentList: function (categoryId) {
    this.setData({ loading: true });

    // 模拟数据获取
    setTimeout(() => {
      const contentList = [
        {
          id: 1,
          title: '春节的由来与传统习俗',
          coverImage: '/images/culture/spring_festival.jpg',
          summary: '春节是中国最重要的传统节日，有着悠久的历史和丰富的习俗...',
          viewCount: 1234,
          categoryId: 1
        },
        {
          id: 2,
          title: '元宵节的灯笼制作与传说',
          coverImage: '/images/culture/lantern_festival.jpg',
          summary: '元宵节是农历正月十五，这一天人们会赏灯、猜灯谜、吃汤圆...',
          viewCount: 986,
          categoryId: 1
        },
        {
          id: 3,
          title: '端午节与屈原的故事',
          coverImage: '/images/culture/dragon_boat_festival.jpg',
          summary: '端午节与爱国诗人屈原有着深厚的渊源，这一天有吃粽子、赛龙舟等习俗...',
          viewCount: 876,
          categoryId: 1
        }
      ];

      // 根据分类ID筛选内容
      const filteredContent = contentList.filter(item => item.categoryId === categoryId);

      this.setData({
        contentList: filteredContent,
        loading: false
      });
    }, 500);
  },

  // 切换标签
  changeTab: function (e) {
    const index = e.currentTarget.dataset.index;
    const categoryId = this.data.categoryList[index].id;

    this.setData({
      currentTab: index
    });

    this.fetchContentList(categoryId);
  },

  // 查看详情
  viewDetail: function (e) {
    const contentId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/culture-detail/culture-detail?id=${contentId}`
    });
  }
}) 