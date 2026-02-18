#!/usr/bin/env python
"""
重置admin用户密码
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from user.models import User

def reset_admin_password():
    """重置admin密码为admin123456"""
    try:
        # 查找admin用户
        admin = User.objects.filter(username='admin').first()
        
        if not admin:
            print('❌ Admin用户不存在，开始创建...')
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123456'
            )
            print('✅ Admin用户创建成功！')
        else:
            # 重置密码
            admin.set_password('admin123456')
            admin.is_staff = True
            admin.is_superuser = True
            admin.is_active = True
            admin.save()
            print('✅ Admin密码已重置为: admin123456')
        
        # 验证
        from django.contrib.auth import authenticate
        test_user = authenticate(username='admin', password='admin123456')
        
        if test_user:
            print('✅ 密码验证成功！')
            print(f'   用户名: {test_user.username}')
            print(f'   邮箱: {test_user.email}')
            print(f'   Staff状态: {test_user.is_staff}')
            print(f'   Superuser状态: {test_user.is_superuser}')
            print('\n现在可以使用以下凭证登录:')
            print('   用户名: admin')
            print('   密码: admin123456')
        else:
            print('❌ 密码验证失败！')
            
    except Exception as e:
        print(f'❌ 错误: {e}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    reset_admin_password()
