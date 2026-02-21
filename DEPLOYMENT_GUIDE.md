# 部署指南 - 简化版

## 📋 配置文件说明

所有服务器配置都保存在 `server-config.json` 文件中，包括：
- 服务器信息（IP、域名、项目路径）
- 数据库配置（密码、库名等）
- Docker 服务名称
- 常见问题的修复方案

**重要：** 如果配置有变化，只需更新 `server-config.json`，AI 助手会先读取这个文件再操作。

## 🚀 快速部署

### 方法一：使用智能部署脚本（推荐）

```bash
cd /home/hsk

# 拉取最新代码
git pull origin main

# 给脚本添加执行权限（只需一次）
chmod +x smart-deploy.sh

# 部署全部服务
./smart-deploy.sh all

# 或仅部署前端用户端
./smart-deploy.sh frontend-user

# 或仅部署前端管理端
./smart-deploy.sh frontend-admin

# 或仅部署后端
./smart-deploy.sh backend
```

### 方法二：使用原有脚本

```bash
cd /home/hsk

# 更新全部
./deploy_all.sh

# 仅更新前端用户端
./deploy-frontend-user.sh

# 仅更新前端管理端
./deploy-frontend-admin.sh
```

## 🔧 智能部署脚本功能

`smart-deploy.sh` 会自动处理：

1. ✅ **检查并启用交换空间** - 避免服务器卡死
2. ✅ **处理 Git 冲突** - 自动保存或丢弃本地修改
3. ✅ **拉取最新代码** - 从 GitHub 获取更新
4. ✅ **检查并创建 .env 文件** - 自动从配置文件读取密码
5. ✅ **修复数据库权限** - 自动执行 MySQL 权限修复
6. ✅ **停止旧容器释放资源** - 避免资源不足
7. ✅ **重新创建容器** - 确保读取最新配置
8. ✅ **检查服务状态** - 显示部署结果

## 📝 配置文件结构

`server-config.json` 包含以下配置：

```json
{
  "server_info": {
    "host": "服务器IP",
    "project_path": "/home/hsk",
    "domain": "tangxinhao.online",
    "www_domain": "www.tangxinhao.online"
  },
  "database": {
    "password": "数据库密码",
    "name": "数据库名",
    "user": "数据库用户"
  },
  "common_issues": {
    "database_permission_fix": "MySQL权限修复SQL"
  }
}
```

## ⚠️ 常见问题处理

### 1. 服务器卡死
- 脚本会自动启用交换空间
- 会自动停止旧容器释放资源

### 2. Git 冲突
- 脚本会自动保存本地修改到 stash
- 如果失败，会自动重置

### 3. 数据库连接失败
- 脚本会自动修复 MySQL 权限
- 会自动创建/更新 .env 文件

### 4. 容器配置不更新
- 脚本会重新创建容器（不只是重启）
- 确保读取最新的 .env 配置

## 🔐 安全提示

⚠️ **重要：** `server-config.json` 包含敏感信息（数据库密码），请：
- 不要将此文件提交到公开的 Git 仓库
- 如果已提交，请立即修改密码
- 建议将 `server-config.json` 添加到 `.gitignore`

## 📞 使用 AI 助手时

当使用 AI 助手进行部署时，请告诉 AI：
1. "请先读取 `server-config.json` 配置文件"
2. "根据配置文件进行部署"
3. AI 会先读取配置，然后使用正确的参数执行操作

这样可以避免：
- ❌ 使用错误的密码
- ❌ 操作错误的容器名称
- ❌ 忘记启用交换空间
- ❌ 其他常见错误
