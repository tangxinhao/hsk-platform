#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
清空所有测试数据的脚本
"""
import os
import sys
import django

# 设置输出编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from question.models import Question, QuestionSet, AnswerRecord, WrongBook
from question.exam_models import ExamAttempt, ExamReport, ExamRanking

def clear_all_data():
    """清空所有测试数据"""
    print("\n" + "="*60)
    print("开始清空测试数据...")
    print("="*60 + "\n")
    
    try:
        # 清空考试相关数据
        print("1. 清空考试记录...")
        
        try:
            ExamRanking.objects.all().delete()
            print("   ✓ 已删除所有考试排名")
        except Exception as e:
            print(f"   ⚠ 考试排名表可能不存在: {str(e)}")
        
        try:
            ExamReport.objects.all().delete()
            print("   ✓ 已删除所有考试报告")
        except Exception as e:
            print(f"   ⚠ 考试报告表可能不存在: {str(e)}")
        
        try:
            ExamAttempt.objects.all().delete()
            print("   ✓ 已删除所有考试尝试记录")
        except Exception as e:
            print(f"   ⚠ 考试尝试记录表可能不存在: {str(e)}")
        
        # 清空答题记录
        print("\n2. 清空答题记录...")
        try:
            WrongBook.objects.all().delete()
            print("   ✓ 已删除所有错题本记录")
        except Exception as e:
            print(f"   ⚠ 错题本表可能不存在: {str(e)}")
        
        try:
            AnswerRecord.objects.all().delete()
            print("   ✓ 已删除所有答题记录")
        except Exception as e:
            print(f"   ⚠ 答题记录表可能不存在: {str(e)}")
        
        # 清空题目数据
        print("\n3. 清空题目数据...")
        Question.objects.all().delete()
        print("   ✓ 已删除所有题目")
        
        # 清空套卷数据
        print("\n4. 清空套卷数据...")
        QuestionSet.objects.all().delete()
        print("   ✓ 已删除所有套卷")
        
        print("\n" + "="*60)
        print("✓ 所有测试数据已清空！")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 清空数据时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    clear_all_data()
