import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from django.db import connection
from django.apps import apps

print("=" * 80)
print("数据库表审计报告")
print("=" * 80)

# 获取所有表
cursor = connection.cursor()

# 检测数据库类型
db_engine = connection.settings_dict['ENGINE']
if 'sqlite' in db_engine:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    all_tables = [row[0] for row in cursor.fetchall()]
else:  # MySQL or other
    cursor.execute("SHOW TABLES;")
    all_tables = [row[0] for row in cursor.fetchall()]

print(f"\n总共 {len(all_tables)} 个表:\n")

# 分类表
django_system_tables = []
app_tables = {}

for table in all_tables:
    if table.startswith('django_') or table.startswith('auth_') or table.startswith('sqlite_'):
        django_system_tables.append(table)
    else:
        # 尝试找到对应的app
        found = False
        for app_config in apps.get_app_configs():
            if table.startswith(app_config.label + '_'):
                if app_config.label not in app_tables:
                    app_tables[app_config.label] = []
                app_tables[app_config.label].append(table)
                found = True
                break
        if not found:
            if 'other' not in app_tables:
                app_tables['other'] = []
            app_tables['other'].append(table)

# 输出系统表
print(f"Django系统表 ({len(django_system_tables)} 个):")
for table in django_system_tables:
    print(f"  - {table}")

# 输出应用表
print(f"\n应用表:")
for app, tables in sorted(app_tables.items()):
    print(f"\n{app.upper()} ({len(tables)} 个表):")
    for table in tables:
        # 检查表是否为空
        cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
        count = cursor.fetchone()[0]
        status = "[OK]" if count > 0 else "[EMPTY]"
        print(f"  {status} {table} ({count} records)")

print("\n" + "=" * 80)
print("模型字段审计")
print("=" * 80)

# 检查每个模型的字段
for app_config in apps.get_app_configs():
    if app_config.name in ['django.contrib.admin', 'django.contrib.auth', 
                           'django.contrib.contenttypes', 'django.contrib.sessions',
                           'django.contrib.messages', 'django.contrib.staticfiles']:
        continue
    
    models_list = app_config.get_models()
    if models_list:
        print(f"\n{app_config.label.upper()} 应用模型:")
        for model in models_list:
            print(f"\n  模型: {model.__name__}")
            print(f"  表名: {model._meta.db_table}")
            
            # 获取字段
            fields = model._meta.get_fields()
            for field in fields:
                if hasattr(field, 'column'):
                    # 检查字段是否有数据
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {model._meta.db_table} WHERE {field.column} IS NOT NULL AND {field.column} != ''")
                        non_null_count = cursor.fetchone()[0]
                        cursor.execute(f"SELECT COUNT(*) FROM {model._meta.db_table}")
                        total_count = cursor.fetchone()[0]
                        
                        if total_count > 0:
                            usage = f"{non_null_count}/{total_count}"
                            if non_null_count == 0:
                                status = "[UNUSED]"
                            elif non_null_count < total_count / 2:
                                status = "[LOW_USE]"
                            else:
                                status = "[OK]"
                        else:
                            usage = "0/0"
                            status = "[EMPTY]"
                        
                        print(f"    {status} {field.name} ({field.get_internal_type()}) - {usage}")
                    except Exception as e:
                        print(f"    ? {field.name} - 检查失败")

print("\n" + "=" * 80)
print("审计完成")
print("=" * 80)
