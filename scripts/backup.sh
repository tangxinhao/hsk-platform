#!/bin/bash
# HSK学习平台 - 数据库备份脚本

set -e

# 配置
BACKUP_DIR="/home/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/hsk_backup_$DATE.sql"

# 加载环境变量
cd /home/hsk
source .env

# 创建备份目录
mkdir -p $BACKUP_DIR

echo "正在备份数据库..."
docker compose -f docker-compose.prod.yml exec -T db mysqldump -u root -p${DB_PASSWORD} ${DB_NAME} > $BACKUP_FILE

# 压缩备份
gzip $BACKUP_FILE

echo "备份完成: ${BACKUP_FILE}.gz"

# 删除7天前的备份
find $BACKUP_DIR -name "hsk_backup_*.sql.gz" -mtime +7 -delete
echo "已清理7天前的旧备份"
