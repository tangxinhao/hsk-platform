import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hsk_project.settings")
django.setup()

# 运行迁移
from django.core.management import call_command
print("应用数据库迁移...")
call_command('makemigrations')
call_command('migrate')
print("数据库迁移完成!") 