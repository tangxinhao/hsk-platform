/**
 * 国际化工具
 * 支持中文和英文切换
 */

const translations = {
  'zh': {
    // 通用
    'app.name': 'HSK学习助手',
    'common.loading': '加载中...',
    'common.noData': '暂无数据',
    'common.loadMore': '加载更多',
    'common.noMore': '没有更多数据了',
    'common.confirm': '确定',
    'common.cancel': '取消',
    'common.back': '返回',
    'common.submit': '提交',
    'common.save': '保存',
    'common.delete': '删除',
    'common.edit': '编辑',
    'common.search': '搜索',
    'common.filter': '筛选',
    'common.all': '全部',
    
    // 导航栏
    'tab.home': '首页',
    'tab.practice': '练习',
    'tab.culture': '文化',
    'tab.exam': '考试',
    'tab.user': '我的',
    
    // 首页
    'home.welcome': '你好',
    'home.todayProgress': '今日学习',
    'home.completed': '已完成',
    'home.questions': '题',
    'home.studyDays': '学习天数',
    'home.totalQuestions': '累计题数',
    'home.accuracy': '正确率',
    'home.hskLevel': 'HSK等级',
    'home.continuePractice': '继续练习',
    'home.mockExam': '模拟考试',
    'home.wrongBook': '错题本',
    'home.studyProgress': '学习进度',
    'home.studyStats': '学习统计',
    
    // 练习页面
    'practice.title': 'HSK题目练习',
    'practice.subtitle': '选择你的HSK等级开始练习',
    'practice.level': '级',
    'practice.questions': '道题',
    'practice.progress': '进度',
    'practice.start': '开始练习',
    'practice.weekStats': '本周学习统计',
    'practice.practiceCount': '练习题数',
    'practice.correctRate': '正确率',
    'practice.studyTime': '学习时长',
    'practice.minutes': '分钟',
    'practice.hours': '小时',
    
    // 文化页面
    'culture.title': '中国文化',
    'culture.subtitle': '传承千年 · 博大精深',
    'culture.cuisinesTitle': '中国八大菜系',
    'culture.categoriesTitle': '文化分类',
    'culture.recommendedTitle': '精选推荐',
    'culture.viewAll': '查看全部',
    'culture.loading': '加载中...',
    'culture.noContent': '暂无内容',
    'culture.beginner': '初级',
    'culture.intermediate': '中级',
    'culture.advanced': '高级',
    'culture.listTitle': '文化内容',
    'culture.allCategories': '全部',
    // 八大菜系
    'culture.cuisines.lu.name': '鲁菜',
    'culture.cuisines.lu.desc': '北方菜系之首',
    'culture.cuisines.lu.region': '山东',
    'culture.cuisines.chuan.name': '川菜',
    'culture.cuisines.chuan.desc': '麻辣鲜香',
    'culture.cuisines.chuan.region': '四川',
    'culture.cuisines.yue.name': '粤菜',
    'culture.cuisines.yue.desc': '清淡鲜美',
    'culture.cuisines.yue.region': '广东',
    'culture.cuisines.su.name': '苏菜',
    'culture.cuisines.su.desc': '清鲜平和',
    'culture.cuisines.su.region': '江苏',
    'culture.cuisines.min.name': '闽菜',
    'culture.cuisines.min.desc': '重视汤鲜',
    'culture.cuisines.min.region': '福建',
    'culture.cuisines.zhe.name': '浙菜',
    'culture.cuisines.zhe.desc': '鲜嫩软滑',
    'culture.cuisines.zhe.region': '浙江',
    'culture.cuisines.xiang.name': '湘菜',
    'culture.cuisines.xiang.desc': '香辣酸咸',
    'culture.cuisines.xiang.region': '湖南',
    'culture.cuisines.hui.name': '徽菜',
    'culture.cuisines.hui.desc': '重油重色',
    'culture.cuisines.hui.region': '安徽',
    
    // 考试页面
    'exam.title': '模拟考试',
    'exam.subtitle': '选择HSK等级开始全真模拟考试',
    'exam.totalQuestions': '共{count}题',
    'exam.duration': '{time}分钟',
    'exam.totalScore': '满分{score}分',
    'exam.start': '开始考试',
    'exam.history': '最近考试记录',
    'exam.score': '分',
    'exam.confirm': '确定开始HSK {level}级模拟考试吗？考试期间请保持专注。',
    
    // 用户页面
    'user.notLogin': '未登录',
    'user.loginTip': '登录后可同步学习数据',
    'user.login': '登录',
    'user.logout': '退出',
    'user.studyDays': '学习天数',
    'user.completedQuestions': '已做题目',
    'user.correctRate': '正确率',
    'user.studyRecord': '学习记录',
    'user.progress': '学习进度',
    'user.wrongBook': '错题本',
    'user.favorites': '我的收藏',
    'user.examHistory': '考试历史',
    'user.settings': '设置',
    'user.language': '语言设置',
    'user.version': 'HSK学习助手 v1.0.0',
    
    // 难度等级
    'difficulty.easy': '简单',
    'difficulty.simple': '较易',
    'difficulty.medium': '中等',
    'difficulty.hard': '较难',
    'difficulty.difficult': '困难',
    
    // 错误提示
    'error.network': '网络错误，请稍后重试',
    'error.loadFailed': '加载失败',
    'error.submitFailed': '提交失败',
    'error.loginRequired': '请先登录',
  },
  
  'en': {
    // Common
    'app.name': 'HSK Study Assistant',
    'common.loading': 'Loading...',
    'common.noData': 'No data',
    'common.loadMore': 'Load More',
    'common.noMore': 'No more data',
    'common.confirm': 'Confirm',
    'common.cancel': 'Cancel',
    'common.back': 'Back',
    'common.submit': 'Submit',
    'common.save': 'Save',
    'common.delete': 'Delete',
    'common.edit': 'Edit',
    'common.search': 'Search',
    'common.filter': 'Filter',
    'common.all': 'All',
    
    // Navigation
    'tab.home': 'Home',
    'tab.practice': 'Practice',
    'tab.culture': 'Culture',
    'tab.exam': 'Exam',
    'tab.user': 'Me',
    
    // Home
    'home.welcome': 'Hello',
    'home.todayProgress': "Today's Study",
    'home.completed': 'Completed',
    'home.questions': ' questions',
    'home.studyDays': 'Study Days',
    'home.totalQuestions': 'Total Questions',
    'home.accuracy': 'Accuracy',
    'home.hskLevel': 'HSK Level',
    'home.continuePractice': 'Continue Practice',
    'home.mockExam': 'Mock Exam',
    'home.wrongBook': 'Wrong Book',
    'home.studyProgress': 'Study Progress',
    'home.studyStats': 'Study Statistics',
    
    // Practice
    'practice.title': 'HSK Practice',
    'practice.subtitle': 'Select your HSK level to start practicing',
    'practice.level': '',
    'practice.questions': ' questions',
    'practice.progress': 'Progress',
    'practice.start': 'Start Practice',
    'practice.weekStats': 'This Week Statistics',
    'practice.practiceCount': 'Questions',
    'practice.correctRate': 'Accuracy',
    'practice.studyTime': 'Study Time',
    'practice.minutes': 'min',
    'practice.hours': 'hrs',
    
    // Culture
    'culture.title': 'Chinese Culture',
    'culture.subtitle': 'Thousands of Years of Heritage',
    'culture.cuisinesTitle': 'Eight Major Cuisines',
    'culture.categoriesTitle': 'Categories',
    'culture.recommendedTitle': 'Featured',
    'culture.viewAll': 'View All',
    'culture.loading': 'Loading...',
    'culture.noContent': 'No content',
    'culture.beginner': 'Beginner',
    'culture.intermediate': 'Intermediate',
    'culture.advanced': 'Advanced',
    'culture.listTitle': 'Cultural Content',
    'culture.allCategories': 'All',
    // Eight cuisines
    'culture.cuisines.lu.name': 'Lu Cuisine',
    'culture.cuisines.lu.desc': 'Shandong Style',
    'culture.cuisines.lu.region': 'Shandong',
    'culture.cuisines.chuan.name': 'Sichuan Cuisine',
    'culture.cuisines.chuan.desc': 'Spicy & Numbing',
    'culture.cuisines.chuan.region': 'Sichuan',
    'culture.cuisines.yue.name': 'Cantonese',
    'culture.cuisines.yue.desc': 'Light & Fresh',
    'culture.cuisines.yue.region': 'Guangdong',
    'culture.cuisines.su.name': 'Jiangsu Cuisine',
    'culture.cuisines.su.desc': 'Mild & Elegant',
    'culture.cuisines.su.region': 'Jiangsu',
    'culture.cuisines.min.name': 'Fujian Cuisine',
    'culture.cuisines.min.desc': 'Soup-based',
    'culture.cuisines.min.region': 'Fujian',
    'culture.cuisines.zhe.name': 'Zhejiang Cuisine',
    'culture.cuisines.zhe.desc': 'Tender & Smooth',
    'culture.cuisines.zhe.region': 'Zhejiang',
    'culture.cuisines.xiang.name': 'Hunan Cuisine',
    'culture.cuisines.xiang.desc': 'Hot & Sour',
    'culture.cuisines.xiang.region': 'Hunan',
    'culture.cuisines.hui.name': 'Anhui Cuisine',
    'culture.cuisines.hui.desc': 'Rich & Bold',
    'culture.cuisines.hui.region': 'Anhui',
    
    // Exam
    'exam.title': 'Mock Exam',
    'exam.subtitle': 'Select HSK level to start mock exam',
    'exam.totalQuestions': '{count} questions',
    'exam.duration': '{time} minutes',
    'exam.totalScore': '{score} points',
    'exam.start': 'Start Exam',
    'exam.history': 'Recent Exam History',
    'exam.score': ' pts',
    'exam.confirm': 'Start HSK {level} mock exam? Please stay focused during the exam.',
    
    // User
    'user.notLogin': 'Not logged in',
    'user.loginTip': 'Login to sync your study data',
    'user.login': 'Login',
    'user.logout': 'Logout',
    'user.studyDays': 'Study Days',
    'user.completedQuestions': 'Completed',
    'user.correctRate': 'Accuracy',
    'user.studyRecord': 'Study Record',
    'user.progress': 'Progress',
    'user.wrongBook': 'Wrong Book',
    'user.favorites': 'Favorites',
    'user.examHistory': 'Exam History',
    'user.settings': 'Settings',
    'user.language': 'Language',
    'user.version': 'HSK Study Assistant v1.0.0',
    
    // Difficulty
    'difficulty.easy': 'Easy',
    'difficulty.simple': 'Simple',
    'difficulty.medium': 'Medium',
    'difficulty.hard': 'Hard',
    'difficulty.difficult': 'Difficult',
    
    // Errors
    'error.network': 'Network error, please try again',
    'error.loadFailed': 'Load failed',
    'error.submitFailed': 'Submit failed',
    'error.loginRequired': 'Please login first',
  }
}

