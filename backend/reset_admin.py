#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
重置admin用户密码
"""
import os
import sys
import io

# 设置输出编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from user.models import User
from django.contrib.auth import authenticate

def reset_admin_password():
    """重置admin密码为admin123456"""
    try:
        # 查找admin用户
        admin = User.objects.filter(username='admin').first()
        
        if not admin:
            print('[!] Admin用户不存在，开始创建...')
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123456'
            )
            print('[OK] Admin用户创建成功！')
        else:
            print(f'[INFO] 找到Admin用户: {admin.username}')
            # 重置密码
            admin.set_password('admin123456')
            admin.is_staff = True
            admin.is_superuser = True
            admin.is_active = True
            admin.save()
            print('[OK] Admin密码已重置为: admin123456')
        
        # 验证
        test_user = authenticate(username='admin', password='admin123456')
        
        if test_user:
            print('\n' + '='*50)
            print('[SUCCESS] 密码验证成功！')
            print('='*50)
            print(f'用户名: {test_user.username}')
            print(f'邮箱: {test_user.email}')
            print(f'Staff: {test_user.is_staff}')
            print(f'Superuser: {test_user.is_superuser}')
            print(f'Active: {test_user.is_active}')
            print('\n现在可以使用以下凭证登录:')
            print('  用户名: admin')
            print('  密码: admin123456')
            print('='*50)
            return True
        else:
            print('\n[ERROR] 密码验证失败！请检查数据库设置')
            return False
            
    except Exception as e:
        print(f'[ERROR] 错误: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    reset_admin_password()
