"""
测试数据初始化脚本
运行方式: python manage.py shell < init_test_data.py
或: python manage.py runscript init_test_data
"""

import os
import django
import json
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from question.models import QuestionCategory, QuestionSet, Question
from university.models import University
from culture.models import Category as CultureCategory, Content as CultureContent
from user.models import User

def create_question_categories():
    """创建题目分类"""
    categories = [
        ('vocabulary', '词汇'),
        ('reading', '阅读'),
        ('listening', '听力'),
        ('writing', '写作'),
        ('grammar', '语法'),
        ('comprehensive', '综合')
    ]
    
    created_categories = []
    for name, description in categories:
        category, created = QuestionCategory.objects.get_or_create(
            name=name,
            defaults={'description': description}
        )
        created_categories.append(category)
        if created:
            print(f'[OK] 创建分类: {description}')
        else:
            print(f'[SKIP] 分类已存在: {description}')
    
    return created_categories

def create_question_sets():
    """创建套卷"""
    sets_data = [
        {
            'title': 'HSK1标准模拟试卷（一）',
            'description': 'HSK1级别完整模拟考试，适合初学者',
            'level': 1,
            'time_limit': 90,
            'question_count': 0
        },
        {
            'title': 'HSK2标准模拟试卷（一）',
            'description': 'HSK2级别完整模拟考试',
            'level': 2,
            'time_limit': 100,
            'question_count': 0
        },
        {
            'title': 'HSK3标准模拟试卷（一）',
            'description': 'HSK3级别完整模拟考试',
            'level': 3,
            'time_limit': 120,
            'question_count': 0
        },
        {
            'title': 'HSK4标准模拟试卷（一）',
            'description': 'HSK4级别完整模拟考试',
            'level': 4,
            'time_limit': 150,
            'question_count': 0
        },
    ]
    
    created_sets = []
    for set_data in sets_data:
        question_set, created = QuestionSet.objects.get_or_create(
            title=set_data['title'],
            defaults=set_data
        )
        created_sets.append(question_set)
        if created:
            print(f'[OK] 创建套卷: {set_data["title"]}')
        else:
            print(f'[SKIP] 套卷已存在: {set_data["title"]}')
    
    return created_sets

