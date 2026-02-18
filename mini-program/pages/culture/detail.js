// pages/culture/detail.js
const app = getApp()
const { t, getLang } = require('../../utils/i18n')

// 中国八大菜系详细数据（本地数据，无需数据库）
const cuisineData = {
  '鲁菜': {
    name: '鲁菜',
    title: '中国八大菜系 - 鲁菜',
    subtitle: '起源于山东，历史悠久，影响广泛',
    cover_image: '',  // 留空或使用本地图片
    category: '饮食文化',
    level: '中级',
    description: '鲁菜是中国传统四大菜系（也是八大菜系）中唯一的自发型菜系，是历史最悠久、技法最丰富的菜系，也是最难掌握的菜系。',
    origin: '山东省济南和胶东地区',
    characteristics: [
      '选料考究，刀法精细',
      '注重调味，口味鲜咸纯正',
      '烹调技法全面，尤以爆、炒、扒见长',
      '善于制汤，精于用汤'
    ],
    famous_dishes: [
      { name: '葱烧海参', desc: '选用上等海参，配以大葱爆炒，鲜香浓郁' },
      { name: '九转大肠', desc: '将猪大肠烧至外焦里嫩，酸甜咸辣香五味俱全' },
      { name: '糖醋鲤鱼', desc: '以黄河鲤鱼为主料，外焦里嫩，酸甜可口' },
      { name: '四喜丸子', desc: '象征人生四喜，肉质鲜嫩，营养丰富' }
    ],
    culture: '鲁菜讲究"食不厌精，脍不厌细"的孔子饮食思想，强调原汁原味和健康养生。',
    tips: '品尝鲁菜时，要注意其浓郁的北方风味，特别是葱姜蒜的运用非常讲究。'
  },
  '川菜': {
    name: '川菜',
    title: '中国八大菜系 - 川菜',
    subtitle: '麻辣鲜香，百菜百味',
    cover_image: '',
    category: '饮食文化',
    level: '中级',
    description: '川菜取材广泛，调味多变，菜式多样，口味清鲜醇浓并重，以善用麻辣调味著称，并以其别具一格的烹调方法和浓郁的地方风味闻名。',
    origin: '四川省成都和重庆地区',
    characteristics: [
      '取材广泛，调味多变',
      '麻辣鲜香，口味浓重',
      '善用豆瓣、花椒、辣椒',
      '烹调方法多样，技法精湛'
    ],
    famous_dishes: [
      { name: '麻婆豆腐', desc: '麻辣鲜香，豆腐嫩滑，是川菜代表作' },
      { name: '宫保鸡丁', desc: '鸡肉鲜嫩，花生酥脆，咸甜适中' },
      { name: '水煮鱼', desc: '鱼片嫩滑，麻辣鲜香，汤汁浓郁' },
      { name: '回锅肉', desc: '肉片薄而不碎，香辣可口，川菜之首' }
    ],
    culture: '川菜体现了四川人民热情奔放的性格，"麻"与"辣"是川菜的灵魂，也反映了四川盆地湿润气候下人们的饮食智慧。',
    tips: '初次品尝川菜建议从微辣开始，逐步适应。川菜的"麻"来自花椒，"辣"来自辣椒，二者缺一不可。'
  },
  '粤菜': {
    name: '粤菜',
    title: '中国八大菜系 - 粤菜',
    subtitle: '清淡鲜美，精致考究',
    cover_image: '',
    category: '饮食文化',
    level: '中级',
    description: '粤菜即广东菜，由广州菜（顺德菜）、潮州菜、东江菜（客家菜）三种地方风味组成。在世界各地粤菜与法国大餐齐名，是中国代表菜系之一。',
    origin: '广东省广州、潮州、东江地区',
    characteristics: [
      '选料精细，料多款式',
      '清而不淡，鲜而不俗',
      '嫩而不生，油而不腻',
      '注重火候，讲究鲜活'
    ],
    famous_dishes: [
      { name: '白切鸡', desc: '皮爽肉滑，清淡鲜美，原汁原味' },
      { name: '烧鹅', desc: '皮脆肉嫩，色泽金黄，香味浓郁' },
      { name: '虾饺', desc: '皮薄馅靓，晶莹剔透，鲜美爽滑' },
      { name: '清蒸鱼', desc: '鱼肉细嫩，保持原味，清鲜美味' }
    ],
    culture: '粤菜讲究"食在广州"，注重食材的新鲜和原味，体现了广东人务实、开放、兼容并包的文化特点。',
    tips: '品尝粤菜要注重食材的新鲜度，早茶文化是体验粤菜的重要方式，建议尝试各式点心。'
  },
  '苏菜': {
    name: '苏菜',
    title: '中国八大菜系 - 苏菜',
    subtitle: '清鲜平和，浓而不腻',
    cover_image: '',
    category: '饮食文化',
    level: '中级',
    description: '苏菜即江苏菜，由金陵菜、淮扬菜、苏锡菜、徐海菜等地方菜组成。苏菜讲究刀工，口味清鲜，擅长炖、焖、蒸、炒。',
    origin: '江苏省扬州、南京、苏州等地',
    characteristics: [
      '用料严谨，刀工精细',
      '注重本味，清鲜平和',
      '擅长炖焖，浓而不腻',
      '造型美观，雅俗共赏'
    ],
    famous_dishes: [
      { name: '松鼠桂鱼', desc: '形似松鼠，外脆里嫩，酸甜可口' },
      { name: '狮子头', desc: '肥而不腻，入口即化，汤汁鲜美' },
      { name: '大煮干丝', desc: '刀工精细，清鲜醇厚，淮扬名菜' },
      { name: '盐水鸭', desc: '南京特色，皮白肉嫩，滋味鲜美' }
    ],
    culture: '苏菜体现了江南水乡的精致文化和文人雅士的审美情趣，讲究"南甜北咸东辣西酸"中的南方清淡风格。',
    tips: '苏菜注重原汁原味，品尝时要细细体会其清鲜平和的口感，不要急于添加调料。'
  },
  '闽菜': {
    name: '闽菜',
    title: '中国八大菜系 - 闽菜',
    subtitle: '清鲜淡爽，重视汤鲜',
    cover_image: '',
    category: '饮食文化',
    level: '中级',
    description: '闽菜是以福州菜为代表，闽南菜、闽西菜为辅的福建菜系。闽菜擅长制汤，讲究调汤，以鲜香见长。',
    origin: '福建省福州、闽南、闽西地区',
    characteristics: [
      '选料精细，刀工严谨',
      '重视汤鲜，清鲜淡爽',
      '善用红糟，味道独特',
      '技法多样，尤擅糟醉'
    ],
    famous_dishes: [
      { name: '佛跳墙', desc: '荤香浓郁，汤鲜味美，闽菜之首' },
      { name: '荔枝肉', desc: '色如荔枝，酸甜适口，香气扑鼻' },
      { name: '醉糟鸡', desc: '色泽红润，香糟味浓，肉质细嫩' },
      { name: '沙茶面', desc: '闽南特色，汤鲜味美，配料丰富' }
    ],
    culture: '闽菜受到福建地理环境和海洋文化的影响，特别注重海鲜的烹制，体现了闽人精打细算、追求鲜美的饮食哲学。',
    tips: '品尝闽菜时要特别注意其独特的红糟调味，这是闽菜区别于其他菜系的重要特征。'
  },
  '浙菜': {
    name: '浙菜',
    title: '中国八大菜系 - 浙菜',
    subtitle: '鲜嫩软滑，清爽利口',
    cover_image: '',
    category: '饮食文化',
    level: '中级',
    description: '浙菜即浙江菜，以杭州菜为代表，还包括宁波菜、绍兴菜、温州菜等。浙菜注重原料的鲜嫩，讲究刀工，口味清鲜。',
    origin: '浙江省杭州、宁波、绍兴等地',
    characteristics: [
      '选料讲究，烹调独特',
      '注重原味，鲜嫩软滑',
      '清香醇厚，清爽利口',
      '讲究造型，精致秀美'
    ],
    famous_dishes: [
      { name: '西湖醋鱼', desc: '色泽红亮，酸甜可口，鱼肉鲜嫩' },
      { name: '东坡肉', desc: '色泽红艳，入口即化，肥而不腻' },
      { name: '龙井虾仁', desc: '虾仁鲜嫩，茶香四溢，清淡雅致' },
      { name: '宋嫂鱼羹', desc: '色泽黄亮，鲜嫩滑润，味美可口' }
    ],
    culture: '浙菜体现了江南水乡的精致和杭州西湖的诗情画意，讲究"轻油轻浆"，追求自然之美。',
    tips: '品尝浙菜要注意其清淡雅致的特点，特别是杭州菜，往往与当地的风景名胜和历史文化相关。'
  },
  '湘菜': {
    name: '湘菜',
    title: '中国八大菜系 - 湘菜',
    subtitle: '香辣酸咸，注重鲜香',
    cover_image: '',
    category: '饮食文化',
    level: '中级',
    description: '湘菜即湖南菜，是我国历史悠久的八大菜系之一。湘菜制作精细，用料广泛，口味多变，品种繁多。',
    origin: '湖南省长沙、湘潭、衡阳等地',
    characteristics: [
      '注重刀工，讲究火候',
      '香辣酸咸，油重色浓',
      '擅长腊熏，味道鲜香',
      '技法多样，尤重煨炖'
    ],
    famous_dishes: [
      { name: '剁椒鱼头', desc: '鱼肉细嫩，剁椒鲜辣，色泽红亮' },
      { name: '毛氏红烧肉', desc: '色泽红亮，肥而不腻，香甜软糯' },
      { name: '腊味合蒸', desc: '腊香浓郁，咸鲜微辣，风味独特' },
      { name: '永州血鸭', desc: '鸭肉鲜嫩，味道鲜辣，营养丰富' }
    ],
    culture: '湘菜体现了湖南人民的热情豪爽和敢为人先的精神，"辣"是湘菜的主基调，但不同于川菜的麻辣，湘菜更注重纯辣。',
    tips: '湘菜的辣较为直接，初次品尝者要做好准备。湘菜的腊味也很有特色，值得一试。'
  },
  '徽菜': {
    name: '徽菜',
    title: '中国八大菜系 - 徽菜',
    subtitle: '重油重色，擅长烧炖',
    cover_image: '',
    category: '饮食文化',
    level: '中级',
    description: '徽菜是安徽菜的简称，起源于徽州府，是徽州山区的地方风味。徽菜讲究火功，擅长烧、炖、蒸，重油重色重火功。',
    origin: '安徽省徽州地区（黄山市）',
    characteristics: [
      '就地取材，选料严谨',
      '善用火候，功夫独到',
      '重油重色，浓香扑鼻',
      '朴素实惠，保持原味'
    ],
    famous_dishes: [
      { name: '臭鳜鱼', desc: '闻起来臭，吃起来香，鱼肉鲜嫩' },
      { name: '红烧划水', desc: '龟肉鲜美，汤汁浓郁，营养丰富' },
      { name: '黄山炖鸽', desc: '鸽肉酥烂，汤汁鲜美，滋补养生' },
      { name: '毛豆腐', desc: '外焦里嫩，鲜美可口，徽州特色' }
    ],
    culture: '徽菜体现了徽商文化和徽州山区的地域特色，讲究原汁原味，注重食补食疗，体现了徽州人勤劳朴实的品格。',
    tips: '徽菜讲究烹调火候，其中炖、烧等技法需要长时间烹制，品尝时要注意其浓郁的香味和醇厚的口感。'
  }
}

