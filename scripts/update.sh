#!/bin/bash
# HSK学习平台 - 代码更新脚本
# 用于更新代码后重新部署

set -e

echo "=========================================="
echo "  HSK学习平台 更新脚本"
echo "=========================================="

cd /home/hsk

# 如果使用Git
if [ -d ".git" ]; then
    echo "正在拉取最新代码..."
    git pull
fi

echo "重新构建镜像..."
docker compose -f docker-compose.prod.yml build

echo "运行数据库迁移..."
docker compose -f docker-compose.prod.yml run --rm backend python manage.py migrate --settings=hsk_project.settings_prod

echo "重启服务..."
docker compose -f docker-compose.prod.yml up -d

echo ""
echo "更新完成！"
echo ""
