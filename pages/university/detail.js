Page({
  data: {
    universityId: null,
    university: null,
    loading: true,
    currentTab: 0,
    tabs: ['基本信息', '院系专业', '招生政策', '校园风光'],
    departments: [],
    admissionPolicies: [],
    campusScenery: []
  },

  onLoad: function (options) {
    if (options.id) {
      this.setData({
        universityId: options.id,
        loading: true
      })
      this.fetchUniversityDetail(options.id)
    }
  },

  fetchUniversityDetail: function (id) {
    // 模拟API请求
    setTimeout(() => {
      // 模拟数据
      const university = {
        id: id,
        name: id === '1' ? '北京大学' : (id === '2' ? '清华大学' : '复旦大学'),
        englishName: id === '1' ? 'Peking University' : (id === '2' ? 'Tsinghua University' : 'Fudan University'),
        badge: `/images/universities/${id === '1' ? 'pku' : (id === '2' ? 'tsinghua' : 'fudan')}_badge.png`,
        banner: `/images/universities/${id === '1' ? 'pku' : (id === '2' ? 'tsinghua' : 'fudan')}_banner.jpg`,
        established: id === '1' ? '1898年' : (id === '2' ? '1911年' : '1905年'),
        region: id === '1' ? '北京' : (id === '2' ? '北京' : '上海'),
        address: id === '1' ? '北京市海淀区颐和园路5号' : (id === '2' ? '北京市海淀区清华园1号' : '上海市杨浦区邯郸路220号'),
        is985: true,
        is211: true,
        isDoubleFirstClass: true,
        ranking: id === '1' ? '1' : (id === '2' ? '2' : '3'),
        website: id === '1' ? 'https://www.pku.edu.cn' : (id === '2' ? 'https://www.tsinghua.edu.cn' : 'https://www.fudan.edu.cn'),
        description: id === '1' ?
          '北京大学创办于1898年，初名京师大学堂，是中国近代第一所国立综合性大学，是当时中国最高教育行政机关。辛亥革命后，于1912年改为现名。作为新文化运动的中心和"五四"运动的策源地，作为中国最早传播马克思主义和民主科学思想的发祥地，作为中国共产党最早的活动基地，北京大学为民族的振兴和解放、国家的建设和发展、社会的文明和进步做出了不可替代的贡献，在中国走向现代化的进程中起到了重要的先锋作用。爱国、进步、民主、科学的传统精神和勤奋、严谨、求实、创新的学风在这里生生不息、代代相传。' :
          (id === '2' ?
            '清华大学(Tsinghua University)是中国著名高等学府，坐落于北京西北郊，是中国高层次人才培养和科学技术研究的重要基地。清华大学的前身是清华学堂，成立于1911年，最初是清政府建立的留美预备学校，其建校的资金源于美国退还的部分庚子赔款。1912年更名为清华学校。1928年更名为国立清华大学。1937年抗日战争爆发后南迁长沙，与北京大学、南开大学组建国立长沙临时大学，1938年迁至昆明，改名为国立西南联合大学。1946年迁回清华园，设有文、法、理、工、农等5个学院、26个系。' :
            '复旦大学创建于1905年，原名复旦公学，是中国人自主创办的第一所高等院校，创始人为中国近代知名教育家马相伯。1917年改名为私立复旦大学。抗战时期，学校内迁重庆，并于1942年改为"国立"。1952年全国高等学校院系调整后，复旦大学成为以文理科为基础的综合性大学。复旦大学以"博学而笃志，切问而近思"为校训，以"学术独立，思想自由"为学风，以"团结、服务、牺牲"为校风，是中国人创办的第一所高等学校。')
      }

      this.setData({
        university,
        loading: false
      })

      // 根据当前tab获取相应数据
      this.switchTab({ currentTarget: { dataset: { index: 0 } } })
    }, 1000)
  },

  fetchDepartments: function () {
    // 模拟API请求
    setTimeout(() => {
      // 模拟院系数据
      const departments = [
        {
          id: '1',
          name: '文学院',
          majors: ['中国语言文学', '汉语言', '古典文献学', '比较文学与世界文学']
        },
        {
          id: '2',
          name: '理学院',
          majors: ['数学与应用数学', '物理学', '化学', '生物科学', '天文学']
        },
        {
          id: '3',
          name: '工学院',
          majors: ['计算机科学与技术', '电子工程', '材料科学与工程', '环境科学与工程']
        },
        {
          id: '4',
          name: '医学院',
          majors: ['临床医学', '基础医学', '口腔医学', '公共卫生学', '药学']
        },
        {
          id: '5',
          name: '法学院',
          majors: ['法学', '国际法', '经济法', '知识产权法']
        }
      ]

      this.setData({ departments })
    }, 500)
  },

  fetchAdmissionPolicies: function () {
    // 模拟API请求
    setTimeout(() => {
      // 模拟招生政策数据
      const admissionPolicies = [
        {
          year: '2023',
          title: '本科招生简章',
          description: '2023年计划招收本科生3500名，其中提前批次800名，统招批次2700名。',
          link: 'https://admission.university.edu.cn/2023'
        },
        {
          year: '2023',
          title: '研究生招生简章',
          description: '2023年计划招收硕士研究生2200名，博士研究生900名。',
          link: 'https://graduate.university.edu.cn/2023'
        },
        {
          year: '2023',
          title: '国际学生招生简章',
          description: '2023年计划招收国际本科生400名，研究生300名。',
          link: 'https://international.university.edu.cn/2023'
        },
        {
          year: '2022',
          title: '本科招生简章(往年)',
          description: '2022年共招收本科生3200名，其中提前批次750名，统招批次2450名。',
          link: 'https://admission.university.edu.cn/2022'
        }
      ]

      this.setData({ admissionPolicies })
    }, 500)
  },

  fetchCampusScenery: function () {
    // 模拟API请求
    setTimeout(() => {
      // 模拟校园风光数据
      const campusScenery = [
        {
          id: '1',
          title: '校门',
          image: '/images/universities/campus_gate.jpg',
          description: '学校正门，建于1952年，是学校的标志性建筑之一。'
        },
        {
          id: '2',
          title: '图书馆',
          image: '/images/universities/campus_library.jpg',
          description: '图书馆藏书超过500万册，是国内藏书最丰富的大学图书馆之一。'
        },
        {
          id: '3',
          title: '教学楼',
          image: '/images/universities/campus_building.jpg',
          description: '主教学楼群，包含多个学院的教室和实验室。'
        },
        {
          id: '4',
          title: '体育场',
          image: '/images/universities/campus_stadium.jpg',
          description: '学校体育场，可容纳5000名观众，是举办各类体育赛事的场所。'
        },
        {
          id: '5',
          title: '校园景观',
          image: '/images/universities/campus_view.jpg',
          description: '校园内湖光山色，四季如画，是学习和休憩的理想场所。'
        },
        {
          id: '6',
          title: '食堂',
          image: '/images/universities/campus_canteen.jpg',
          description: '学生食堂，提供多种风味美食，满足不同地区学生的饮食习惯。'
        }
      ]

      this.setData({ campusScenery })
    }, 500)
  },

  switchTab: function (e) {
    const index = e.currentTarget.dataset.index
    this.setData({ currentTab: index })

    // 根据切换的标签加载对应数据
    if (index === 1 && this.data.departments.length === 0) {
      this.fetchDepartments()
    } else if (index === 2 && this.data.admissionPolicies.length === 0) {
      this.fetchAdmissionPolicies()
    } else if (index === 3 && this.data.campusScenery.length === 0) {
      this.fetchCampusScenery()
    }
  },

  previewImage: function (e) {
    const urls = this.data.campusScenery.map(item => item.image)
    const current = e.currentTarget.dataset.url

    wx.previewImage({
      current: current,
      urls: urls
    })
  },

  openWebsite: function () {
    // 在实际应用中，可能需要使用web-view组件或者复制链接
    wx.showModal({
      title: '访问网站',
      content: `是否前往${this.data.university.website}?`,
      success: function (res) {
        if (res.confirm) {
          // 小程序内无法直接打开外部链接，可以复制链接到剪贴板
          wx.setClipboardData({
            data: this.data.university.website,
            success: function () {
              wx.showToast({
                title: '网址已复制',
                icon: 'success'
              })
            }
          })
        }
      }.bind(this)
    })
  },

  viewLocationMap: function () {
    // 在实际应用中，可以调用地图API
    wx.showToast({
      title: '地图功能开发中',
      icon: 'none'
    })
  },

  onShareAppMessage: function () {
    return {
      title: this.data.university ? `${this.data.university.name}大学详情` : '大学详情',
      path: `/pages/university/detail?id=${this.data.universityId}`
    }
  }
}) 