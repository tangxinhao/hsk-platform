# 排查 HTTPS 无法访问问题

## 可能的原因

虽然容器已创建，证书文件也存在，但浏览器显示 `ERR_CONNECTION_REFUSED`，可能的原因：

1. Nginx 容器没有正常启动
2. 443 端口没有监听
3. Nginx 配置有错误（虽然测试通过，但实际启动可能失败）
4. 域名解析问题

## 排查步骤

### 步骤 1：检查容器状态

```bash
docker ps | grep nginx
```

应该看到容器状态是 `Up`。

### 步骤 2：检查 443 端口是否监听

```bash
netstat -tlnp | grep 443
```

或者：
```bash
ss -tlnp | grep 443
```

应该看到类似：
```
tcp  0  0  0.0.0.0:443  LISTEN  xxx/nginx
```

### 步骤 3：查看 Nginx 日志

```bash
docker logs hsk-nginx --tail 50
```

检查是否有错误信息。

### 步骤 4：检查 Nginx 是否在容器内运行

```bash
docker exec hsk-nginx ps aux | grep nginx
```

应该看到 nginx 进程在运行。

### 步骤 5：测试容器内的 HTTPS

```bash
docker exec hsk-nginx wget -O- https://localhost 2>&1 | head -20
```

或者：
```bash
docker exec hsk-nginx curl -k https://localhost
```

### 步骤 6：检查域名解析

```bash
nslookup www.tangxinhao.online
```

或者：
```bash
dig www.tangxinhao.online
```

确认域名解析到 `118.190.106.159`。

### 步骤 7：检查 Nginx 配置中的 server_name

```bash
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep server_name
```

确认配置中包含 `www.tangxinhao.online`。

## 常见问题

### 问题 1：容器启动但 Nginx 进程没有运行

**解决方案**：重启容器
```bash
docker restart hsk-nginx
docker logs hsk-nginx
```

### 问题 2：443 端口没有监听

**可能原因**：
- Nginx 配置错误
- 证书文件路径错误

**解决方案**：
```bash
# 检查 Nginx 配置
docker exec hsk-nginx nginx -t

# 检查证书文件
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/
```

### 问题 3：域名解析不正确

**解决方案**：确认域名 A 记录指向 `118.190.106.159`。
