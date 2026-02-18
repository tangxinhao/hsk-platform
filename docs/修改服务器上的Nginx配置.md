# 修改服务器上的 Nginx 配置

## 问题确认

主机上的配置文件仍然使用旧的 Let's Encrypt 证书路径，需要修改为阿里云证书路径。

## 修改步骤

### 方法一：使用 sed 命令直接修改（推荐）

在 FinalShell 终端执行：

```bash
cd /home/hsk

# 备份原配置
cp nginx/conf.d/default.conf nginx/conf.d/default.conf.bak

# 修改证书路径
sed -i 's|/etc/letsencrypt/live/tangxinhao.online/fullchain.pem|/etc/nginx/ssl/tangxinhao.online/cert.pem|g' nginx/conf.d/default.conf
sed -i 's|/etc/letsencrypt/live/tangxinhao.online/privkey.pem|/etc/nginx/ssl/tangxinhao.online/cert.key|g' nginx/conf.d/default.conf

# 验证修改
cat nginx/conf.d/default.conf | grep -A 5 "listen 443"
```

应该看到：
```
ssl_certificate /etc/nginx/ssl/tangxinhao.online/cert.pem;
ssl_certificate_key /etc/nginx/ssl/tangxinhao.online/cert.key;
```

### 方法二：使用 FinalShell 文件管理器编辑

1. 在 FinalShell 文件管理器中，找到 `/home/hsk/nginx/conf.d/default.conf`
2. 右键点击文件 → **编辑**
3. 找到 `ssl_certificate` 和 `ssl_certificate_key` 这两行
4. 修改为：
   ```
   ssl_certificate /etc/nginx/ssl/tangxinhao.online/cert.pem;
   ssl_certificate_key /etc/nginx/ssl/tangxinhao.online/cert.key;
   ```
5. 保存文件

## 重新创建容器

修改配置文件后，重新创建容器：

```bash
cd /home/hsk

# 停止并删除容器
docker stop hsk-nginx
docker rm hsk-nginx

# 重新创建容器
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
```

## 验证

```bash
# 1. 检查容器内的配置
docker exec hsk-nginx cat /etc/nginx/conf.d/default.conf | grep -A 5 "listen 443"

# 2. 测试配置
docker exec hsk-nginx nginx -t

# 3. 测试 HTTPS
curl -k https://118.190.106.159 -H "Host: www.tangxinhao.online"
```
