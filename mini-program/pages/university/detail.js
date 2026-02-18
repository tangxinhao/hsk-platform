// 高校详情页面
const app = getApp()

Page({
  data: {
    universityId: null,
    university: {},
    departments: [],
    admission: null,
    sceneryImages: [],
    loading: true,
    error: false,
    errorMsg: '',
    currentTab: 'info',
    isFavorite: false
  },

  onLoad: function (options) {
    if (options.id) {
      // 确保 universityId 统一为字符串类型
      const universityId = String(options.id)
      this.setData({
        universityId: universityId
      })
      this.fetchUniversityDetail()
      this.checkIfFavorite()
    } else {
      this.setData({
        loading: false,
        error: true,
        errorMsg: '未找到高校ID'
      })
    }
  },

  onPullDownRefresh: function () {
    this.fetchUniversityDetail()
  },

  fetchUniversityDetail: function () {
    const { universityId } = this.data

    this.setData({
      loading: true,
      error: false
    })

    // 使用封装的request工具
    app.globalData.request({
      url: `/university/${universityId}/`,
      method: 'GET'
    })
      .then((res) => {
        this.setData({
          university: res
        })

        // 获取院系专业信息
        this.fetchDepartments()

        // 获取招生政策信息
        this.fetchAdmissionInfo()

        // 获取校园风光图片
        this.fetchSceneryImages()
      })
      .catch((err) => {
        console.error('获取高校详情失败:', err)
        this.setData({
          error: true,
          errorMsg: err.data?.detail || '获取高校信息失败，请稍后重试'
        })
      })
      .finally(() => {
        this.setData({ loading: false })
        wx.stopPullDownRefresh()
      })
  },

  fetchDepartments: function () {
    const { university } = this.data

    // 从后端返回的 university.majors / university.popular_majors 构建院系与专业列表
    // majors 建议在数据库中以 JSON 形式存储，例如：
    // [{"name": "计算机科学与技术学院", "majors": ["计算机科学与技术", "软件工程"]}, ...]

    const departments = []

    if (Array.isArray(university.majors) && university.majors.length > 0) {
      university.majors.forEach((dept, index) => {
        if (typeof dept === 'string') {
          departments.push({
            id: index + 1,
            name: dept,
            majors: []
          })
        } else if (dept && typeof dept === 'object') {
          departments.push({
            id: index + 1,
            name: dept.name || `学院${index + 1}`,
            majors: Array.isArray(dept.majors)
              ? dept.majors.map((m, i) => ({
                  id: `${index + 1}-${i + 1}`,
                  name: typeof m === 'string' ? m : (m.name || `专业${i + 1}`)
                }))
              : []
          })
        }
      })
    }

    // 如果 popular_majors 里还有额外专业，也附加到第一个学院
    if (Array.isArray(university.popular_majors) && university.popular_majors.length > 0) {
      const firstDept = departments[0] || { id: 1, name: '热门专业', majors: [] }
      if (!departments[0]) {
        departments.push(firstDept)
      }
      university.popular_majors.forEach((m, i) => {
        firstDept.majors.push({
          id: `hot-${i + 1}`,
          name: typeof m === 'string' ? m : (m.name || `热门专业${i + 1}`)
        })
      })
    }

      this.setData({
      departments
      })
  },

  fetchAdmissionInfo: function () {
    const { university } = this.data

    // 使用 University 模型中的字段来构建招生信息
    const plan = university.scholarship || '请参考学校官网发布的最新招生计划'
    const requirements = university.language_requirements || `建议HSK等级不低于 ${university.min_hsk_level || 1} 级`
    const policy = university.features || '具体录取政策以学校和各省市招生考试机构公布的信息为准'

    const links = []
    if (university.website) {
      links.push({ title: '学校官网', url: university.website })
    }

    const admission = {
      plan,
      requirements,
      policy,
      links
    }

      this.setData({
      admission
      })
  },

  fetchSceneryImages: function () {
    const { university } = this.data

    const images = []

    // 优先使用 campus_image_url
    if (university.campus_image_url) {
      images.push({
        url: university.campus_image_url,
        caption: `${university.name || ''} 校园风光`
      })
    }

    // 其次可以使用 logo_url 作为一张补充图片
    if (university.logo_url) {
      images.push({
        url: university.logo_url,
        caption: `${university.name || ''} 校徽`
      })
    }

      this.setData({
      sceneryImages: images
      })
  },

  switchTab: function (e) {
    const tab = e.currentTarget.dataset.tab
    this.setData({
      currentTab: tab
    })
  },

  openWebsite: function (e) {
    const url = e.currentTarget.dataset.url
    if (url) {
      wx.showModal({
        title: '打开外部链接',
        content: '即将前往外部网站，是否继续？',
        success: (res) => {
          if (res.confirm) {
            wx.setClipboardData({
              data: url,
              success: () => {
                wx.showToast({
                  title: '链接已复制，请在浏览器中打开',
                  icon: 'none'
                })
              }
            })
          }
        }
      })
    }
  },

  makePhoneCall: function (e) {
    const phone = e.currentTarget.dataset.phone
    if (phone) {
      wx.makePhoneCall({
        phoneNumber: phone
      })
    }
  },

  previewImage: function (e) {
    const index = parseInt(e.currentTarget.dataset.index)
    const { sceneryImages } = this.data

    if (!sceneryImages || sceneryImages.length === 0) {
      wx.showToast({
        title: '暂无图片',
        icon: 'none'
      })
      return
    }

    const urls = sceneryImages
      .map(item => item && item.url ? item.url : null)
      .filter(url => url !== null)

    if (urls.length === 0) {
      wx.showToast({
        title: '图片加载失败',
        icon: 'none'
      })
      return
    }

    // 确保 index 在有效范围内
    const validIndex = Math.max(0, Math.min(index || 0, urls.length - 1))

    wx.previewImage({
      current: urls[validIndex],
      urls: urls
    })
  },

  checkIfFavorite: function () {
    const { universityId } = this.data
    if (!universityId) return

    const favorites = wx.getStorageSync('favoriteUniversities') || []
    // 统一转换为字符串进行比较，避免类型不一致问题
    const favoriteIds = favorites.map(id => String(id))

    this.setData({
      isFavorite: favoriteIds.includes(String(universityId))
    })
  },

  toggleFavorite: function () {
    const { universityId, isFavorite } = this.data
    if (!universityId) return

    let favorites = wx.getStorageSync('favoriteUniversities') || []
    // 统一转换为字符串，确保类型一致
    const universityIdStr = String(universityId)
    const favoriteIds = favorites.map(id => String(id))

    if (isFavorite) {
      // 取消收藏
      favorites = favoriteIds.filter(id => id !== universityIdStr)
      wx.showToast({
        title: '已取消收藏',
        icon: 'none'
      })
    } else {
      // 添加收藏（避免重复添加）
      if (!favoriteIds.includes(universityIdStr)) {
        favorites.push(universityIdStr)
      }
      wx.showToast({
        title: '收藏成功',
        icon: 'success'
      })
    }

    wx.setStorageSync('favoriteUniversities', favorites)

    this.setData({
      isFavorite: !isFavorite
    })
  },

  onShareAppMessage: function () {
    const { university, universityId } = this.data
    const universityName = university && university.name ? university.name : '高校'
    return {
      title: `${universityName} - 高校详情`,
      path: `/pages/university/detail?id=${universityId || ''}`
    }
  }
}) 