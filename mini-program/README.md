# HSK学习助手小程序

这是一个帮助用户学习HSK（汉语水平考试）的微信小程序，同时提供中国高校信息和中国文化内容。

## 功能特点

- **HSK练习**：提供HSK各级别的题目练习，包括单选题、多选题、判断题等多种题型
- **高校信息**：展示中国高校的详细信息，包括基本信息、院系专业、招生政策和校园风光
- **中国文化**：分类展示中国文化内容，帮助用户了解中国传统文化
- **个人中心**：记录学习进度、收藏内容和个人设置

## 项目结构

```
mini-program/
├── pages/                  # 页面文件
│   ├── index/              # 首页
│   ├── university/         # 高校相关页面
│   ├── question/           # 题目相关页面
│   ├── culture/            # 文化相关页面
│   ├── hsk/                # HSK练习页面
│   ├── wrong-book/         # 错题本页面
│   ├── daily/              # 每日练习页面
│   ├── search/             # 搜索页面
│   └── user/               # 用户相关页面
├── assets/                 # 静态资源
│   ├── icons/              # 图标
│   └── images/             # 图片
├── utils/                  # 工具函数
├── app.js                  # 全局JS
├── app.json                # 全局配置
└── app.wxss                # 全局样式
```

## 开始使用

### 前提条件

- 安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
- 申请微信小程序AppID

### 安装步骤

1. 克隆项目到本地
2. 打开微信开发者工具
3. 导入项目，选择项目目录
4. 在项目配置中填入AppID

### 配置后端API

在 `app.js` 文件中，修改 `globalData.apiBaseUrl` 为你的后端API地址：

```js
globalData: {
  // ...
  apiBaseUrl: 'https://your-api-domain.com/api'
}
```

## 资源准备

### 图标资源

小程序需要以下图标资源：

1. 在 `/assets/icons/` 目录下准备所有需要的图标
2. 特别是底部导航栏图标：
   - tab-home.png 和 tab-home-active.png
   - tab-hsk.png 和 tab-hsk-active.png
   - tab-university.png 和 tab-university-active.png
   - tab-user.png 和 tab-user-active.png

### 图片资源

在 `/assets/images/` 目录下准备以下图片：

1. 轮播图：banner1.jpg, banner2.jpg, banner3.jpg
2. 默认图片：default-university.jpg, default-culture.jpg 等

## 注意事项

1. 小程序中的静态资源路径必须以 `/` 开头
2. 图标尺寸建议为 81px × 81px（底部导航）或 64px × 64px（功能图标）
3. 轮播图建议尺寸为 750px × 300px

## 开发建议

1. 使用微信开发者工具的调试功能检查网络请求和页面渲染
2. 在真机上测试小程序，确保在不同设备上的显示效果一致
3. 注意处理网络请求的错误情况和加载状态
4. 优化图片资源，减少加载时间 