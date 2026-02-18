const { getLang } = require('../../utils/i18n')
const app = getApp()

Component({
  data: {
    currentLang: 'zh'
  },
  
  lifetimes: {
    attached() {
      this.setData({
        currentLang: getLang()
      })
    }
  },
  
  methods: {
    showLanguageMenu() {
      const itemList = ['中文 (Chinese)', 'English']
      const currentIndex = this.data.currentLang === 'zh' ? 0 : 1
      
      wx.showActionSheet({
        itemList: itemList,
        success: (res) => {
          const newLang = res.tapIndex === 0 ? 'zh' : 'en'
          if (newLang !== this.data.currentLang) {
            this.switchLanguage(newLang)
          }
        }
      })
    },
    
    switchLanguage(newLang) {
      app.switchLanguage(newLang)
      this.setData({
        currentLang: newLang
      })
    }
  }
})
