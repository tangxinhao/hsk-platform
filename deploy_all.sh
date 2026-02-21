#!/bin/bash

# 更新全部服务（前端+后端）
# 使用方法: cd /home/hsk && ./deploy_all.sh

set -e  # 遇到错误立即退出

echo "=========================================="
echo "开始更新全部服务"
echo "=========================================="

# 1. 检查并启用交换空间
echo ""
echo "步骤 1: 检查交换空间..."
if ! swapon --show | grep -q swapfile; then
    if [ -f /swapfile ]; then
        echo "发现交换文件，正在启用..."
        swapon /swapfile 2>/dev/null || true
    else
        echo "设置交换空间..."
        bash setup-swap.sh 2>/dev/null || true
    fi
fi
echo "交换空间状态:"
free -h | grep Swap

# 2. 进入项目目录
cd /home/hsk || exit 1

# 3. 拉取最新代码
echo ""
echo "步骤 2: 拉取最新代码..."
git pull origin main || {
    echo "警告: git pull 失败，继续使用本地代码"
}

# 4. 停止旧容器释放资源
echo ""
echo "步骤 3: 停止旧容器释放资源..."
docker compose -f docker-compose.prod.yml stop frontend-user frontend-admin backend 2>/dev/null || true
sleep 5

# 5. 构建所有服务
echo ""
echo "步骤 4: 构建所有服务..."
docker compose -f docker-compose.prod.yml build frontend-user frontend-admin backend

# 6. 启动所有服务
echo ""
echo "步骤 5: 启动所有服务..."
docker compose -f docker-compose.prod.yml up -d frontend-user frontend-admin backend

# 7. 等待服务启动
echo ""
echo "步骤 6: 等待服务启动..."
sleep 10

# 8. 查看服务状态
echo ""
echo "=========================================="
echo "部署完成！服务状态："
echo "=========================================="
docker compose -f docker-compose.prod.yml ps

echo ""
echo "查看日志: docker compose -f docker-compose.prod.yml logs -f"
echo ""