class I18n {
  constructor() {
    this.currentLang = wx.getStorageSync('language') || 'zh'
  }
  
  // 获取当前语言
  getLang() {
    return this.currentLang
  }
  
  // 设置语言
  setLang(lang) {
    if (lang !== 'zh' && lang !== 'en') {
      lang = 'zh'
    }
    this.currentLang = lang
    wx.setStorageSync('language', lang)
  }
  
  // 翻译文本
  t(key, params = {}) {
    const langData = translations[this.currentLang] || translations['zh']
    let text = langData[key] || key
    
    // 替换参数
    Object.keys(params).forEach(paramKey => {
      text = text.replace(`{${paramKey}}`, params[paramKey])
    })
    
    return text
  }
  
  // 获取数据的多语言字段
  getField(data, field) {
    if (!data) return ''
    
    if (this.currentLang === 'en') {
      // 英文：优先使用英文字段，回退到中文
      return data[`${field}_en`] || data[field] || ''
    } else {
      // 中文：直接使用中文字段
      return data[field] || ''
    }
  }
  
  // 格式化难度显示
  getDifficulty(level) {
    const map = {
      1: 'difficulty.easy',
      2: 'difficulty.simple',
      3: 'difficulty.medium',
      4: 'difficulty.hard',
      5: 'difficulty.difficult'
    }
    return this.t(map[level] || 'difficulty.medium')
  }
}

// 创建单例
const i18n = new I18n()

module.exports = {
  i18n,
  t: (key, params) => i18n.t(key, params),
  getField: (data, field) => i18n.getField(data, field),
  getLang: () => i18n.getLang(),
  setLang: (lang) => i18n.setLang(lang)
}
