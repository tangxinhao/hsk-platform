# HSK学习平台

一个完整的HSK汉语水平考试学习系统，包含小程序、后端API和管理系统。

## 快速启动

### 1. 启动后端服务

**双击运行：**
```
【启动后端】.bat
```

或者手动启动：
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

看到 "Starting development server at http://0.0.0.0:8000/" 表示成功。

### 2. 配置小程序

1. 查看你的电脑IP地址：
   - 打开命令行，输入：`ipconfig`
   - 找到"IPv4 地址"，例如：192.168.3.5

2. 修改小程序配置：
   - 打开：`mini-program/app.js`
   - 第60行修改为你的IP：`apiBaseUrl: 'http://你的IP:8000/api'`

### 3. 打开小程序

1. 使用微信开发者工具
2. 导入项目：选择 `mini-program` 文件夹
3. 点击"编译"
4. 开始测试

## 项目结构

```
d:\bs\
├── backend/              # Django后端
├── mini-program/         # 微信小程序
├── frontend-admin/       # 管理后台（Vue）
├── frontend-user/        # 用户前端（Vue）
├── 【启动后端】.bat       # 后端启动脚本
└── 启动说明.txt          # 详细说明
```

## 主要功能

### 无需后端也能使用
- ✅ 中国八大菜系详情
- ✅ 院校智能推荐
- ✅ 收藏和点赞

### 需要后端支持
- 文化内容列表
- HSK题目练习
- 模拟考试
- 用户管理
- 学习进度

## 常见问题

**Q: 看到 ERR_CONNECTION_CLOSED 错误？**
A: 后端服务未启动，双击运行"【启动后端】.bat"

**Q: 小程序显示空白或报错？**
A: 检查 mini-program/app.js 中的 IP 地址配置

**Q: 后端启动失败？**
A: 确保已安装 Python 3.8 或更高版本

## 技术栈

- **小程序**: 微信原生 + Vant Weapp
- **后端**: Django + Django REST Framework
- **数据库**: SQLite（开发环境）
- **前端管理**: Vue 3 + Element Plus

## 更多帮助

详细说明请查看：`启动说明.txt`

管理后台地址：http://localhost:8000/admin
后端API文档：http://localhost:8000/api/
