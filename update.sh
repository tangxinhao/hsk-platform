#!/bin/bash
# HSK学习平台 - 代码更新脚本
# 用途：你在本地修改完代码后，通过 finshell/SFTP 覆盖到服务器目录，然后执行本脚本完成一键更新

set -e

echo "=========================================="
echo "  HSK学习平台 - 一键更新代码"
echo "=========================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ "$EUID" -ne 0 ]; then
  echo -e "${YELLOW}提示: 建议使用 root 或具备 docker 权限的用户运行本脚本${NC}"
fi

if [ ! -f .env ]; then
  echo -e "${RED}错误: 当前目录没有 .env，无法确定数据库和域名配置${NC}"
  exit 1
fi

echo -e "${GREEN}[1/4] 拉取最新镜像 / 重新构建本地镜像...${NC}"
docker compose -f docker-compose.prod.yml build

echo -e "${GREEN}[2/4] 以最小停机方式重启服务...${NC}"
docker compose -f docker-compose.prod.yml up -d

echo -e "${GREEN}[3/4] 执行数据库迁移（如有变更）...${NC}"
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate --settings=hsk_project.settings_prod || echo -e "${YELLOW}迁移失败，请检查日志${NC}"

echo -e "${GREEN}[4/4] 清理无用镜像，释放磁盘空间（可选）...${NC}"
docker image prune -f >/dev/null 2>&1 || true

echo ""
echo -e "${GREEN}更新完成！${NC}"
echo "如需查看运行情况：docker compose -f docker-compose.prod.yml ps"
echo "如需查看日志：docker compose -f docker-compose.prod.yml logs -f"

