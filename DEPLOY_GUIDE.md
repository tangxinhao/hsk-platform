# 🚀 HSK学习平台 - 阿里云部署完整指南

## 📋 目录

1. [前置准备](#前置准备)
2. [服务器配置](#服务器配置)
3. [域名解析](#域名解析)
4. [上传代码](#上传代码)
5. [部署应用](#部署应用)
6. [配置SSL证书](#配置ssl证书)
7. [日常维护](#日常维护)
8. [常见问题](#常见问题)

---

## 前置准备

### 你已有的资源
- ✅ 阿里云ECS服务器 (Ubuntu 24.04, 2核2G)
- ✅ 域名: tangxinhao.online

### 需要确认
- ⚠️ **公网IP**: 你的服务器目前显示公网IP为空，需要绑定**弹性公网IP (EIP)**

---

## 服务器配置

### 步骤1: 绑定弹性公网IP

1. 登录阿里云控制台
2. 进入 **云服务器ECS** → **实例**
3. 点击你的实例 `iZm5e0ziuo8u5v220ueg6nZ`
4. 在 **基本信息** 中找到 **公网IP**
5. 点击 **绑定弹性公网IP**
6. 如果没有EIP，先购买一个（按量付费很便宜）

### 步骤2: 配置安全组

1. 在实例详情页，点击 **安全组** 选项卡
2. 点击安全组ID进入配置
3. 添加以下入方向规则：

| 端口范围 | 授权对象 | 描述 |
|---------|---------|-----|
| 22/22 | 0.0.0.0/0 | SSH |
| 80/80 | 0.0.0.0/0 | HTTP |
| 443/443 | 0.0.0.0/0 | HTTPS |

### 步骤3: 远程连接服务器

**方式一：使用阿里云控制台**
- 点击 **远程连接** 按钮

**方式二：使用SSH（推荐）**
```bash
# Windows PowerShell 或 CMD
ssh root@你的公网IP

# 如果提示输入密码，使用你设置的密码
# 如果忘记密码，可以在控制台重置
```

### 步骤4: 安装Docker

连接到服务器后，执行以下命令：

```bash
# 更新系统
apt update && apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com | sh

# 启动Docker并设置开机自启
systemctl start docker
systemctl enable docker

# 安装Docker Compose
apt install docker-compose-plugin -y

# 验证安装
docker --version
docker compose version
```

---

## 域名解析

### 步骤1: 配置DNS解析

1. 登录阿里云控制台
2. 进入 **域名与网站** → **云解析DNS**
3. 找到域名 `tangxinhao.online`，点击 **解析设置**
4. 添加以下记录：

| 记录类型 | 主机记录 | 记录值 | TTL |
|---------|---------|-------|-----|
| A | @   | 你的公网IP（例如：118.190.106.159） | 10分钟 |
| A | www | 你的公网IP（例如：118.190.106.159） | 10分钟 |

### 步骤2: 验证解析

```bash
# 在本地或服务器上执行
ping tangxinhao.online

# 应该能看到你的公网IP
```

---

## 上传代码

### 方式一：使用Git（推荐）

```bash
# 在服务器上
cd /home
apt install git -y

# 如果代码在GitHub/Gitee
git clone 你的仓库地址 hsk

cd hsk
```

### 方式二：使用SFTP上传

**使用WinSCP (Windows):**
1. 下载安装 WinSCP
2. 新建会话：
   - 主机名: 你的公网IP
   - 用户名: root
   - 密码: 你的密码
3. 连接后，将本地 `D:\bs1\bs` 文件夹上传到 `/home/hsk`

**使用命令行:**
```powershell
# 在本地Windows PowerShell中执行
scp -r D:\bs1\bs root@你的公网IP:/home/hsk
```

---

## 部署应用

### 步骤1: 准备环境变量

```bash
# 进入项目目录
cd /home/hsk

# 复制环境变量模板
cp env.example .env

# 编辑环境变量
nano .env
```

**修改.env文件内容：**
```ini
# 数据库配置 - 请修改密码！
DB_NAME=hsk_schema
DB_USER=root
DB_PASSWORD=YourStrongPassword123!

# Django配置 - 请修改密钥！
SECRET_KEY=your-very-long-random-secret-key-change-this
ALLOWED_HOSTS=tangxinhao.online,www.tangxinhao.online,118.190.106.159,localhost

# API地址
API_BASE_URL=https://tangxinhao.online

# 域名配置
DOMAIN=tangxinhao.online
```

> 💡 **生成安全密钥**: `openssl rand -hex 32`

### 步骤2: 执行部署

```bash
# 添加执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### 步骤3: 创建管理员账号

```bash
# 创建Django超级用户
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser --settings=hsk_project.settings_prod
```

按提示输入用户名、邮箱和密码。

### 步骤4: 验证部署

打开浏览器访问：
- 用户前台: `http://tangxinhao.cn`
- 管理后台: `http://tangxinhao.cn/admin-panel/`
- Django管理: `http://tangxinhao.cn/django-admin/`

---

## 配置SSL证书

### 步骤1: 申请证书

```bash
# 添加执行权限
chmod +x ssl-init.sh

# 执行SSL初始化脚本
./ssl-init.sh
```

### 步骤2: 启用HTTPS

```bash
# 编辑Nginx配置
nano nginx/conf.d/default.conf
```

**修改内容：**
1. 找到HTTP配置中的临时location块，注释掉
2. 取消HTTP重定向的注释
3. 取消整个HTTPS server块的注释

```bash
# 重启Nginx
docker compose -f docker-compose.prod.yml restart nginx
```

### 步骤3: 验证HTTPS

访问 `https://tangxinhao.online`，应该能看到安全锁标志。

---

## 日常维护

### 查看日志

```bash
# 查看所有服务日志
docker compose -f docker-compose.prod.yml logs -f

# 查看特定服务日志
docker compose -f docker-compose.prod.yml logs -f backend
docker compose -f docker-compose.prod.yml logs -f nginx
```

### 更新代码

```bash
cd /home/hsk

# 如果使用Git
git pull

# 重新构建并部署
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d

# 如果有数据库变更
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate --settings=hsk_project.settings_prod
```

### 备份数据库

```bash
# 创建备份目录
mkdir -p /home/backups

# 备份数据库
docker compose -f docker-compose.prod.yml exec db mysqldump -u root -p$DB_PASSWORD hsk_learning > /home/backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### 恢复数据库

```bash
# 恢复数据库
docker compose -f docker-compose.prod.yml exec -T db mysql -u root -p$DB_PASSWORD hsk_learning < /home/backups/backup_file.sql
```

### 重启服务

```bash
# 重启所有服务
docker compose -f docker-compose.prod.yml restart

# 重启特定服务
docker compose -f docker-compose.prod.yml restart backend
```

### 停止服务

```bash
docker compose -f docker-compose.prod.yml down
```

---

## 常见问题

### Q1: 容器启动失败

```bash
# 查看容器状态
docker compose -f docker-compose.prod.yml ps

# 查看失败容器的日志
docker compose -f docker-compose.prod.yml logs backend
```

### Q2: 数据库连接失败

1. 检查数据库容器是否正常运行
2. 确认.env中的数据库密码与docker-compose.prod.yml中一致
3. 等待数据库完全启动（约30秒）

```bash
# 测试数据库连接
docker compose -f docker-compose.prod.yml exec db mysql -u root -p -e "SHOW DATABASES;"
```

### Q3: 网站无法访问

1. 检查安全组是否开放80/443端口
2. 检查域名解析是否生效
3. 检查Nginx是否正常运行

```bash
# 检查端口监听
netstat -tlnp | grep -E '80|443'

# 检查Nginx配置
docker compose -f docker-compose.prod.yml exec nginx nginx -t
```

### Q4: 静态文件/媒体文件无法访问

```bash
# 重新收集静态文件
docker compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput --settings=hsk_project.settings_prod

# 检查文件权限
ls -la backend/static/
ls -la backend/media/
```

### Q5: 内存不足

你的服务器只有2GB内存，如果出现内存不足：

```bash
# 检查内存使用
free -h

# 创建交换分区
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

---

## 项目结构说明

```
/home/hsk/
├── backend/                 # Django后端
│   ├── Dockerfile.prod     # 生产环境Dockerfile
│   ├── hsk_project/
│   │   ├── settings.py     # 开发环境配置
│   │   └── settings_prod.py # 生产环境配置
│   ├── media/              # 用户上传文件
│   └── static/             # 静态文件
├── frontend-user/          # 用户前台
├── frontend-admin/         # 管理后台
├── nginx/                  # Nginx配置
│   ├── nginx.conf
│   └── conf.d/
│       └── default.conf
├── certbot/                # SSL证书
├── docker-compose.prod.yml # 生产环境编排
├── .env                    # 环境变量
├── deploy.sh               # 部署脚本
└── ssl-init.sh            # SSL初始化脚本
```

---

## 联系方式

如有问题，请检查日志或参考阿里云文档。

祝部署顺利！🎉