def create_questions():
    """创建题目"""
    vocab_category = QuestionCategory.objects.get(name='vocabulary')
    grammar_category = QuestionCategory.objects.get(name='grammar')
    
    hsk1_set = QuestionSet.objects.get(title='HSK1标准模拟试卷（一）')
    hsk2_set = QuestionSet.objects.get(title='HSK2标准模拟试卷（一）')
    
    questions_data = [
        # HSK1 单选题
        {
            'type': '单选题',
            'level': 1,
            'content': '"你好" 的意思是？',
            'options': json.dumps([
                {'content': 'Hello', 'isCorrect': True},
                {'content': 'Goodbye', 'isCorrect': False},
                {'content': 'Thank you', 'isCorrect': False},
                {'content': 'Sorry', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': 'Hello',
            'category': vocab_category,
            'question_set': hsk1_set,
            'difficulty': 1
        },
        {
            'type': '单选题',
            'level': 1,
            'content': '"谢谢" 的意思是？',
            'options': json.dumps([
                {'content': 'Hello', 'isCorrect': False},
                {'content': 'Thank you', 'isCorrect': True},
                {'content': 'Sorry', 'isCorrect': False},
                {'content': 'Goodbye', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': 'Thank you',
            'category': vocab_category,
            'question_set': hsk1_set,
            'difficulty': 1
        },
        {
            'type': '单选题',
            'level': 1,
            'content': '"再见" 的意思是？',
            'options': json.dumps([
                {'content': 'Hello', 'isCorrect': False},
                {'content': 'Thank you', 'isCorrect': False},
                {'content': 'Goodbye', 'isCorrect': True},
                {'content': 'Sorry', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': 'Goodbye',
            'category': vocab_category,
            'question_set': hsk1_set,
            'difficulty': 1
        },
        {
            'type': '单选题',
            'level': 1,
            'content': '我___学生。',
            'options': json.dumps([
                {'content': '是', 'isCorrect': True},
                {'content': '在', 'isCorrect': False},
                {'content': '有', 'isCorrect': False},
                {'content': '去', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': '是',
            'category': grammar_category,
            'question_set': hsk1_set,
            'difficulty': 1
        },
        {
            'type': '单选题',
            'level': 1,
            'content': '他___中国人。',
            'options': json.dumps([
                {'content': '在', 'isCorrect': False},
                {'content': '是', 'isCorrect': True},
                {'content': '有', 'isCorrect': False},
                {'content': '到', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': '是',
            'category': grammar_category,
            'question_set': hsk1_set,
            'difficulty': 1
        },
        # HSK1 判断题
        {
            'type': '判断题',
            'level': 1,
            'content': '"我爱你" 的意思是 "I love you"。',
            'options': '',
            'answer': '正确',
            'category': vocab_category,
            'question_set': hsk1_set,
            'difficulty': 1
        },
        {
            'type': '判断题',
            'level': 1,
            'content': '"对不起" 的意思是 "Thank you"。',
            'options': '',
            'answer': '错误',
            'category': vocab_category,
            'question_set': hsk1_set,
            'difficulty': 1
        },
        # HSK1 填空题
        {
            'type': '填空题',
            'level': 1,
            'content': '你___吗？（你好吗？）',
            'options': '',
            'answer': '好',
            'category': vocab_category,
            'question_set': hsk1_set,
            'difficulty': 2
        },
        {
            'type': '填空题',
            'level': 1,
            'content': '我___小明。（介绍名字）',
            'options': '',
            'answer': '叫',
            'category': vocab_category,
            'question_set': hsk1_set,
            'difficulty': 2
        },
        # HSK2 题目
        {
            'type': '单选题',
            'level': 2,
            'content': '我___在图书馆看书。',
            'options': json.dumps([
                {'content': '正', 'isCorrect': False},
                {'content': '正在', 'isCorrect': True},
                {'content': '在正', 'isCorrect': False},
                {'content': '在', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': '正在',
            'category': grammar_category,
            'question_set': hsk2_set,
            'difficulty': 2
        },
        {
            'type': '单选题',
            'level': 2,
            'content': '今天天气___。',
            'options': json.dumps([
                {'content': '很好', 'isCorrect': True},
                {'content': '很高', 'isCorrect': False},
                {'content': '很大', 'isCorrect': False},
                {'content': '很多', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': '很好',
            'category': vocab_category,
            'question_set': hsk2_set,
            'difficulty': 2
        },
        {
            'type': '单选题',
            'level': 2,
            'content': '我___去超市买东西。',
            'options': json.dumps([
                {'content': '想', 'isCorrect': True},
                {'content': '觉得', 'isCorrect': False},
                {'content': '认为', 'isCorrect': False},
                {'content': '知道', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': '想',
            'category': grammar_category,
            'question_set': hsk2_set,
            'difficulty': 2
        },
        {
            'type': '多选题',
            'level': 2,
            'content': '下列哪些是水果？',
            'options': json.dumps([
                {'content': '苹果', 'isCorrect': True},
                {'content': '香蕉', 'isCorrect': True},
                {'content': '椅子', 'isCorrect': False},
                {'content': '桌子', 'isCorrect': False}
            ], ensure_ascii=False),
            'answer': '苹果,香蕉',
            'category': vocab_category,
            'question_set': hsk2_set,
            'difficulty': 2
        },
        {
            'type': '填空题',
            'level': 2,
            'content': '我每天___点起床。（早上7点）',
            'options': '',
            'answer': '七',
            'category': vocab_category,
            'question_set': hsk2_set,
            'difficulty': 2
        },
    ]
    
    created_count = 0
    for q_data in questions_data:
        question, created = Question.objects.get_or_create(
            content=q_data['content'],
            level=q_data['level'],
            defaults=q_data
        )
        if created:
            created_count += 1
    
    print(f'[OK] 创建了 {created_count} 道题目')
    return created_count

def create_universities():
    """创建院校数据"""
    universities_data = [
        {
            'name': '北京大学',
            'name_en': 'Peking University',
            'region': '北京',
            'city': '北京市',
            'ranking_national': 1,
            'ranking_world': 18,
            'website': 'https://www.pku.edu.cn',
            'description': '中国最顶尖的综合性大学之一',
            'tuition_fee': 25000.00,
            'hsk_requirement': 6,
            'majors': json.dumps(['计算机科学', '经济学', '法学', '中文'], ensure_ascii=False)
        },
        {
            'name': '清华大学',
            'name_en': 'Tsinghua University',
            'region': '北京',
            'city': '北京市',
            'ranking_national': 2,
            'ranking_world': 17,
            'website': 'https://www.tsinghua.edu.cn',
            'description': '中国顶尖的理工科大学',
            'tuition_fee': 26000.00,
            'hsk_requirement': 6,
            'majors': json.dumps(['工程学', '计算机科学', '建筑学', '经济学'], ensure_ascii=False)
        },
        {
            'name': '复旦大学',
            'name_en': 'Fudan University',
            'region': '上海',
            'city': '上海市',
            'ranking_national': 3,
            'ranking_world': 34,
            'website': 'https://www.fudan.edu.cn',
            'description': '位于上海的综合性研究型大学',
            'tuition_fee': 24000.00,
            'hsk_requirement': 5,
            'majors': json.dumps(['新闻学', '经济学', '医学', '数学'], ensure_ascii=False)
        },
        {
            'name': '浙江大学',
            'name_en': 'Zhejiang University',
            'region': '浙江',
            'city': '杭州市',
            'ranking_national': 4,
            'ranking_world': 42,
            'website': 'https://www.zju.edu.cn',
            'description': '历史悠久的综合性大学',
            'tuition_fee': 23000.00,
            'hsk_requirement': 5,
            'majors': json.dumps(['工程学', '农学', '医学', '管理学'], ensure_ascii=False)
        },
        {
            'name': '上海交通大学',
            'name_en': 'Shanghai Jiao Tong University',
            'region': '上海',
            'city': '上海市',
            'ranking_national': 5,
            'ranking_world': 46,
            'website': 'https://www.sjtu.edu.cn',
            'description': '以工科见长的研究型大学',
            'tuition_fee': 24500.00,
            'hsk_requirement': 5,
            'majors': json.dumps(['机械工程', '电子工程', '医学', '商学'], ensure_ascii=False)
        },
    ]
    
    created_count = 0
    for uni_data in universities_data:
        university, created = University.objects.get_or_create(
            name=uni_data['name'],
            defaults=uni_data
        )
        if created:
            created_count += 1
    
    print(f'[OK] 创建了 {created_count} 所大学')
    return created_count

def create_culture_content():
    """创建文化内容"""
    # 创建文化分类
    categories_data = [
        {'name': '节日习俗', 'description': '中国传统节日和习俗'},
        {'name': '历史典故', 'description': '中国历史故事和典故'},
        {'name': '成语故事', 'description': '中国成语及其来源'},
    ]
    
    culture_categories = []
    for cat_data in categories_data:
        category, created = CultureCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        culture_categories.append(category)
        if created:
            print(f'[OK] 创建文化分类: {cat_data["name"]}')
    
    # 创建文化内容
    festival_cat = CultureCategory.objects.get(name='节日习俗')
    idiom_cat = CultureCategory.objects.get(name='成语故事')
    
    contents_data = [
        {
            'title': '春节',
            'category': festival_cat,
            'content': '春节是中国最重要的传统节日，通常在农历正月初一。人们会贴春联、放鞭炮、吃饺子、拜年等。',
            'content_type': 'article',
            'difficulty': 1,
            'reading_time': 5
        },
        {
            'title': '中秋节',
            'category': festival_cat,
            'content': '中秋节在农历八月十五，是团圆的节日。人们会赏月、吃月饼、和家人团聚。',
            'content_type': 'article',
            'difficulty': 1,
            'reading_time': 5
        },
        {
            'title': '愚公移山',
            'category': idiom_cat,
            'content': '愚公移山的故事告诉我们：只要坚持不懈，再大的困难也能克服。',
            'content_type': 'article',
            'difficulty': 2,
            'reading_time': 10
        },
    ]
    
    created_count = 0
    for content_data in contents_data:
        content, created = CultureContent.objects.get_or_create(
            title=content_data['title'],
            defaults=content_data
        )
        if created:
            created_count += 1
    
    print(f'[OK] 创建了 {created_count} 篇文化内容')
    return created_count

def main():
    """主函数"""
    print('=' * 50)
    print('开始初始化测试数据...')
    print('=' * 50)
    
    try:
        print('\n[1/4] 创建题目分类...')
        create_question_categories()
        
        print('\n[2/4] 创建套卷...')
        create_question_sets()
        
        print('\n[3/4] 创建题目...')
        create_questions()
        
        print('\n[4/4] 创建院校数据...')
        create_universities()
        
        print('\n[5/5] 创建文化内容...')
        create_culture_content()
        
        print('\n' + '=' * 50)
        print('[SUCCESS] 测试数据初始化完成！')
        print('=' * 50)
        
        print('\n统计信息:')
        print(f'- 题目分类: {QuestionCategory.objects.count()} 个')
        print(f'- 套卷: {QuestionSet.objects.count()} 个')
        print(f'- 题目: {Question.objects.count()} 道')
        print(f'- 院校: {University.objects.count()} 所')
        print(f'- 文化内容: {CultureContent.objects.count()} 篇')
        
    except Exception as e:
        print(f'\n[ERROR] 错误: {str(e)}')
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
