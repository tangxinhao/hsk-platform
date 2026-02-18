# 修复 Volume 映射问题

## 问题确认

- ✅ 证书文件在主机上存在：`/home/hsk/ssl/tangxinhao.online/cert.pem` 和 `cert.key`
- ✅ `docker-compose.prod.yml` 中配置了 `./ssl:/etc/nginx/ssl:ro`
- ❌ 但容器创建时 volume 映射没有生效

## 解决方案

### 方法一：重新创建整个服务栈（推荐）

```bash
cd /home/hsk

# 停止所有服务
docker compose -f docker-compose.prod.yml down

# 重新创建所有服务（会重新读取配置）
docker compose -f docker-compose.prod.yml up -d
```

### 方法二：只重新创建 Nginx 服务

```bash
cd /home/hsk

# 停止并删除 Nginx 容器
docker compose -f docker-compose.prod.yml stop nginx
docker compose -f docker-compose.prod.yml rm -f nginx

# 重新创建
docker compose -f docker-compose.prod.yml up -d nginx
```

### 方法三：使用 docker run 测试（临时方案）

如果上面方法不行，可以手动创建容器测试：

```bash
cd /home/hsk

# 停止并删除现有容器
docker stop hsk-nginx
docker rm hsk-nginx

# 手动创建容器，明确指定 volume 映射
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

## 验证修复

重新创建后，执行：

```bash
# 1. 检查 volume 映射
docker inspect hsk-nginx | grep -A 30 "Mounts"

# 应该看到：
# "/home/hsk/ssl" -> "/etc/nginx/ssl"

# 2. 检查容器内的证书文件
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/

# 应该看到：
# cert.pem
# cert.key
```
