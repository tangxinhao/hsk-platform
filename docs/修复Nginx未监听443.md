# 修复 Nginx 未监听 443 端口

## 问题确认

- ✅ 证书文件存在
- ✅ Nginx 进程在运行
- ✅ 主机 443 端口开放
- ❌ 容器内 Nginx 没有监听 443

## 解决方案

### 步骤 1：检查 Nginx 是否真的在监听 443

```bash
# 在容器内检查
docker exec hsk-nginx sh -c "cat /proc/net/tcp | grep :01BB"
```

`01BB` 是 443 的十六进制。如果有输出，说明在监听。

### 步骤 2：检查 Nginx 启动日志

```bash
docker logs hsk-nginx 2>&1 | grep -i "ssl\|certificate\|443\|error"
```

### 步骤 3：重新加载 Nginx 配置

```bash
# 测试配置
docker exec hsk-nginx nginx -t

# 重新加载配置
docker exec hsk-nginx nginx -s reload

# 检查是否监听 443
docker exec hsk-nginx sh -c "cat /proc/net/tcp | grep :01BB"
```

### 步骤 4：如果重新加载不行，重启容器

```bash
docker restart hsk-nginx
docker logs hsk-nginx --tail 30
```

### 步骤 5：检查证书文件权限

```bash
# 检查权限
docker exec hsk-nginx ls -l /etc/nginx/ssl/tangxinhao.online/

# 如果权限不对，需要修改主机上的文件权限
chmod 644 /home/hsk/ssl/tangxinhao.online/cert.pem
chmod 600 /home/hsk/ssl/tangxinhao.online/cert.key
```

## 终极解决方案：强制重新加载配置

如果以上都不行，尝试：

```bash
# 停止容器
docker stop hsk-nginx

# 删除容器
docker rm hsk-nginx

# 重新创建（确保配置正确）
docker run -d \
  --name hsk-nginx \
  --restart always \
  -p 80:80 \
  -p 443:443 \
  -v /home/hsk/nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v /home/hsk/nginx/conf.d:/etc/nginx/conf.d:ro \
  -v /home/hsk/ssl:/etc/nginx/ssl:ro \
  -v /home/hsk/certbot/www:/var/www/certbot:ro \
  -v /home/hsk/certbot/conf:/etc/letsencrypt:ro \
  -v /home/hsk/backend/media:/var/www/media:ro \
  -v /home/hsk/backend/static:/var/www/static:ro \
  --network hsk_hsk-network \
  nginx:alpine

# 立即检查日志
docker logs hsk-nginx --tail 50

# 检查是否监听 443
docker exec hsk-nginx sh -c "cat /proc/net/tcp | grep :01BB"
```
