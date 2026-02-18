"""
创建测试用户脚本
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from user.models import User

def create_test_users():
    """创建测试用户"""
    
    # 创建普通测试用户
    if not User.objects.filter(username='test').exists():
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123456',
            phone='13800138000'
        )
        print(f'✓ 创建测试用户成功: {user.username}')
    else:
        print('○ 测试用户已存在: test')
    
    # 创建管理员用户
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123456',
            phone='13900139000'
        )
        print(f'✓ 创建管理员成功: {admin.username}')
    else:
        print('○ 管理员已存在: admin')
    
    # 显示所有用户
    print('\n当前所有用户:')
    for user in User.objects.all():
        print(f'  - {user.username} ({"管理员" if user.is_superuser else "普通用户"})')
    
    print('\n可以使用以下账号登录:')
    print('  普通用户: test / test123456')
    print('  管理员: admin / admin123456')

if __name__ == '__main__':
    create_test_users()
