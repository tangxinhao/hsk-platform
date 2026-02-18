# 检查 Nginx 证书加载错误

## 问题确认

容器内 Nginx 没有监听 443 端口，即使重新加载配置后仍然如此。

## 可能的原因

Nginx 启动时因为证书问题没有启动 HTTPS server，但错误可能没有记录在日志中。

## 排查步骤

### 步骤 1：检查 Nginx 错误日志（详细）

```bash
# 查看完整的错误日志
docker exec hsk-nginx cat /var/log/nginx/error.log

# 或者查看最近的日志
docker logs hsk-nginx 2>&1 | tail -50
```

### 步骤 2：手动测试证书文件

```bash
# 检查证书文件是否真的可读
docker exec hsk-nginx cat /etc/nginx/ssl/tangxinhao.online/cert.pem > /dev/null && echo "证书可读" || echo "证书不可读"

# 检查私钥文件
docker exec hsk-nginx cat /etc/nginx/ssl/tangxinhao.online/cert.key > /dev/null && echo "私钥可读" || echo "私钥不可读"
```

### 步骤 3：检查 Nginx 配置中的证书路径

```bash
# 确认配置中的路径
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep ssl_certificate
```

### 步骤 4：尝试手动启动 Nginx 并查看输出

```bash
# 停止容器
docker stop hsk-nginx

# 以前台模式启动，查看详细输出
docker run --rm -it \
  -p 443:443 \
  -v /home/hsk/nginx/conf.d:/etc/nginx/conf.d:ro \
  -v /home/hsk/ssl:/etc/nginx/ssl:ro \
  nginx:alpine nginx -g "daemon off;"
```

这样可以看到 Nginx 启动时的所有输出，包括任何错误。

### 步骤 5：检查证书文件格式

```bash
# 检查证书格式
docker exec hsk-nginx openssl x509 -in /etc/nginx/ssl/tangxinhao.online/cert.pem -text -noout 2>&1 | head -5

# 检查私钥格式
docker exec hsk-nginx openssl rsa -in /etc/nginx/ssl/tangxinhao.online/cert.key -check -noout 2>&1
```

## 终极解决方案：简化配置测试

如果以上都不行，创建一个最简单的 HTTPS 配置：

```bash
# 创建一个最小配置
cat > /tmp/minimal-ssl.conf << 'EOF'
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
EOF

# 使用这个配置测试
docker run --rm -d \
  --name hsk-nginx-test \
  -p 8443:443 \
  -v /home/hsk/ssl:/etc/nginx/ssl:ro \
  -v /tmp/minimal-ssl.conf:/etc/nginx/conf.d/default.conf:ro \
  nginx:alpine

# 测试
curl -k https://118.190.106.159:8443
```
