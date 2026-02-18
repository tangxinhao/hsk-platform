#!/bin/bash
# HSK学习平台 - 部署脚本
# 在服务器上执行此脚本进行部署

set -e

echo "=========================================="
echo "  HSK学习平台 Docker部署脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}建议使用root用户运行此脚本${NC}"
fi

# 检查.env文件
if [ ! -f .env ]; then
    echo -e "${RED}错误: .env文件不存在!${NC}"
    echo "请先复制env.example为.env并修改配置"
    echo "  cp env.example .env"
    echo "  nano .env"
    exit 1
fi

# 加载环境变量
source .env

echo -e "${GREEN}[1/6] 创建必要目录...${NC}"
mkdir -p certbot/www certbot/conf
mkdir -p backend/static backend/media
mkdir -p database

echo -e "${GREEN}[2/6] 停止旧容器...${NC}"
docker compose -f docker-compose.prod.yml down 2>/dev/null || true

echo -e "${GREEN}[3/6] 构建镜像...${NC}"
docker compose -f docker-compose.prod.yml build --no-cache

echo -e "${GREEN}[4/6] 启动数据库...${NC}"
docker compose -f docker-compose.prod.yml up -d db
echo "等待数据库启动(30秒)..."
sleep 30

echo -e "${GREEN}[5/6] 运行数据库迁移...${NC}"
docker compose -f docker-compose.prod.yml run --rm backend python manage.py migrate --settings=hsk_project.settings_prod

echo -e "${GREEN}[6/6] 启动所有服务...${NC}"
docker compose -f docker-compose.prod.yml up -d

echo ""
echo -e "${GREEN}=========================================="
echo "  部署完成!"
echo "=========================================="
echo -e "${NC}"
echo "访问地址:"
echo "  用户前台: http://${DOMAIN:-tangxinhao.cn}"
echo "  管理后台: http://${DOMAIN:-tangxinhao.cn}/admin-panel/"
echo "  Django管理: http://${DOMAIN:-tangxinhao.cn}/django-admin/"
echo ""
echo "查看日志: docker compose -f docker-compose.prod.yml logs -f"
echo "停止服务: docker compose -f docker-compose.prod.yml down"
echo ""
