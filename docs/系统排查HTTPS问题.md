# 系统排查 HTTPS 问题

## 完整排查清单

### 1. 检查证书文件（最重要）

```bash
# 检查文件是否存在
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/

# 检查文件内容（应该能看到证书内容）
docker exec hsk-nginx head -5 /etc/nginx/ssl/tangxinhao.online/cert.pem

# 检查文件权限
docker exec hsk-nginx ls -l /etc/nginx/ssl/tangxinhao.online/
```

### 2. 检查容器内 Nginx 是否监听 443

```bash
# 方法一
docker exec hsk-nginx netstat -tlnp 2>/dev/null | grep 443

# 方法二（如果 netstat 不可用）
docker exec hsk-nginx ss -tlnp 2>/dev/null | grep 443

# 方法三（检查进程）
docker exec hsk-nginx ps aux | grep nginx
```

### 3. 检查完整的 Nginx 配置

```bash
# 查看完整的 HTTPS server 块
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep -A 100 "listen 443" | head -50
```

### 4. 测试容器内的 HTTPS

```bash
# 方法一：使用 wget
docker exec hsk-nginx wget --no-check-certificate -O- https://localhost 2>&1

# 方法二：使用 curl（如果可用）
docker exec hsk-nginx curl -k https://localhost 2>&1
```

### 5. 检查 Nginx 配置语法（再次确认）

```bash
docker exec hsk-nginx nginx -t
```

### 6. 检查容器状态和端口映射

```bash
# 检查容器状态
docker ps | grep nginx

# 检查端口映射
docker port hsk-nginx
```

### 7. 从主机测试容器端口

```bash
# 测试容器内的 443 端口
telnet localhost 443
# 或者
nc -zv localhost 443
```

## 可能的问题

### 问题 1：证书文件不存在或路径错误

如果 `ls -la` 显示文件不存在，说明 volume 映射有问题。

### 问题 2：Nginx 没有监听 443

如果 `netstat` 或 `ss` 没有显示 443 端口，说明 Nginx 的 HTTPS server 块没有生效。

### 问题 3：配置被注释或语法错误

检查配置文件中 HTTPS server 块是否被正确启用。
