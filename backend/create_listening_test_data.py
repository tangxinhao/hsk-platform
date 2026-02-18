#!/usr/bin/env python
"""
创建听力题目测试数据
基于HSK真题格式
"""
import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from question.models import QuestionSet, Question, QuestionCategory

def create_listening_questions():
    """创建听力题目样例数据"""
    print('=' * 60)
    print('开始创建听力题目测试数据...')
    print('=' * 60)
    
    # 获取或创建听力分类
    listening_category, _ = QuestionCategory.objects.get_or_create(
        name='listening',
        defaults={'description': 'HSK听力理解题目'}
    )
    
    created_count = 0
    
    # 为HSK 1-6级创建听力题目
    for level in range(1, 7):
        # 获取或创建该等级的套卷
        question_set, created = QuestionSet.objects.get_or_create(
            title=f'HSK{level}听力专项练习',
            level=level,
            defaults={
                'description': f'HSK{level}级听力理解专项练习，包含各类听力题型',
                'time_limit': 30 if level <= 3 else 45,
                'question_count': 0
            }
        )
        
        if created:
            print(f'\n[新建] 创建套卷: {question_set.title}')
        else:
            print(f'\n[OK] 套卷已存在: {question_set.title}')
        
        # 创建听力题目
        listening_questions = []
        
        if level == 1:
            # HSK1 听力题目示例
            listening_questions = [
                {
                    'content': '请听录音，选择正确的图片。',
                    'options': ['图片A：一个人在看书', '图片B：一个人在写字', '图片C：一个人在说话', '图片D：一个人在听音乐'],
                    'answer': '图片A：一个人在看书',
                    'audio_url': '/media/audio/H11556.mp3',
                    'audio_duration': 10
                },
                {
                    'content': '请听对话，判断说话人的关系。',
                    'options': ['老师和学生', '医生和病人', '售货员和顾客', '朋友'],
                    'answer': '老师和学生',
                    'audio_url': '/media/audio/sample1.mp3',
                    'audio_duration': 15
                },
            ]
        elif level == 2:
            listening_questions = [
                {
                    'content': '男：你今天去哪儿了？\n女：我去图书馆了。\n问：女的去哪儿了？',
                    'options': ['商店', '图书馆', '学校', '医院'],
                    'answer': '图书馆',
                    'audio_url': '/media/audio/sample2.mp3',
                    'audio_duration': 12
                },
                {
                    'content': '女：这个多少钱？\n男：二十块。\n问：东西多少钱？',
                    'options': ['十块', '二十块', '三十块', '四十块'],
                    'answer': '二十块',
                    'audio_url': '/media/audio/sample3.mp3',
                    'audio_duration': 10
                },
            ]
        elif level == 3:
            listening_questions = [
                {
                    'content': '男：你觉得这部电影怎么样？\n女：我觉得很有意思，但是有点儿长。\n问：女的觉得电影怎么样？',
                    'options': ['很无聊', '很有意思但有点长', '很短', '不好看'],
                    'answer': '很有意思但有点长',
                    'audio_url': '/media/audio/sample4.mp3',
                    'audio_duration': 18
                },
                {
                    'content': '女：明天的会议改到下午三点了。\n男：好的，我知道了。\n问：会议什么时候开？',
                    'options': ['上午九点', '中午十二点', '下午三点', '晚上六点'],
                    'answer': '下午三点',
                    'audio_url': '/media/audio/sample5.mp3',
                    'audio_duration': 15
                },
            ]
        elif level == 4:
            listening_questions = [
                {
                    'content': '''女：小李，听说你最近在学习中国书法？
男：是的，我觉得中国书法很有艺术价值，想好好学习一下。
女：那你觉得难吗？
男：刚开始确实有点难，但是慢慢就好了。
问：关于小李，可以知道什么？''',
                    'options': ['他觉得书法很简单', '他正在学习中国书法', '他不喜欢艺术', '他已经学了很久'],
                    'answer': '他正在学习中国书法',
                    'audio_url': '/media/audio/sample6.mp3',
                    'audio_duration': 25
                },
            ]
        elif level == 5:
            listening_questions = [
                {
                    'content': '''（采访录音）
记者：王教授，您对目前中国的环境保护工作有什么看法？
王教授：我认为近年来中国在环境保护方面取得了显著的进步，但仍然面临很多挑战。比如空气污染、水资源保护等问题还需要继续努力。
记者：您觉得普通人能做些什么？
王教授：普通人可以从日常生活做起，比如节约用水、垃圾分类、绿色出行等等。
问：根据对话，下列哪项正确？''',
                    'options': [
                        '中国的环境保护工作没有进步',
                        '空气污染问题已经完全解决',
                        '普通人可以通过日常行为参与环保',
                        '水资源很充足'
                    ],
                    'answer': '普通人可以通过日常行为参与环保',
                    'audio_url': '/media/audio/sample7.mp3',
                    'audio_duration': 45
                },
            ]
        else:  # level == 6
            listening_questions = [
                {
                    'content': '''（讲座片段）
中国的茶文化源远流长，可以追溯到几千年前。茶不仅是一种饮料，更是一种文化符号。在中国传统文化中，茶道讲究"和、敬、清、寂"，这四个字概括了茶文化的精髓。品茶的过程也是一种修身养性的过程，通过品茶可以让人静下心来，思考人生。
问：根据讲座，下列哪项不正确？''',
                    'options': [
                        '中国茶文化历史悠久',
                        '茶在中国只是一种普通饮料',
                        '茶道讲究"和、敬、清、寂"',
                        '品茶是一种修身养性的方式'
                    ],
                    'answer': '茶在中国只是一种普通饮料',
                    'audio_url': '/media/audio/sample8.mp3',
                    'audio_duration': 60
                },
            ]
        
        # 创建题目
        for i, q_data in enumerate(listening_questions):
            Question.objects.create(
                type='listening',
                level=level,
                content=q_data['content'],
                answer=q_data['answer'],
                options=json.dumps(q_data['options'], ensure_ascii=False),
                category=listening_category,
                question_set=question_set,
                difficulty=min(level, 5),
                audio_url=q_data['audio_url'],
                audio_duration=q_data['audio_duration'],
                explanation=f'这是HSK{level}级听力题目，考查听力理解能力。'
            )
            created_count += 1
        
        # 更新套卷题目数量
        question_set.question_count = Question.objects.filter(question_set=question_set).count()
        question_set.save()
        
        print(f'  [OK] 创建了 {len(listening_questions)} 道听力题目')
    
    print('\n' + '=' * 60)
    print('听力题目创建完成！')
    print('=' * 60)
    print(f'本次创建听力题目: {created_count} 道')
    print(f'听力题目总数: {Question.objects.filter(type="listening").count()} 道')
    print(f'所有题目总数: {Question.objects.count()} 道')
    print('=' * 60)
    print('\n[提示] 请将音频文件放置在: backend/media/audio/ 目录下')
    print('[提示] 或在管理后台上传音频文件')
    print('\n[SUCCESS] 所有听力测试数据已就绪！')

if __name__ == '__main__':
    try:
        create_listening_questions()
    except Exception as e:
        print(f'\n[ERROR] 创建听力题目时出错: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
