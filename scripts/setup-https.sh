#!/bin/bash

# HTTPS 配置脚本
# 使用前确保：
# 1. 域名 tangxinhao.online 已备案
# 2. 域名已解析到服务器 IP (118.190.106.159)
# 3. 服务器 80 和 443 端口已开放

set -e

echo "=========================================="
echo "开始配置 HTTPS 证书"
echo "=========================================="

# 检查域名解析
echo "检查域名解析..."
if ! dig +short tangxinhao.online | grep -q "118.190.106.159"; then
    echo "❌ 错误：域名 tangxinhao.online 未解析到 118.190.106.159"
    echo "请先在 DNS 提供商处添加 A 记录"
    exit 1
fi
echo "✅ 域名解析正常"

# 获取证书
echo ""
echo "获取 Let's Encrypt 证书..."
read -p "请输入邮箱地址（用于证书到期提醒）: " EMAIL

docker run -it --rm \
  -v $(pwd)/certbot/www:/var/www/certbot \
  -v $(pwd)/certbot/conf:/etc/letsencrypt \
  certbot/certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email "$EMAIL" \
  --agree-tos \
  --no-eff-email \
  -d tangxinhao.online \
  -d www.tangxinhao.online

if [ $? -eq 0 ]; then
    echo "✅ 证书获取成功"
else
    echo "❌ 证书获取失败"
    exit 1
fi

# 检查证书文件
CERT_PATH="./certbot/conf/live/tangxinhao.online"
if [ ! -f "$CERT_PATH/fullchain.pem" ] || [ ! -f "$CERT_PATH/privkey.pem" ]; then
    echo "❌ 错误：证书文件不存在"
    exit 1
fi

echo ""
echo "=========================================="
echo "证书配置完成！"
echo "=========================================="
echo ""
echo "下一步操作："
echo "1. 编辑 nginx/conf.d/default.conf，取消注释 HTTPS 配置（第 90-171 行）"
echo "2. 注释掉临时 HTTP 配置中的 location / 部分（第 30-40 行）"
echo "3. 取消注释 HTTP 到 HTTPS 重定向（第 25-27 行）"
echo "4. 运行: docker restart hsk-nginx"
echo "5. 更新小程序代码中的 apiBaseUrl 为 https://tangxinhao.online/api"
echo "6. 在微信后台添加 https://tangxinhao.online 到 request合法域名"
echo ""
