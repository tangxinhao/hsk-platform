# 检查完整的 Volume 映射

## 步骤 1：查看完整的 Mounts 信息

```bash
docker inspect hsk-nginx | grep -A 50 "Mounts"
```

或者更详细：

```bash
docker inspect hsk-nginx --format '{{json .Mounts}}' | python3 -m json.tool
```

查看是否有 `/home/hsk/ssl` 到 `/etc/nginx/ssl` 的映射。

## 步骤 2：检查 docker-compose 文件是否被正确读取

```bash
cd /home/hsk
cat docker-compose.prod.yml | grep -A 15 "nginx:"
```

确认配置文件中确实有：
```yaml
- ./ssl:/etc/nginx/ssl:ro
```

## 步骤 3：如果映射确实不存在，手动创建容器

如果 docker-compose 的映射不生效，可以手动创建容器：

```bash
cd /home/hsk

# 停止并删除现有容器
docker stop hsk-nginx
docker rm hsk-nginx

# 手动创建容器，明确指定所有 volume
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

## 步骤 4：验证

```bash
# 检查映射
docker inspect hsk-nginx | grep -A 50 "Mounts" | grep ssl

# 检查证书文件
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/
```
