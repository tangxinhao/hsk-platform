# 手动创建 Nginx 容器（修复 SSL 映射）

## 问题确认

从 `docker inspect` 输出可以看到，容器中**没有** `/home/hsk/ssl` 到 `/etc/nginx/ssl` 的映射。

虽然 `docker-compose.prod.yml` 中配置了，但容器创建时没有生效。

## 解决方案：手动创建容器

在 FinalShell 终端执行：

```bash
cd /home/hsk

# 1. 停止并删除现有容器
docker stop hsk-nginx
docker rm hsk-nginx

# 2. 手动创建容器，明确指定所有 volume（包括 ssl）
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
  --network hsk-network \
  nginx:alpine
```

## 验证

创建后执行：

```bash
# 1. 检查映射（应该能看到 ssl）
docker inspect hsk-nginx | grep -A 50 "Mounts" | grep ssl

# 2. 检查证书文件
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/

# 应该看到：
# cert.pem
# cert.key

# 3. 测试 Nginx 配置
docker exec hsk-nginx nginx -t
```

## 如果网络不存在

如果提示 `network hsk-network not found`，先创建网络：

```bash
docker network create hsk-network
```

或者检查现有网络：

```bash
docker network ls | grep hsk
```
