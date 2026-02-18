"""
添加测试数据脚本
"""
import os
import sys
import django
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from user.models import User
from question.models import Question, QuestionSet, QuestionCategory
from university.models import University
from culture.models import Content

def create_users():
    """创建测试用户"""
    print('\n=== 创建用户 ===')
    
    # 创建管理员
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123456'
        )
        print('[OK] 创建管理员: admin / admin123456')
    else:
        print('[SKIP] 管理员已存在: admin')
    
    # 创建测试用户
    if not User.objects.filter(username='test').exists():
        user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='test123456'
        )
        print('[OK] 创建测试用户: test / test123456')
    else:
        print('[SKIP] 测试用户已存在: test')

def create_categories():
    """创建题目分类"""
    print('\n=== 创建题目分类 ===')
    
    categories = [
        ('vocabulary', '词汇'),
        ('reading', '阅读'),
        ('listening', '听力'),
        ('writing', '写作'),
        ('grammar', '语法'),
        ('comprehensive', '综合'),
    ]
    
    created = 0
    for code, name in categories:
        if not QuestionCategory.objects.filter(name=code).exists():
            QuestionCategory.objects.create(name=code, description=f'{name}题目')
            created += 1
            print(f'[OK] 创建分类: {name}')
    
    if created == 0:
        print('[SKIP] 所有分类已存在')
    
    print(f'数据库中共有 {QuestionCategory.objects.count()} 个分类')

def get_category(category_name):
    """根据中文名称获取分类"""
    category_map = {
        '词汇': 'vocabulary',
        '阅读': 'reading',
        '听力': 'listening',
        '写作': 'writing',
        '语法': 'grammar',
        '语音': 'vocabulary',  # 语音归入词汇类
        '综合': 'comprehensive',
    }
    
    code = category_map.get(category_name, 'vocabulary')
    category, _ = QuestionCategory.objects.get_or_create(
        name=code,
        defaults={'description': f'{category_name}题目'}
    )
    return category

