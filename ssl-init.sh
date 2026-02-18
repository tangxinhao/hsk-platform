#!/bin/bash
# SSL证书初始化脚本
# 使用Let's Encrypt免费证书

set -e

# 加载环境变量
source .env

DOMAIN=${DOMAIN:-tangxinhao.cn}
EMAIL=${EMAIL:-admin@$DOMAIN}

echo "=========================================="
echo "  SSL证书初始化"
echo "=========================================="
echo "域名: $DOMAIN"
echo "邮箱: $EMAIL"
echo ""

# 检查域名解析
echo "检查域名解析..."
if ! host $DOMAIN > /dev/null 2>&1; then
    echo "警告: 无法解析域名 $DOMAIN"
    echo "请确保域名已正确解析到服务器IP"
fi

# 确保Nginx正在运行
docker compose -f docker-compose.prod.yml up -d nginx

# 申请证书
echo "申请SSL证书..."
docker compose -f docker-compose.prod.yml run --rm certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN \
    -d www.$DOMAIN

echo ""
echo "=========================================="
echo "  证书申请完成!"
echo "=========================================="
echo ""
echo "接下来请执行以下步骤:"
echo "1. 编辑 nginx/conf.d/default.conf"
echo "2. 取消HTTPS配置的注释"
echo "3. 注释掉HTTP配置中的location块，启用重定向"
echo "4. 重启Nginx: docker compose -f docker-compose.prod.yml restart nginx"
echo ""
