#!/bin/bash

# 配置文件同步脚本
# 当修改了 docker-compose.prod.yml 或 .env 后，运行此脚本更新 server-config.json

set -e

CONFIG_FILE="server-config.json"
COMPOSE_FILE="docker-compose.prod.yml"
ENV_FILE=".env"

echo "检查配置文件更新..."

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo "错误: 需要 Python 3 来更新配置文件"
    exit 1
fi

# 使用 Python 更新配置文件
python3 << 'PYTHON_SCRIPT'
import json
import os
import re

config_file = "server-config.json"
compose_file = "docker-compose.prod.yml"
env_file = ".env"

# 读取现有配置
with open(config_file, 'r', encoding='utf-8') as f:
    config = json.load(f)

# 从 .env 文件读取配置（如果存在）
env_vars = {}
if os.path.exists(env_file):
    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

# 更新数据库配置
if 'DB_PASSWORD' in env_vars:
    config['database']['password'] = env_vars['DB_PASSWORD']
if 'DB_NAME' in env_vars:
    config['database']['name'] = env_vars['DB_NAME']
if 'DB_USER' in env_vars:
    config['database']['user'] = env_vars['DB_USER']

# 更新 Django 配置
if 'SECRET_KEY' in env_vars:
    config['django']['secret_key'] = env_vars['SECRET_KEY']
if 'ALLOWED_HOSTS' in env_vars:
    config['django']['allowed_hosts'] = env_vars['ALLOWED_HOSTS']
if 'API_BASE_URL' in env_vars:
    config['django']['api_base_url'] = env_vars['API_BASE_URL']

# 更新最后修改时间
from datetime import datetime
config['notes']['last_updated'] = datetime.now().strftime('%Y-%m-%d')

# 保存配置
with open(config_file, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"配置文件已更新: {config_file}")
PYTHON_SCRIPT

echo "完成！"
