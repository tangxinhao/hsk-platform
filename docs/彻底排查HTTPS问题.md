# 彻底排查 HTTPS 问题

## 完整排查步骤

### 步骤 1：检查 Nginx 错误日志（最重要）

```bash
docker exec hsk-nginx cat /var/log/nginx/error.log
```

或者：
```bash
docker logs hsk-nginx 2>&1 | grep -i error
```

**关键**：查看是否有证书文件找不到的错误。

### 步骤 2：确认证书文件在容器内存在且可读

```bash
# 检查文件是否存在
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/

# 检查文件内容（应该能看到证书内容）
docker exec hsk-nginx cat /etc/nginx/ssl/tangxinhao.online/cert.pem | head -5

# 检查文件权限
docker exec hsk-nginx ls -l /etc/nginx/ssl/tangxinhao.online/
```

### 步骤 3：测试容器内的 HTTPS

```bash
# 在容器内测试
docker exec hsk-nginx wget --no-check-certificate -O- https://localhost 2>&1 | head -20
```

### 步骤 4：检查 Nginx 是否真的在监听 443

```bash
# 在容器内检查
docker exec hsk-nginx netstat -tlnp | grep 443
```

或者：
```bash
docker exec hsk-nginx ss -tlnp | grep 443
```

### 步骤 5：检查 Nginx 进程和配置

```bash
# 检查 Nginx 进程
docker exec hsk-nginx ps aux | grep nginx

# 检查完整的 HTTPS server 块
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep -A 50 "listen 443"
```

## 可能的问题和解决方案

### 问题 1：证书文件不存在或路径错误

**检查**：
```bash
docker exec hsk-nginx test -f /etc/nginx/ssl/tangxinhao.online/cert.pem && echo "存在" || echo "不存在"
docker exec hsk-nginx test -f /etc/nginx/ssl/tangxinhao.online/cert.key && echo "存在" || echo "不存在"
```

**解决方案**：如果不存在，检查 volume 映射。

### 问题 2：Nginx 启动时证书加载失败

**检查错误日志**：
```bash
docker logs hsk-nginx 2>&1 | grep -i "certificate\|ssl\|error"
```

### 问题 3：Nginx 配置语法正确但实际无法启动 HTTPS

**解决方案**：尝试重新加载配置
```bash
docker exec hsk-nginx nginx -s reload
```

## 终极解决方案：简化测试

如果以上都不行，创建一个最简单的 HTTPS 配置测试：

```bash
# 创建一个测试配置文件
docker exec hsk-nginx sh -c 'cat > /tmp/test-ssl.conf << EOF
server {
    listen 443 ssl;
    server_name _;
    
    ssl_certificate /etc/nginx/ssl/tangxinhao.online/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/tangxinhao.online/cert.key;
    
    location / {
        return 200 "HTTPS Works!";
        add_header Content-Type text/plain;
    }
}
EOF'

# 测试这个配置
docker exec hsk-nginx nginx -t -c /tmp/test-ssl.conf
```
