# 配置阿里云 SSL 证书（备案前可配置）

## 当前状态

✅ **已有证书**：阿里云个人测试证书（www.tangxinhao.online，有效期至 2026-05-11）  
⏳ **备案状态**：管局审核中（预计 10 个工作日）  
✅ **可以配置**：备案未完成也可以先配置 HTTPS

## 配置步骤

### 步骤 1：下载 SSL 证书

1. 登录 [阿里云控制台](https://ecs.console.aliyun.com)
2. 进入：**产品与服务** → **数字证书管理服务** → **SSL证书管理**
3. 找到证书 `cert-wmwmfb`（www.tangxinhao.online）
4. 点击 **下载** 按钮
5. 选择 **Nginx** 格式下载
6. 解压后会得到两个文件：
   - `证书文件名.pem`（证书文件）
   - `证书文件名.key`（私钥文件）

### 步骤 2：上传证书到服务器

使用 FinalShell 或 scp 将证书文件上传到服务器：

```bash
# 在服务器上创建证书目录
mkdir -p /root/bs/ssl/tangxinhao.online

# 使用 FinalShell 上传两个文件到：
# /root/bs/ssl/tangxinhao.online/
```

或者使用 scp（在本地执行）：

```bash
scp 证书文件名.pem root@118.190.106.159:/root/bs/ssl/tangxinhao.online/cert.pem
scp 证书文件名.key root@118.190.106.159:/root/bs/ssl/tangxinhao.online/cert.key
```

### 步骤 3：修改 Nginx 配置

编辑 `nginx/conf.d/default.conf`：

1. **取消注释 HTTPS 配置**（第 90-171 行）
2. **修改证书路径**：
   ```nginx
   ssl_certificate /etc/nginx/ssl/tangxinhao.online/cert.pem;
   ssl_certificate_key /etc/nginx/ssl/tangxinhao.online/cert.key;
   ```
3. **启用 HTTP 到 HTTPS 重定向**（取消注释第 25-27 行）

### 步骤 4：更新 docker-compose.prod.yml

在 `nginx` 服务的 `volumes` 中添加证书目录映射：

```yaml
volumes:
  - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  - ./nginx/conf.d:/etc/nginx/conf.d:ro
  - ./ssl:/etc/nginx/ssl:ro  # 添加这一行
  - ./certbot/www:/var/www/certbot:ro
  - ./certbot/conf:/etc/letsencrypt:ro
  - ./backend/media:/var/www/media:ro
  - ./backend/static:/var/www/static:ro
```

### 步骤 5：重启 Nginx

```bash
docker restart hsk-nginx
```

### 步骤 6：测试 HTTPS

在浏览器访问：
- `https://www.tangxinhao.online`
- `https://www.tangxinhao.online/api/health/`（如果有健康检查接口）

### 步骤 7：更新小程序代码

修改 `mini-program/app.js`：

```javascript
apiBaseUrl: 'https://www.tangxinhao.online/api',
```

## 备案完成后的操作

备案完成后（管局审核通过）：

1. **在微信后台配置域名**：
   - 登录 [微信公众平台](https://mp.weixin.qq.com)
   - 进入：**开发** → **开发管理** → **开发设置**
   - 在 **request合法域名** 中添加：`https://www.tangxinhao.online`
   - 点击 **保存并提交**

2. **测试小程序**：
   - 在微信开发者工具中测试
   - 确认 API 请求正常

## 注意事项

1. **证书域名**：你的证书是 `www.tangxinhao.online`，所以：
   - ✅ 可以使用 `https://www.tangxinhao.online`
   - ❌ 不能使用 `https://tangxinhao.online`（除非证书包含根域名）

2. **备案期间**：
   - HTTPS 可以正常配置和使用
   - 但小程序后台无法添加域名（需要备案完成）
   - 可以先在开发工具测试

3. **证书续期**：
   - 证书有效期至 2026-05-11
   - 到期前需要在阿里云续期或重新申请