Page({
  data: {
    contentId: null,
    content: null,
    loading: true,
    error: false,
    errorMsg: '',
    isFavorite: false,
    isLiked: false,
    // 如果是八大菜系的特殊展示
    isCuisine: false,
    cuisineDetail: null,
    activeSection: 0,
    sections: ['简介', '特点', '名菜', '文化', '小贴士'],
    // 国际化
    currentLang: 'zh',
    displayTitle: '',
    displaySubtitle: '',
    displayCategory: '',
    displayLevel: '',
    viewText: '浏览'
  },

  onLoad(options) {
    this.updateLanguage()
    
    if (options.id) {
      this.setData({ contentId: options.id })
      this.fetchContentDetail()
    } else {
      this.setData({
        loading: false,
        error: true,
        errorMsg: t('error.loadFailed')
      })
    }
  },
  
  updateLanguage() {
    const lang = getLang()
    const sections = lang === 'zh' 
      ? ['简介', '特点', '名菜', '文化', '小贴士']
      : ['Intro', 'Features', 'Dishes', 'Culture', 'Tips']
    
    this.setData({
      currentLang: lang,
      sections: sections,
      viewText: lang === 'zh' ? '浏览' : 'Views'
    })
    
    // 如果已经有内容，更新显示
    if (this.data.content) {
      this.updateDisplayFields()
    }
    
    wx.setNavigationBarTitle({
      title: lang === 'zh' ? '文化详情' : 'Cultural Content'
    })
  },
  
  updateDisplayFields() {
    const lang = this.data.currentLang
    const content = this.data.content
    const cuisineDetail = this.data.cuisineDetail
    
    this.setData({
      displayTitle: lang === 'zh' ? content.title : (content.title_en || content.title),
      displaySubtitle: lang === 'zh' 
        ? (content.subtitle || (cuisineDetail && cuisineDetail.subtitle) || '') 
        : (content.subtitle_en || (cuisineDetail && cuisineDetail.subtitle_en) || content.subtitle || ''),
      displayCategory: lang === 'zh' 
        ? (content.category_name || '文化') 
        : (content.category_name_en || 'Culture'),
      displayLevel: content.difficulty_display || (lang === 'zh' ? '中级' : 'Intermediate')
    })
    
    // 如果是菜系内容，重新格式化数据
    if (this.data.isCuisine && content.structured_data) {
      this.setData({
        cuisineDetail: this.formatCuisineData(content, lang)
      })
    }
  },
  
  onLanguageChange() {
    this.updateLanguage()
  },

  onPullDownRefresh() {
    if (this.data.contentId) {
      this.fetchContentDetail()
    }
    wx.stopPullDownRefresh()
  },

  // 加载菜系本地数据
  loadCuisineData(cuisineName) {
    // 优先从API获取菜系数据
    this.setData({ loading: true })
    
    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/content/`,
      method: 'GET',
      data: {
        search: cuisineName,
        page_size: 1
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data.results && res.data.results.length > 0) {
          const content = res.data.results[0]
          const lang = this.data.currentLang
          
          this.setData({
            loading: false,
            isCuisine: true,
            contentId: content.id,
            cuisineDetail: this.formatCuisineData(content, lang),
            content: content
          }, () => {
            this.updateDisplayFields()
            this.checkIfFavorite(content.id)
          })
        } else {
          this.setData({
            loading: false,
            error: true,
            errorMsg: t('error.loadFailed')
          })
        }
      },
      fail: (err) => {
        console.error('获取菜系数据失败:', err)
        this.setData({
          loading: false,
          error: true,
          errorMsg: t('error.network')
        })
      }
    })
  },

  // 从API获取内容详情
  fetchContentDetail() {
    const { contentId } = this.data
    
    this.setData({ loading: true, error: false })

    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/content/${contentId}/`,
      method: 'GET',
      success: (res) => {
        if (res.statusCode === 200) {
          const content = res.data
          
          // 检查是否有结构化数据（菜系数据）
          if (content.structured_data) {
            // 从数据库获取的结构化数据
            const lang = this.data.currentLang
            this.setData({
              isCuisine: true,
              cuisineDetail: this.formatCuisineData(content, lang),
              content: content
            }, () => {
              this.updateDisplayFields()
            })
          } else if (content.title && content.title.includes('八大菜系')) {
            // 不再降级到本地菜系数据，直接提示错误
            this.setData({
              loading: false,
              error: true,
              errorMsg: t('error.loadFailed')
            })
          } else {
            this.setData({
              content: content,
              isCuisine: false
            }, () => {
              this.updateDisplayFields()
            })
          }
          
          this.checkIfFavorite(contentId)
          this.checkIfLiked(contentId)
          this.incrementViewCount(contentId)
        } else {
          this.setData({
            error: true,
            errorMsg: '获取内容失败'
          })
        }
      },
      fail: (err) => {
        console.error('获取内容详情失败:', err)
        this.setData({
          error: true,
          errorMsg: '网络错误，请稍后重试'
        })
      },
      complete: () => {
        this.setData({ loading: false })
        wx.stopPullDownRefresh()
      }
    })
  },
  
  // 格式化数据库中的菜系数据为页面需要的格式
  formatCuisineData(content, lang = null) {
    if (!lang) {
      lang = this.data.currentLang || 'zh'
    }
    
    const structuredData = content.structured_data || {}
    
    return {
      name: lang === 'zh' ? content.title : (content.title_en || content.title),
      title: lang === 'zh' ? content.title : (content.title_en || content.title),
      subtitle: lang === 'zh' ? content.subtitle : (content.subtitle_en || content.subtitle || ''),
      subtitle_en: content.subtitle_en || '',
      cover_image: content.cover_image || '',
      category: content.category_name || (lang === 'zh' ? '饮食文化' : 'Cuisine'),
      level: content.difficulty_display || (lang === 'zh' ? '中级' : 'Intermediate'),
      description: lang === 'zh' 
        ? (content.description || content.content || '') 
        : (content.description_en || content.description || content.content || ''),
      origin: (structuredData.origin && structuredData.origin[lang]) || '',
      characteristics: (structuredData.characteristics && structuredData.characteristics[lang]) || [],
      famous_dishes: (structuredData.famous_dishes || []).map(dish => ({
        name: (dish.name && dish.name[lang]) || '',
        desc: (dish.desc && dish.desc[lang]) || ''
      })),
      culture: (structuredData.culture && structuredData.culture[lang]) || '',
      tips: (structuredData.tips && structuredData.tips[lang]) || ''
    }
  },

  // 切换菜系详情的不同部分
  switchSection(e) {
    const index = e.currentTarget.dataset.index
    this.setData({ activeSection: index })
  },

  // 检查是否已收藏
  checkIfFavorite(id) {
    const favorites = wx.getStorageSync('cultureFavorites') || []
    this.setData({
      isFavorite: favorites.includes(String(id))
    })
  },

  // 检查是否已点赞
  checkIfLiked(id) {
    const likes = wx.getStorageSync('cultureLikes') || []
    this.setData({
      isLiked: likes.includes(String(id))
    })
  },

  // 增加浏览次数
  incrementViewCount(id) {
    wx.request({
      url: `${app.globalData.apiBaseUrl}/culture/content/${id}/increment_view/`,  // 修复：使用正确的路径
      method: 'POST',
      success: (res) => {
        console.log('浏览次数已增加')
      },
      fail: (err) => {
        console.log('增加浏览次数失败:', err)
      }
    })
  },

  // 切换收藏状态
  toggleFavorite() {
    const id = this.data.isCuisine ? 
      'cuisine_' + this.data.cuisineDetail.name : 
      this.data.contentId
    
    let favorites = wx.getStorageSync('cultureFavorites') || []
    const idStr = String(id)
    
    if (this.data.isFavorite) {
      favorites = favorites.filter(item => item !== idStr)
      wx.showToast({
        title: '已取消收藏',
        icon: 'none'
      })
    } else {
      favorites.push(idStr)
      wx.showToast({
        title: '收藏成功',
        icon: 'success'
      })
    }
    
    wx.setStorageSync('cultureFavorites', favorites)
    this.setData({ isFavorite: !this.data.isFavorite })
  },

  // 切换点赞状态
  toggleLike() {
    if (this.data.isCuisine) {
      wx.showToast({
        title: '本地数据暂不支持点赞',
        icon: 'none'
      })
      return
    }

    const id = this.data.contentId
    let likes = wx.getStorageSync('cultureLikes') || []
    const idStr = String(id)
    
    if (this.data.isLiked) {
      likes = likes.filter(item => item !== idStr)
      wx.showToast({
        title: '已取消点赞',
        icon: 'none'
      })
    } else {
      likes.push(idStr)
      wx.showToast({
        title: '点赞成功',
        icon: 'success'
      })
    }
    
    wx.setStorageSync('cultureLikes', likes)
    this.setData({ isLiked: !this.data.isLiked })
  },

  // 预览图片
  previewImage(e) {
    const url = e.currentTarget.dataset.url
    if (url) {
      wx.previewImage({
        current: url,
        urls: [url]
      })
    }
  },

  // 分享
  onShareAppMessage() {
    const title = this.data.isCuisine ? 
      this.data.cuisineDetail.title : 
      this.data.content.title
    
    return {
      title: title,
      path: `/pages/culture/detail?id=${this.data.contentId || ''}`
    }
  }
})