def create_questions():
    """创建测试题目"""
    print('\n=== 创建题目 ===')
    
    questions_data = [
        # HSK 1 题目
        {
            'type': '单选题',
            'content': '"你好"的意思是？',
            'options': json.dumps(['Hello', 'Goodbye', 'Thanks', 'Sorry']),
            'answer': 'Hello',
            'level': 1,
            'difficulty': 1,
            'category': '词汇'
        },
        {
            'type': '单选题',
            'content': '"谢谢"的意思是？',
            'options': json.dumps(['Thank you', 'Sorry', 'Hello', 'Goodbye']),
            'answer': 'Thank you',
            'level': 1,
            'difficulty': 1,
            'category': '词汇'
        },
        {
            'type': '判断题',
            'content': '"再见"means "Goodbye"',
            'options': json.dumps(['正确', '错误']),
            'answer': '正确',
            'level': 1,
            'difficulty': 1,
            'category': '词汇'
        },
        {
            'type': '单选题',
            'content': '选择正确的拼音：我',
            'options': json.dumps(['wǒ', 'nǐ', 'tā', 'wǒmen']),
            'answer': 'wǒ',
            'level': 1,
            'difficulty': 2,
            'category': '语音'
        },
        {
            'type': '填空题',
            'content': '你___？(你好吗)',
            'options': json.dumps([]),
            'answer': '好吗',
            'level': 1,
            'difficulty': 2,
            'category': '语法'
        },
        
        # HSK 2 题目
        {
            'type': '单选题',
            'content': '"学习"的意思是？',
            'options': json.dumps(['study', 'work', 'play', 'eat']),
            'answer': 'study',
            'level': 2,
            'difficulty': 2,
            'category': '词汇'
        },
        {
            'type': '单选题',
            'content': '选择正确的量词：一___书',
            'options': json.dumps(['本', '个', '张', '条']),
            'answer': '本',
            'level': 2,
            'difficulty': 3,
            'category': '语法'
        },
        {
            'type': '多选题',
            'content': '下列哪些是家庭成员的称呼？',
            'options': json.dumps(['爸爸', '妈妈', '桌子', '椅子']),
            'answer': '爸爸,妈妈',
            'level': 2,
            'difficulty': 2,
            'category': '词汇'
        },
        
        # HSK 3 题目
        {
            'type': '单选题',
            'content': '"努力"的意思最接近？',
            'options': json.dumps(['hard-working', 'lazy', 'happy', 'sad']),
            'answer': 'hard-working',
            'level': 3,
            'difficulty': 3,
            'category': '词汇'
        },
        {
            'type': '单选题',
            'content': '选择正确的句子：',
            'options': json.dumps(['他比我高', '他比高我', '比我他高', '高比他我']),
            'answer': '他比我高',
            'level': 3,
            'difficulty': 3,
            'category': '语法'
        },
        
        # HSK 4 题目
        {
            'type': '单选题',
            'content': '"尽管...但是..."表示什么关系？',
            'options': json.dumps(['转折', '因果', '并列', '递进']),
            'answer': '转折',
            'level': 4,
            'difficulty': 4,
            'category': '语法'
        },
        {
            'type': '单选题',
            'content': '选择合适的词语填空：他___很累，___坚持工作。',
            'options': json.dumps(['虽然...但是', '因为...所以', '不但...而且', '如果...就']),
            'answer': '虽然...但是',
            'level': 4,
            'difficulty': 4,
            'category': '语法'
        },
        
        # HSK 5 题目
        {
            'type': '单选题',
            'content': '"望其项背"的意思是？',
            'options': json.dumps(['能够赶得上', '赶不上', '超越', '并驾齐驱']),
            'answer': '能够赶得上',
            'level': 5,
            'difficulty': 5,
            'category': '词汇'
        },
        {
            'type': '单选题',
            'content': '下列哪个不是书面语？',
            'options': json.dumps(['鉴于', '诸位', '咱们', '兹']),
            'answer': '咱们',
            'level': 5,
            'difficulty': 5,
            'category': '词汇'
        },
        
        # HSK 6 题目
        {
            'type': '单选题',
            'content': '"差强人意"的正确理解是？',
            'options': json.dumps(['很不满意', '大致令人满意', '非常满意', '完全不行']),
            'answer': '大致令人满意',
            'level': 6,
            'difficulty': 5,
            'category': '词汇'
        },
    ]
    
    created = 0
    for data in questions_data:
        if not Question.objects.filter(content=data['content']).exists():
            # 将分类名称转换为QuestionCategory实例
            category_name = data.pop('category')
            data['category'] = get_category(category_name)
            
            Question.objects.create(**data)
            created += 1
            print(f'[OK] 创建题目: {data["content"][:20]}...')
    
    print(f'\n总计创建 {created} 道新题目')
    print(f'数据库中共有 {Question.objects.count()} 道题目')

def create_question_sets():
    """创建套卷"""
    print('\n=== 创建套卷 ===')
    
    sets_data = [
        {
            'title': 'HSK 1级模拟试卷（一）',
            'level': 1,
            'time_limit': 35,
            'description': 'HSK一级标准模拟试题'
        },
        {
            'title': 'HSK 2级模拟试卷（一）',
            'level': 2,
            'time_limit': 50,
            'description': 'HSK二级标准模拟试题'
        },
        {
            'title': 'HSK 3级模拟试卷（一）',
            'level': 3,
            'time_limit': 85,
            'description': 'HSK三级标准模拟试题'
        },
        {
            'title': 'HSK 4级模拟试卷（一）',
            'level': 4,
            'time_limit': 100,
            'description': 'HSK四级标准模拟试题'
        },
        {
            'title': 'HSK 5级模拟试卷（一）',
            'level': 5,
            'time_limit': 120,
            'description': 'HSK五级标准模拟试题'
        },
        {
            'title': 'HSK 6级模拟试卷（一）',
            'level': 6,
            'time_limit': 135,
            'description': 'HSK六级标准模拟试题'
        },
    ]
    
    created = 0
    for data in sets_data:
        if not QuestionSet.objects.filter(title=data['title']).exists():
            QuestionSet.objects.create(**data)
            created += 1
            print(f'[OK] 创建套卷: {data["title"]}')
    
    print(f'\n总计创建 {created} 个新套卷')
    print(f'数据库中共有 {QuestionSet.objects.count()} 个套卷')

