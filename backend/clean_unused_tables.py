#!/usr/bin/env python
"""
清理不需要的数据库表
删除 question_audiofile 和 question_paperimport 表
"""

import os
import sys
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

# Configure stdout for UTF-8 encoding (Windows compatibility)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from django.db import connection

def drop_unused_tables():
    """删除不再使用的数据库表"""
    tables_to_drop = [
        'question_audiofile',
        'question_paperimport'
    ]
    
    print("=" * 60)
    print("清理不需要的数据库表")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        for table in tables_to_drop:
            try:
                # 检查表是否存在
                cursor.execute(f"""
                    SELECT COUNT(*)
                    FROM information_schema.tables 
                    WHERE table_schema = DATABASE()
                    AND table_name = '{table}'
                """)
                
                if cursor.fetchone()[0] > 0:
                    print(f"\n[处理中] 删除表: {table}")
                    
                    # 删除表
                    cursor.execute(f"DROP TABLE IF EXISTS {table}")
                    print(f"  ✓ 成功删除表: {table}")
                else:
                    print(f"\n[跳过] 表不存在: {table}")
                    
            except Exception as e:
                print(f"\n  ✗ 删除表 {table} 失败: {e}")
                print(f"  提示: 如果表有外键关联，可能需要手动删除")
    
    print("\n" + "=" * 60)
    print("表清理完成!")
    print("=" * 60)
    print("\n说明:")
    print("  - question_audiofile: 音频信息已整合到 Question 模型")
    print("  - question_paperimport: 使用脚本导入，不需要数据库表")
    print("\n如需导入试卷，请使用: python backend/create_hsk_real_test_data.py")
    print("=" * 60)

if __name__ == '__main__':
    try:
        drop_unused_tables()
    except Exception as e:
        print(f"\n[错误] 清理过程中出现错误: {e}")
        sys.exit(1)
