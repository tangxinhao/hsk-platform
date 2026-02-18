# 检查 Nginx 配置是否正确加载

## 问题

虽然容器、端口、进程都正常，但浏览器无法访问 HTTPS。可能是 Nginx 配置没有正确加载 HTTPS server 块。

## 检查步骤

### 步骤 1：检查容器内的 Nginx 配置

```bash
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep -A 5 "listen 443"
```

应该看到：
```
listen 443 ssl http2;
```

### 步骤 2：检查 server_name 配置

```bash
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep server_name
```

应该看到：
```
server_name tangxinhao.online www.tangxinhao.online;
```

### 步骤 3：检查证书路径配置

```bash
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep ssl_certificate
```

应该看到：
```
ssl_certificate /etc/nginx/ssl/tangxinhao.online/cert.pem;
ssl_certificate_key /etc/nginx/ssl/tangxinhao.online/cert.key;
```

### 步骤 4：测试容器内的 HTTPS

```bash
docker exec hsk-nginx wget --no-check-certificate -O- https://localhost 2>&1 | head -20
```

或者：
```bash
docker exec hsk-nginx curl -k https://localhost
```

### 步骤 5：检查域名解析

```bash
nslookup www.tangxinhao.online
```

确认解析到 `118.190.106.159`。

### 步骤 6：从服务器本地测试

```bash
curl -k https://www.tangxinhao.online
```

或者：
```bash
curl -k https://118.190.106.159 -H "Host: www.tangxinhao.online"
```

## 可能的问题

### 问题 1：访问的域名不对

- 证书是 `www.tangxinhao.online`
- 如果访问 `tangxinhao.online`（没有 www），可能会失败

**解决方案**：确保访问 `https://www.tangxinhao.online`

### 问题 2：域名解析不正确

**检查**：
```bash
nslookup www.tangxinhao.online
```

如果解析不到 `118.190.106.159`，需要检查 DNS 配置。

### 问题 3：Nginx HTTPS server 块没有生效

**检查**：查看完整的配置文件，确认 HTTPS server 块没有被注释。
