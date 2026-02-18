# HTTPS 配置快速指南

## ✅ 已完成的配置

1. ✅ Nginx 配置已启用 HTTPS
2. ✅ Docker Compose 已添加证书目录映射
3. ✅ 已创建证书目录结构说明

## 📋 你需要做的步骤

### 步骤 1：下载阿里云证书

1. 登录 [阿里云控制台](https://ecs.console.aliyun.com)
2. 进入：**产品与服务** → **数字证书管理服务** → **SSL证书管理**
3. 找到证书 `cert-wmwmfb`（www.tangxinhao.online）
4. 点击 **下载** → 选择 **Nginx** 格式
5. 解压后会得到两个文件（文件名可能类似 `xxx.pem` 和 `xxx.key`）

### 步骤 2：上传证书到服务器

**使用 FinalShell：**

1. 连接到服务器 `118.190.106.159`
2. 在服务器上创建目录：
   ```bash
   mkdir -p /root/bs/ssl/tangxinhao.online
   ```
3. 使用 FinalShell 的文件管理器，将下载的两个文件上传到：
   ```
   /root/bs/ssl/tangxinhao.online/
   ```
4. 重命名文件：
   ```bash
   cd /root/bs/ssl/tangxinhao.online
   mv 原证书文件名.pem cert.pem
   mv 原私钥文件名.key cert.key
   ```

### 步骤 3：重启 Nginx

```bash
docker restart hsk-nginx
```

### 步骤 4：测试 HTTPS

在浏览器访问：
- `https://www.tangxinhao.online`
- `https://www.tangxinhao.online/api/`

如果看到锁图标 ✅，说明 HTTPS 配置成功！

### 步骤 5：更新小程序代码（可选，等备案完成后再改）

编辑 `mini-program/app.js`，将：
```javascript
apiBaseUrl: 'http://118.190.106.159/api',
```
改为：
```javascript
apiBaseUrl: 'https://www.tangxinhao.online/api',
```

## ⚠️ 重要提示

1. **证书域名**：你的证书是 `www.tangxinhao.online`，所以：
   - ✅ 使用 `https://www.tangxinhao.online`
   - ❌ 不能使用 `https://tangxinhao.online`（除非证书包含根域名）

2. **备案期间**：
   - HTTPS 可以正常使用
   - 但小程序后台无法添加域名（需要备案完成）
   - 可以先在开发工具测试（勾选"不校验合法域名"）

3. **备案完成后**：
   - 在微信后台添加 `https://www.tangxinhao.online` 到 request合法域名
   - 更新小程序代码使用 HTTPS 地址
   - 正式发布小程序

## 🔍 验证配置

检查 Nginx 配置是否正确：
```bash
docker exec hsk-nginx nginx -t
```

查看 Nginx 日志：
```bash
docker logs hsk-nginx
```

## ❓ 遇到问题？

1. **证书文件找不到**：检查文件路径和文件名是否正确
2. **HTTPS 无法访问**：检查 443 端口是否开放
3. **证书错误**：确认证书文件完整且未损坏
