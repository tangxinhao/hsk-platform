#!/bin/bash

# 设置交换空间脚本
# 用于解决服务器内存不足导致构建卡死的问题

SWAP_SIZE=2G  # 交换空间大小，根据服务器磁盘空间调整

echo "检查交换空间状态..."

# 检查是否已有交换空间
if swapon --show | grep -q swapfile; then
    echo "交换空间已存在，跳过创建"
    swapon --show
    exit 0
fi

# 检查磁盘空间
AVAILABLE_SPACE=$(df -BG / | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$AVAILABLE_SPACE" -lt 3 ]; then
    echo "警告：磁盘空间不足，无法创建 ${SWAP_SIZE} 交换空间"
    exit 1
fi

echo "创建 ${SWAP_SIZE} 交换空间..."

# 创建交换文件
fallocate -l ${SWAP_SIZE} /swapfile 2>/dev/null || dd if=/dev/zero of=/swapfile bs=1M count=2048

# 设置权限
chmod 600 /swapfile

# 格式化为交换空间
mkswap /swapfile

# 启用交换空间
swapon /swapfile

# 验证
echo "交换空间已启用："
swapon --show
free -h

# 添加到 /etc/fstab 使其永久生效
if ! grep -q "/swapfile" /etc/fstab; then
    echo "/swapfile none swap sw 0 0" >> /etc/fstab
    echo "已添加到 /etc/fstab，重启后自动启用"
fi

echo "完成！"