def create_universities():
    """创建院校数据"""
    print('\n=== 创建院校 ===')
    
    universities_data = [
        {
            'name': '北京大学',
            'location': '北京市',
            'rank': 1,
            'hsk_requirement': 5,
            'website': 'https://www.pku.edu.cn',
            'description': '中国顶尖综合性大学'
        },
        {
            'name': '清华大学',
            'location': '北京市',
            'rank': 2,
            'hsk_requirement': 5,
            'website': 'https://www.tsinghua.edu.cn',
            'description': '中国顶尖理工类大学'
        },
        {
            'name': '复旦大学',
            'location': '上海市',
            'rank': 3,
            'hsk_requirement': 5,
            'website': 'https://www.fudan.edu.cn',
            'description': '中国著名综合性大学'
        },
        {
            'name': '浙江大学',
            'location': '浙江省杭州市',
            'rank': 4,
            'hsk_requirement': 5,
            'website': 'https://www.zju.edu.cn',
            'description': '中国著名综合性大学'
        },
        {
            'name': '上海交通大学',
            'location': '上海市',
            'rank': 5,
            'hsk_requirement': 5,
            'website': 'https://www.sjtu.edu.cn',
            'description': '中国著名理工类大学'
        },
    ]
    
    created = 0
    for data in universities_data:
        if not University.objects.filter(name=data['name']).exists():
            University.objects.create(**data)
            created += 1
            print(f'[OK] 创建院校: {data["name"]}')
    
    print(f'\n总计创建 {created} 所新院校')
    print(f'数据库中共有 {University.objects.count()} 所院校')

def create_culture_content():
    """创建文化内容"""
    print('\n=== 创建文化内容 ===')
    
    culture_data = [
        {
            'title': '春节',
            'content': '春节是中国最重要的传统节日，通常在农历正月初一庆祝。',
            'category': '节日',
        },
        {
            'title': '中秋节',
            'content': '中秋节在农历八月十五，是中国重要的传统节日之一。',
            'category': '节日',
        },
        {
            'title': '端午节',
            'content': '端午节在农历五月初五，纪念爱国诗人屈原。',
            'category': '节日',
        },
    ]
    
    created = 0
    for data in culture_data:
        if not Content.objects.filter(title=data['title']).exists():
            Content.objects.create(**data)
            created += 1
            print(f'[OK] 创建文化内容: {data["title"]}')
    
    print(f'\n总计创建 {created} 条新文化内容')
    print(f'数据库中共有 {Content.objects.count()} 条文化内容')

def main():
    """主函数"""
    print('='*50)
    print('开始创建测试数据...')
    print('='*50)
    
    try:
        create_users()
        create_categories()
        create_questions()
        create_question_sets()
        create_universities()
        create_culture_content()
        
        print('\n'+'='*50)
        print('[OK] 所有测试数据创建完成!')
        print('='*50)
        
        print('\n登录账号:')
        print('  管理员: admin / admin123456')
        print('  测试用户: test / test123456')
        
        print('\n数据统计:')
        print(f'  用户: {User.objects.count()} 个')
        print(f'  题目: {Question.objects.count()} 道')
        print(f'  套卷: {QuestionSet.objects.count()} 个')
        print(f'  院校: {University.objects.count()} 所')
        print(f'  文化内容: {Content.objects.count()} 条')
        
    except Exception as e:
        print(f'\n[ERROR] 创建测试数据失败: {str(e)}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
