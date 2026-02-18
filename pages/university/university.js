Page({
  data: {
    searchText: '',
    loading: true,
    universities: [],
    filteredUniversities: [],
    currentTab: 0, // 0: 全部, 1: 985, 2: 211, 3: 双一流
    tabs: ['全部', '985工程', '211工程', '双一流'],
    regions: [],
    selectedRegion: '全部地区',
    showRegionPicker: false
  },

  onLoad: function () {
    this.fetchUniversities()
    this.initRegions()
  },

  fetchUniversities: function () {
    // 模拟API请求
    setTimeout(() => {
      // 模拟数据
      const universities = [
        {
          id: '1',
          name: '北京大学',
          englishName: 'Peking University',
          region: '北京',
          badge: '/images/universities/pku_badge.png',
          is985: true,
          is211: true,
          isDoubleFirstClass: true,
          ranking: 1,
          summary: '北京大学创办于1898年，初名京师大学堂，是中国近代第一所国立综合性大学，也是当时中国最高教育行政机关。'
        },
        {
          id: '2',
          name: '清华大学',
          englishName: 'Tsinghua University',
          region: '北京',
          badge: '/images/universities/tsinghua_badge.png',
          is985: true,
          is211: true,
          isDoubleFirstClass: true,
          ranking: 2,
          summary: '清华大学(Tsinghua University)是中国著名高等学府，坐落于北京西北郊，是中国高层次人才培养和科学技术研究的重要基地。'
        },
        {
          id: '3',
          name: '复旦大学',
          englishName: 'Fudan University',
          region: '上海',
          badge: '/images/universities/fudan_badge.png',
          is985: true,
          is211: true,
          isDoubleFirstClass: true,
          ranking: 3,
          summary: '复旦大学创建于1905年，是中国人自主创办的第一所高等院校，是中国最著名的高等学府之一。'
        },
        {
          id: '4',
          name: '浙江大学',
          englishName: 'Zhejiang University',
          region: '浙江',
          badge: '/images/universities/zju_badge.png',
          is985: true,
          is211: true,
          isDoubleFirstClass: true,
          ranking: 4,
          summary: '浙江大学坐落于"人间天堂"杭州，前身是1897年创建的求是书院，是中国人自己最早创办的新式高等学校之一。'
        },
        {
          id: '5',
          name: '华中科技大学',
          englishName: 'Huazhong University of Science and Technology',
          region: '湖北',
          badge: '/images/universities/hust_badge.png',
          is985: true,
          is211: true,
          isDoubleFirstClass: true,
          ranking: 8,
          summary: '华中科技大学是国家教育部直属的全国重点大学，由原华中理工大学、同济医科大学、武汉城市建设学院合并组建而成。'
        },
        {
          id: '6',
          name: '深圳大学',
          englishName: 'Shenzhen University',
          region: '广东',
          badge: '/images/universities/szu_badge.png',
          is985: false,
          is211: false,
          isDoubleFirstClass: false,
          ranking: 42,
          summary: '深圳大学位于中国广东省深圳市，是一所综合性大学，创办于1983年，是深圳市人民政府举办的综合性大学。'
        }
      ]

      this.setData({
        universities,
        filteredUniversities: universities,
        loading: false
      })
    }, 1000)
  },

  initRegions: function () {
    // 这里可以调用API获取地区列表
    // 模拟数据
    const regions = ['全部地区', '北京', '上海', '浙江', '江苏', '湖北', '广东', '四川', '陕西']
    this.setData({ regions })
  },

  searchUniversity: function (e) {
    const searchText = e.detail.value
    this.setData({ searchText })
    this.filterUniversities()
  },

  selectTab: function (e) {
    const currentTab = e.currentTarget.dataset.index
    this.setData({ currentTab })
    this.filterUniversities()
  },

  toggleRegionPicker: function () {
    this.setData({
      showRegionPicker: !this.data.showRegionPicker
    })
  },

  selectRegion: function (e) {
    const selectedRegion = e.currentTarget.dataset.region
    this.setData({
      selectedRegion,
      showRegionPicker: false
    })
    this.filterUniversities()
  },

  filterUniversities: function () {
    let filteredUniversities = [...this.data.universities]

    // 按关键词筛选
    if (this.data.searchText) {
      const searchText = this.data.searchText.toLowerCase()
      filteredUniversities = filteredUniversities.filter(uni =>
        uni.name.toLowerCase().includes(searchText) ||
        uni.englishName.toLowerCase().includes(searchText)
      )
    }

    // 按类型筛选
    if (this.data.currentTab === 1) {
      filteredUniversities = filteredUniversities.filter(uni => uni.is985)
    } else if (this.data.currentTab === 2) {
      filteredUniversities = filteredUniversities.filter(uni => uni.is211)
    } else if (this.data.currentTab === 3) {
      filteredUniversities = filteredUniversities.filter(uni => uni.isDoubleFirstClass)
    }

    // 按地区筛选
    if (this.data.selectedRegion !== '全部地区') {
      filteredUniversities = filteredUniversities.filter(uni =>
        uni.region === this.data.selectedRegion
      )
    }

    this.setData({ filteredUniversities })
  },

  viewUniversityDetail: function (e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({
      url: `/pages/university/detail?id=${id}`
    })
  },

  onShareAppMessage: function () {
    return {
      title: '中国大学信息查询',
      path: '/pages/university/university'
    }
  }
}) 