"""检查数据库表"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    
    print("\n数据库表列表：")
    print("="*60)
    for table in sorted(tables):
        print(f"  - {table[0]}")
    print("="*60)
    print(f"总计：{len(tables)}个表\n")
