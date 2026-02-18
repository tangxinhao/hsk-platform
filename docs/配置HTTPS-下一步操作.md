# HTTPS 配置 - 下一步操作

## ✅ 已完成
- ✅ 证书文件已上传到 `/home/hsk/ssl/tangxinhao.online/`
- ✅ 文件已重命名为 `cert.pem` 和 `cert.key`

## 📋 接下来的步骤

### 步骤 1：重启 Nginx 容器

在 FinalShell 终端中执行：

```bash
cd /home/hsk
docker restart hsk-nginx
```

等待几秒钟，让容器重启完成。

### 步骤 2：检查 Nginx 配置是否正确

```bash
docker exec hsk-nginx nginx -t
```

如果看到 `test is successful`，说明配置正确。

### 步骤 3：查看 Nginx 日志（如果有错误）

```bash
docker logs hsk-nginx --tail 50
```

检查是否有错误信息。

### 步骤 4：测试 HTTPS

在浏览器中访问：
- `https://www.tangxinhao.online`
- `https://www.tangxinhao.online/api/`

**预期结果**：
- ✅ 看到锁图标（🔒），表示 HTTPS 配置成功
- ✅ 页面可以正常访问
- ✅ 没有证书错误提示

### 步骤 5：测试 API 接口

在浏览器访问：
```
https://www.tangxinhao.online/api/
```

应该能看到 API 响应（可能是 JSON 格式或错误页面，但应该是 HTTPS 连接）。

---

## ⚠️ 如果遇到问题

### 问题 1：Nginx 启动失败

**检查证书文件权限**：
```bash
ls -la /home/hsk/ssl/tangxinhao.online/
```

如果权限不对，执行：
```bash
chmod 644 /home/hsk/ssl/tangxinhao.online/cert.pem
chmod 600 /home/hsk/ssl/tangxinhao.online/cert.key
```

### 问题 2：HTTPS 无法访问

**检查 443 端口是否开放**：
```bash
netstat -tlnp | grep 443
```

或者检查防火墙：
```bash
# 如果使用 ufw
ufw status

# 如果使用 firewalld
firewall-cmd --list-ports
```

### 问题 3：证书错误

**检查证书文件是否完整**：
```bash
openssl x509 -in /home/hsk/ssl/tangxinhao.online/cert.pem -text -noout
```

应该能看到证书信息。

---

## 🎉 配置成功后

### 1. 更新小程序代码（可选，等备案完成后再改也可以）

编辑 `mini-program/app.js`，将：
```javascript
apiBaseUrl: 'http://118.190.106.159/api',
```

改为：
```javascript
apiBaseUrl: 'https://www.tangxinhao.online/api',
```

### 2. 备案完成后

在微信小程序后台添加域名：
- 登录 [微信公众平台](https://mp.weixin.qq.com)
- 进入：**开发** → **开发管理** → **开发设置**
- 在 **request合法域名** 中添加：`https://www.tangxinhao.online`
- 点击 **保存并提交**

---

## 📝 快速命令总结

```bash
# 1. 重启 Nginx
cd /home/hsk
docker restart hsk-nginx

# 2. 检查配置
docker exec hsk-nginx nginx -t

# 3. 查看日志
docker logs hsk-nginx --tail 50
```
