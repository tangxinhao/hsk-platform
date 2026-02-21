#!/bin/bash

# 智能部署脚本 - 自动读取配置并处理常见问题
# 使用方法: cd /home/hsk && ./smart-deploy.sh [frontend-user|frontend-admin|backend|all]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置文件路径
CONFIG_FILE="server-config.json"
ENV_FILE=".env"

# 读取配置
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}错误: 配置文件 $CONFIG_FILE 不存在！${NC}"
    echo "请先创建配置文件或从 GitHub 拉取最新代码"
    exit 1
fi

# 解析 JSON 配置（使用 Python，因为大多数服务器都有）
read_config() {
    python3 -c "
import json
import sys
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
    print(config['$1']['$2'])
" 2>/dev/null || echo ""
}

# 获取配置值
PROJECT_PATH=$(read_config "server_info" "project_path" || echo "/home/hsk")
DB_PASSWORD=$(read_config "database" "password" || echo "tangxinhao521")
DB_NAME=$(read_config "database" "name" || echo "hsk_schema")
COMPOSE_FILE=$(read_config "docker" "compose_file" || echo "docker-compose.prod.yml")
SWAP_FILE=$(read_config "deployment" "swap_file" || echo "/swapfile")

echo -e "${BLUE}=========================================="
echo "智能部署脚本"
echo "==========================================${NC}"

# 1. 检查并启用交换空间
echo ""
echo -e "${GREEN}[1/8] 检查交换空间...${NC}"
if ! swapon --show | grep -q swapfile; then
    if [ -f "$SWAP_FILE" ]; then
        echo "启用现有交换文件..."
        swapon "$SWAP_FILE" 2>/dev/null || {
            mkswap "$SWAP_FILE"
            swapon "$SWAP_FILE"
        }
    else
        echo "创建交换空间..."
        SWAP_SIZE=$(read_config "deployment" "swap_size" || echo "2G")
        fallocate -l "$SWAP_SIZE" "$SWAP_FILE" 2>/dev/null || dd if=/dev/zero of="$SWAP_FILE" bs=1M count=2048
        chmod 600 "$SWAP_FILE"
        mkswap "$SWAP_FILE"
        swapon "$SWAP_FILE"
    fi
fi
echo "交换空间状态:"
free -h | grep Swap

# 2. 进入项目目录
cd "$PROJECT_PATH" || exit 1

# 3. 处理 Git 冲突并拉取代码
echo ""
echo -e "${GREEN}[2/8] 处理 Git 并拉取代码...${NC}"
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
    echo "发现本地修改，保存到 stash..."
    git stash push -m "Auto stash before deploy $(date +%Y%m%d_%H%M%S)" 2>/dev/null || {
        echo "警告: git stash 失败，尝试重置..."
        git reset --hard HEAD
    }
fi

GIT_REPO=$(read_config "deployment" "git_repo" || echo "")
GIT_BRANCH=$(read_config "deployment" "git_branch" || echo "main")

if [ -n "$GIT_REPO" ]; then
    git pull "$GIT_REPO" "$GIT_BRANCH" 2>/dev/null || {
        echo "警告: git pull 失败，继续使用本地代码"
    }
else
    git pull origin main 2>/dev/null || {
        echo "警告: git pull 失败，继续使用本地代码"
    }
fi

# 4. 检查并创建 .env 文件
echo ""
echo -e "${GREEN}[3/8] 检查 .env 文件...${NC}"
if [ ! -f "$ENV_FILE" ]; then
    echo "创建 .env 文件..."
    cat > "$ENV_FILE" <<ENVEOF
DB_PASSWORD=$DB_PASSWORD
DB_NAME=$DB_NAME
DB_USER=$(read_config "database" "user" || echo "root")
SECRET_KEY=$(read_config "common_issues" "secret_key" || echo "your_django_secret_key_here")
ALLOWED_HOSTS=$(read_config "server_info" "domain" || echo "tangxinhao.online"),$(read_config "server_info" "www_domain" || echo "www.tangxinhao.online"),localhost,$(read_config "server_info" "host" || echo "118.190.106.159")
API_BASE_URL=https://$(read_config "server_info" "www_domain" || echo "www.tangxinhao.online")
ENVEOF
    echo ".env 文件已创建"
else
    echo ".env 文件已存在"
    # 更新密码（如果配置中有）
    if grep -q "DB_PASSWORD=" "$ENV_FILE"; then
        sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=$DB_PASSWORD/" "$ENV_FILE"
    else
        echo "DB_PASSWORD=$DB_PASSWORD" >> "$ENV_FILE"
    fi
fi

# 5. 修复 MySQL 权限（如果需要）
echo ""
echo -e "${GREEN}[4/8] 检查数据库权限...${NC}"
MYSQL_CONTAINER=$(read_config "docker" "services" "mysql" || echo "hsk-mysql")
DB_FIX_SQL=$(read_config "common_issues" "database_permission_fix" || echo "")

if [ -n "$DB_FIX_SQL" ]; then
    echo "修复数据库权限..."
    docker exec "$MYSQL_CONTAINER" mysql -uroot -p"$DB_PASSWORD" -e "$DB_FIX_SQL" 2>/dev/null || {
        echo "警告: 数据库权限修复失败，可能已经正确配置"
    }
fi

# 6. 确定要部署的服务
DEPLOY_TARGET="${1:-all}"
echo ""
echo -e "${GREEN}[5/8] 准备部署: $DEPLOY_TARGET${NC}"

# 7. 停止旧容器释放资源
echo ""
echo -e "${GREEN}[6/8] 停止旧容器释放资源...${NC}"
case "$DEPLOY_TARGET" in
    frontend-user)
        docker compose -f "$COMPOSE_FILE" stop frontend-user 2>/dev/null || true
        SERVICES="frontend-user"
        ;;
    frontend-admin)
        docker compose -f "$COMPOSE_FILE" stop frontend-admin 2>/dev/null || true
        SERVICES="frontend-admin"
        ;;
    backend)
        docker compose -f "$COMPOSE_FILE" stop backend 2>/dev/null || true
        SERVICES="backend"
        ;;
    all|*)
        docker compose -f "$COMPOSE_FILE" stop frontend-user frontend-admin backend 2>/dev/null || true
        SERVICES="frontend-user frontend-admin backend"
        ;;
esac
sleep 5

# 8. 重新创建容器（确保读取最新配置）
echo ""
echo -e "${GREEN}[7/8] 重新创建并启动容器...${NC}"
for service in $SERVICES; do
    echo "处理服务: $service"
    docker compose -f "$COMPOSE_FILE" rm -f "$service" 2>/dev/null || true
done
docker compose -f "$COMPOSE_FILE" up -d $SERVICES

# 9. 等待服务启动并检查状态
echo ""
echo -e "${GREEN}[8/8] 等待服务启动并检查状态...${NC}"
sleep 10

echo ""
echo -e "${BLUE}=========================================="
echo "部署完成！服务状态："
echo "==========================================${NC}"
docker compose -f "$COMPOSE_FILE" ps $SERVICES

echo ""
echo -e "${GREEN}查看日志:${NC}"
echo "  docker compose -f $COMPOSE_FILE logs -f $SERVICES"
echo ""
