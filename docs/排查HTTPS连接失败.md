# 排查 HTTPS 连接失败

## 问题确认

- ✅ HTTP (80端口) 工作正常
- ❌ HTTPS (443端口) 无法连接，即使直接用 IP 也不行
- ❌ 域名解析失败（次要问题）

## 可能的原因

1. Nginx HTTPS server 块没有正确启动
2. 证书文件路径或权限问题
3. Nginx 配置有错误但测试时没发现

## 排查步骤

### 步骤 1：检查 Nginx 错误日志

```bash
docker exec hsk-nginx cat /var/log/nginx/error.log
```

或者：
```bash
docker logs hsk-nginx 2>&1 | grep -i error
```

### 步骤 2：检查容器内的 Nginx 配置

```bash
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep -A 10 "listen 443"
```

确认 HTTPS server 块存在且没有被注释。

### 步骤 3：检查证书文件权限

```bash
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/
```

确认文件可读。

### 步骤 4：重启 Nginx 容器

```bash
docker restart hsk-nginx
docker logs hsk-nginx --tail 50
```

查看启动日志是否有错误。

### 步骤 5：测试容器内的 HTTPS

```bash
docker exec hsk-nginx wget --no-check-certificate -O- https://localhost 2>&1 | head -20
```

## 可能的问题和解决方案

### 问题 1：Nginx 配置中的 HTTPS server 块被注释

**检查**：
```bash
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep -A 5 "listen 443"
```

如果看不到输出，说明 HTTPS server 块可能被注释了。

### 问题 2：证书文件路径错误

**检查**：
```bash
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep ssl_certificate
```

确认路径是 `/etc/nginx/ssl/tangxinhao.online/cert.pem`。

### 问题 3：Nginx 没有正确加载配置

**解决方案**：重启容器并查看日志
```bash
docker restart hsk-nginx
docker logs hsk-nginx --tail 50
```
