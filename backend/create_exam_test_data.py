#!/usr/bin/env python
"""
创建HSK考试测试数据
快速创建套卷和题目用于测试
"""
import os
import sys
import django
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from question.models import QuestionSet, Question

def create_test_exam_sets():
    """创建测试考试套卷和题目"""
    print('=' * 60)
    print('开始创建HSK考试测试数据...')
    print('=' * 60)
    
    created_sets = 0
    created_questions = 0
    
    # 为HSK 1-6级各创建一套测试题
    for level in range(1, 7):
        set_title = f'HSK{level}模拟试卷A'
        
        # 检查是否已存在
        if QuestionSet.objects.filter(level=level, title=set_title).exists():
            print(f'[OK] {set_title} 已存在，跳过创建')
            continue
        
        # 创建套卷
        question_set = QuestionSet.objects.create(
            title=set_title,
            description=f'HSK{level}级别标准模拟试卷，适合备考练习使用。包含听力、阅读、书写等各类题型。',
            level=level,
            time_limit=60 if level <= 3 else 90,  # 1-3级60分钟，4-6级90分钟
            question_count=0  # 先设为0，后面会更新
        )
        
        print(f'\n[OK] 创建套卷: {question_set.title}')
        created_sets += 1
        
        # 为每个套卷创建20道测试题
        question_types = ['单选题', '填空题', '判断题', '多选题']
        
        for i in range(20):
            question_type = question_types[i % len(question_types)]
            
            # 根据题型创建不同的选项和答案
            if question_type == '单选题':
                options = [
                    f'选项A：这是第{i+1}题的选项A',
                    f'选项B：这是第{i+1}题的选项B',
                    f'选项C：这是第{i+1}题的选项C',
                    f'选项D：这是第{i+1}题的选项D'
                ]
                options_json = json.dumps(options, ensure_ascii=False)
                answer = options[0]  # 正确答案是第一个选项
                
            elif question_type == '多选题':
                options = [
                    f'选项A：这是第{i+1}题的选项A',
                    f'选项B：这是第{i+1}题的选项B',
                    f'选项C：这是第{i+1}题的选项C',
                    f'选项D：这是第{i+1}题的选项D'
                ]
                options_json = json.dumps(options, ensure_ascii=False)
                answer = f'{options[0]},{options[1]}'  # 正确答案是前两个选项
                
            elif question_type == '判断题':
                options_json = '[]'  # 空JSON数组而不是空字符串
                answer = '正确' if i % 2 == 0 else '错误'
                
            else:  # 填空题
                options_json = '[]'  # 空JSON数组而不是空字符串
                answer = f'测试答案{i+1}'
            
            # 创建题目（不包含explanation字段，因为数据库表中可能没有）
            question_data = {
                'type': question_type,
                'level': level,
                'content': f'这是HSK{level}的第{i+1}道{question_type}。请根据题目要求选择或填写正确答案。题目内容测试数据...',
                'answer': answer,
                'options': options_json,
                'question_set': question_set,
            }
            
            # 尝试添加可选字段
            try:
                question_data['difficulty'] = min(level, 5)
            except:
                pass
                
            try:
                question_data['explanation'] = f'【解析】这是第{i+1}题的详细解析说明。正确答案是"{answer}"。'
            except:
                pass
            
            Question.objects.create(**question_data)
            created_questions += 1
        
        # 更新套卷的题目数量
        question_set.question_count = 20
        question_set.save()
        
        print(f'  [OK] 创建了 20 道题目')
    
    print('\n' + '=' * 60)
    print('测试数据创建完成！')
    print('=' * 60)
    print(f'本次创建：')
    print(f'  - 套卷数: {created_sets} 套')
    print(f'  - 题目数: {created_questions} 道')
    print(f'\n数据库统计：')
    print(f'  - 总套卷数: {QuestionSet.objects.count()} 套')
    print(f'  - 总题目数: {Question.objects.count()} 道')
    print('=' * 60)
    
    # 显示每个等级的统计
    print('\n各等级套卷统计：')
    for level in range(1, 7):
        count = QuestionSet.objects.filter(level=level).count()
        q_count = Question.objects.filter(level=level).count()
        print(f'  HSK{level}: {count} 套套卷, {q_count} 道题目')
    
    print('\n[SUCCESS] 所有测试数据已就绪，可以开始使用系统了！')

if __name__ == '__main__':
    try:
        create_test_exam_sets()
    except Exception as e:
        print(f'\n[ERROR] 创建测试数据时出错: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
