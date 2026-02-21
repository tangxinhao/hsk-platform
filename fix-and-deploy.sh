#!/bin/bash

# 紧急修复脚本：处理 Git 冲突、启用交换空间、释放资源、重新部署

set -e

echo "=========================================="
echo "紧急修复：处理卡死问题"
echo "=========================================="

# 1. 进入项目目录
cd /home/hsk || exit 1

# 2. 处理 Git 冲突（保存本地修改）
echo ""
echo "步骤 1: 处理 Git 冲突..."
if [ -n "$(git status --porcelain)" ]; then
    echo "发现本地修改，先保存..."
    git stash push -m "Auto stash before pull $(date +%Y%m%d_%H%M%S)" || {
        echo "警告: git stash 失败，尝试强制覆盖..."
        git reset --hard HEAD
    }
fi

# 3. 拉取最新代码
echo ""
echo "步骤 2: 拉取最新代码..."
git pull origin main || {
    echo "警告: git pull 失败，使用本地代码继续"
}

# 4. 启用交换空间（关键！）
echo ""
echo "步骤 3: 启用交换空间..."
if ! swapon --show | grep -q swapfile; then
    if [ -f /swapfile ]; then
        echo "启用现有交换文件..."
        swapon /swapfile 2>/dev/null || {
            echo "尝试重新格式化交换文件..."
            mkswap /swapfile
            swapon /swapfile
        }
    else
        echo "创建交换文件..."
        fallocate -l 2G /swapfile 2>/dev/null || dd if=/dev/zero of=/swapfile bs=1M count=2048
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
    fi
fi
echo "交换空间状态:"
free -h | grep Swap

# 5. 停止所有 Docker 构建和容器（释放资源）
echo ""
echo "步骤 4: 停止所有 Docker 进程释放资源..."
docker ps -q | xargs -r docker stop 2>/dev/null || true
docker ps -a -q | xargs -r docker rm -f 2>/dev/null || true
# 停止所有构建进程
pkill -f "docker.*build" 2>/dev/null || true
# 清理 Docker 构建缓存（释放内存）
docker builder prune -f 2>/dev/null || true

# 6. 等待系统恢复
echo ""
echo "步骤 5: 等待系统恢复（30秒）..."
sleep 30

# 7. 检查系统资源
echo ""
echo "步骤 6: 检查系统资源..."
echo "内存:"
free -h
echo ""
echo "负载:"
uptime

# 8. 给脚本添加执行权限
echo ""
echo "步骤 7: 准备部署脚本..."
chmod +x deploy_all.sh deploy-frontend-user.sh deploy-frontend-admin.sh setup-swap.sh 2>/dev/null || true

echo ""
echo "=========================================="
echo "修复完成！现在可以运行部署脚本："
echo "=========================================="
echo ""
echo "更新全部: ./deploy_all.sh"
echo "仅更新前端用户端: ./deploy-frontend-user.sh"
echo "仅更新前端管理端: ./deploy-frontend-admin.sh"
echo ""
