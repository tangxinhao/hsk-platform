#!/bin/bash
# 初始化HSK学习系统数据库
# 请确保已启动MySQL服务，并将下方SQL脚本手动导入
# 使用方法：bash scripts/init_db.sh

# 手动执行区域：
# 请在MySQL命令行或可视化工具中执行 database/hsk_schema.sql
# 例如：
# mysql -u root -p123456 hsk_learning < database/hsk_schema.sql

echo "请手动将 database/hsk_schema.sql 导入到 hsk_learning 数据库。" 