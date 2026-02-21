#!/bin/bash

# 安全的部署脚本，自动处理交换空间和资源限制

set -e  # 遇到错误立即退出

echo "=========================================="
echo "开始安全部署流程"
echo "=========================================="

# 1. 检查并设置交换空间
echo ""
echo "步骤 1: 检查交换空间..."
if ! swapon --show | grep -q swapfile; then
    echo "交换空间未启用，正在设置..."
    bash setup-swap.sh
else
    echo "交换空间已启用"
    swapon --show
fi

# 2. 检查系统资源
echo ""
echo "步骤 2: 检查系统资源..."
echo "内存使用情况："
free -h
echo ""
echo "CPU 负载："
uptime

# 3. 等待系统负载降低（如果负载过高）
LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
LOAD_INT=${LOAD%.*}
if [ "$LOAD_INT" -gt 5 ]; then
    echo "警告：系统负载较高 ($LOAD)，等待 30 秒..."
    sleep 30
fi

# 4. 进入项目目录
cd /home/hsk || exit 1

# 5. 拉取最新代码
echo ""
echo "步骤 3: 拉取最新代码..."
git pull origin main || {
    echo "警告：git pull 失败，可能是网络问题，继续使用本地代码"
}

# 6. 停止旧容器（释放资源）
echo ""
echo "步骤 4: 停止旧容器释放资源..."
docker compose -f docker-compose.prod.yml stop frontend-user frontend-admin 2>/dev/null || true
sleep 5

# 7. 清理 Docker 缓存（可选，释放磁盘空间）
echo ""
read -p "是否清理 Docker 构建缓存以释放空间？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "清理 Docker 构建缓存..."
    docker builder prune -f
fi

# 8. 构建前端（限制并发，减少资源占用）
echo ""
echo "步骤 5: 构建前端镜像..."
echo "注意：构建过程可能需要较长时间，请耐心等待..."

# 设置 Docker 构建资源限制
export DOCKER_BUILDKIT=1
export BUILDKIT_STEP_LOG_MAX_SIZE=10485760  # 限制日志大小

# 逐个构建，避免同时构建导致资源耗尽
docker compose -f docker-compose.prod.yml build --no-cache frontend-user || {
    echo "错误：frontend-user 构建失败"
    exit 1
}

docker compose -f docker-compose.prod.yml build --no-cache frontend-admin || {
    echo "错误：frontend-admin 构建失败"
    exit 1
}

# 9. 启动容器
echo ""
echo "步骤 6: 启动容器..."
docker compose -f docker-compose.prod.yml up -d frontend-user frontend-admin

# 10. 检查容器状态
echo ""
echo "步骤 7: 检查容器状态..."
docker compose -f docker-compose.prod.yml ps

echo ""
echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo ""
echo "查看日志："
echo "  docker compose -f docker-compose.prod.yml logs frontend-user --tail 50"
echo "  docker compose -f docker-compose.prod.yml logs frontend-admin --tail 50"
