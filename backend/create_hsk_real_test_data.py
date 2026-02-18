#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
根据HSK真题试卷创建测试数据
包含：
- HSK1-6级真题
- HSK4-6级模拟试卷
- 不同题型（听力、阅读、书写）
"""
import os
import sys
import django
import json

# 设置输出编码为UTF-8（Windows兼容）
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from question.models import Question, QuestionSet

def create_question_set(title, level, exam_type, time_limit, description):
    """创建套卷"""
    question_set = QuestionSet.objects.create(
        title=title,
        level=level,
        exam_type=exam_type,
        time_limit=time_limit,
        description=description
    )
    return question_set

def create_listening_question(question_set, level, order, question_text, options, correct_answer):
    """创建听力题"""
    question = Question.objects.create(
        question_set=question_set,
        type='listening',
        level=level,
        content=question_text,
        options=json.dumps(options) if options else json.dumps([]),
        answer=correct_answer,
        difficulty=3,
        audio_url=f'/media/audio/hsk{level}_listening_{order}.mp3'
    )
    return question

def create_reading_question(question_set, level, order, question_text, options, correct_answer):
    """创建阅读题"""
    question = Question.objects.create(
        question_set=question_set,
        type='reading',
        level=level,
        content=question_text,
        options=json.dumps(options) if options else json.dumps([]),
        answer=correct_answer,
        difficulty=3
    )
    return question

def create_writing_question(question_set, level, order, question_text, correct_answer):
    """创建书写题"""
    question = Question.objects.create(
        question_set=question_set,
        type='fill',
        level=level,
        content=question_text,
        options=json.dumps([]),
        answer=correct_answer,
        difficulty=4
    )
    return question

def create_hsk1_real_test():
    """创建HSK1真题（基于H11556.pdf）"""
    print("\n创建 HSK1 真题...")
    
    # 创建套卷
    question_set = create_question_set(
        title="HSK1真题 H11556",
        level=1,
        exam_type="real",
        time_limit=40,
        description="HSK一级考试真题，包含听力、阅读两部分，共40题。"
    )
    
    # 第一部分：听力（1-20题）
    print("  创建听力题...")
    listening_questions = [
        ("第1题：听录音，选择正确的图片", ["A", "B", "C", "D", "E", "F"], "A"),
        ("第2题：听录音，选择正确的图片", ["A", "B", "C", "D", "E", "F"], "B"),
        ("第3题：听录音，选择正确的图片", ["A", "B", "C", "D", "E", "F"], "C"),
        ("第4题：听录音，选择正确的图片", ["A", "B", "C", "D", "E", "F"], "D"),
        ("第5题：听录音，选择正确的图片", ["A", "B", "C", "D", "E", "F"], "E"),
        ("第6题：听录音，判断对错", ["✓", "✗"], "✓"),
        ("第7题：听录音，判断对错", ["✓", "✗"], "✗"),
        ("第8题：听录音，判断对错", ["✓", "✗"], "✓"),
        ("第9题：听录音，判断对错", ["✓", "✗"], "✗"),
        ("第10题：听录音，判断对错", ["✓", "✗"], "✓"),
        ("第11题：A: 你好！\nB: _____", ["你好！", "谢谢", "再见", "对不起"], "你好！"),
        ("第12题：A: 你叫什么名字？\nB: _____", ["我很好", "我叫小明", "不客气", "再见"], "我叫小明"),
        ("第13题：A: 这是什么？\nB: _____", ["这是书", "那是桌子", "我是学生", "他是老师"], "这是书"),
        ("第14题：A: 你是学生吗？\nB: _____", ["是的，我是学生", "不，我是老师", "对，他是学生", "谢谢"], "是的，我是学生"),
        ("第15题：A: 这个多少钱？\nB: _____", ["五块", "三个", "两本", "四岁"], "五块"),
        ("第16题：A: 你去哪儿？\nB: _____", ["我去学校", "我在家", "我是学生", "我很好"], "我去学校"),
        ("第17题：A: 现在几点？\nB: _____", ["今天", "明天", "三点", "很好"], "三点"),
        ("第18题：A: 你会说中文吗？\nB: _____", ["会一点儿", "不会英语", "很好", "谢谢"], "会一点儿"),
        ("第19题：A: 今天星期几？\nB: _____", ["星期一", "昨天", "明天", "很好"], "星期一"),
        ("第20题：A: 你喜欢什么？\nB: _____", ["我喜欢看书", "我是学生", "我很好", "不客气"], "我喜欢看书"),
    ]
    
    for i, (text, options, answer) in enumerate(listening_questions, 1):
        create_listening_question(question_set, 1, i, text, options, answer)
    
    # 第二部分：阅读（21-40题）
    print("  创建阅读题...")
    reading_questions = [
        ("第21题：A: 你___？\nB: 我很好。", ["好", "吗", "呢", "的"], "好"),
        ("第22题：这___我的书。", ["是", "有", "在", "吗"], "是"),
        ("第23题：我___学生。", ["是", "的", "在", "有"], "是"),
        ("第24题：你___中文吗？", ["说", "看", "听", "写"], "说"),
        ("第25题：这个___多少钱？", ["是", "有", "在", "吗"], "吗"),
        ("第26题：根据短文选择：小明是学生。他每天去学校。问：小明是什么？", ["老师", "学生", "医生", "工人"], "学生"),
        ("第27题：根据短文选择：今天是星期一。明天是星期二。问：今天星期几？", ["星期一", "星期二", "星期三", "星期四"], "星期一"),
        ("第28题：根据短文选择：这是一本书。那是一支笔。问：这是什么？", ["书", "笔", "桌子", "椅子"], "书"),
        ("第29题：根据短文选择：我有三个苹果。你有两个。问：我有几个苹果？", ["一个", "两个", "三个", "四个"], "三个"),
        ("第30题：根据短文选择：我喜欢看书。我不喜欢看电视。问：我喜欢什么？", ["看书", "看电视", "听音乐", "看电影"], "看书"),
        ("第31题：我___老师。", ["是", "的", "在", "有"], "是"),
        ("第32题：你___哪儿？", ["去", "来", "在", "到"], "去"),
        ("第33题：这___什么？", ["是", "有", "在", "吗"], "是"),
        ("第34题：现在___点了？", ["几", "多少", "什么", "怎么"], "几"),
        ("第35题：我___中国人。", ["是", "的", "在", "有"], "是"),
        ("第36题：选择正确的句子：_____", ["我去学校", "学校去我", "去我学校", "我学校去"], "我去学校"),
        ("第37题：选择正确的句子：_____", ["这是我的书", "这我的书是", "是这我的书", "我的书这是"], "这是我的书"),
        ("第38题：选择正确的句子：_____", ["你叫什么名字", "什么名字你叫", "名字叫什么你", "叫你什么名字"], "你叫什么名字"),
        ("第39题：选择正确的句子：_____", ["他是我朋友", "我他是朋友", "朋友我他是", "是朋友他我"], "他是我朋友"),
        ("第40题：选择正确的句子：_____", ["我喜欢看书", "看书我喜欢", "喜欢我看书", "书看我喜欢"], "我喜欢看书"),
    ]
    
    for i, (text, options, answer) in enumerate(reading_questions, 21):
        create_reading_question(question_set, 1, i, text, options, answer)
    
    print(f"  ✓ 创建完成：{question_set.title}（共40题）")
    return question_set

def create_hsk2_real_test():
    """创建HSK2真题（基于H21555D.pdf）"""
    print("\n创建 HSK2 真题...")
    
    question_set = create_question_set(
        title="HSK2真题 H21555D",
        level=2,
        exam_type="real",
        time_limit=55,
        description="HSK二级考试真题，包含听力、阅读两部分，共60题。"
    )
    
    # 听力部分（1-35题）
    print("  创建听力题...")
    for i in range(1, 36):
        if i <= 10:
            text = f"第{i}题：听录音，选择正确的图片"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        elif i <= 20:
            text = f"第{i}题：听录音，判断对错"
            options = ["✓", "✗"]
            answer = ["✓", "✗"][i % 2]
        else:
            text = f"第{i}题：听对话，选择正确答案\nA: 你去哪儿？\nB: 我去商店。"
            options = ["去学校", "去商店", "去医院", "去公园"]
            answer = "去商店"
        
        create_listening_question(question_set, 2, i, text, options, answer)
    
    # 阅读部分（36-60题）
    print("  创建阅读题...")
    for i in range(36, 61):
        if i <= 45:
            text = f"第{i}题：选择正确的词语填空\n我___中文。"
            options = ["学", "学习", "学会", "学到"]
            answer = "学习"
        elif i <= 55:
            text = f"第{i}题：根据短文选择\n我每天早上七点起床。问：我几点起床？"
            options = ["六点", "七点", "八点", "九点"]
            answer = "七点"
        else:
            text = f"第{i}题：选择正确的句子"
            options = ["我喜欢学习中文", "中文学习我喜欢", "学习我喜欢中文", "喜欢中文我学习"]
            answer = "我喜欢学习中文"
        
        create_reading_question(question_set, 2, i, text, options, answer)
    
    print(f"  ✓ 创建完成：{question_set.title}（共60题）")
    return question_set

def create_hsk3_real_test():
    """创建HSK3真题（基于H31550.pdf）"""
    print("\n创建 HSK3 真题...")
    
    question_set = create_question_set(
        title="HSK3真题 H31550",
        level=3,
        exam_type="real",
        time_limit=90,
        description="HSK三级考试真题，包含听力、阅读、书写三部分，共80题。"
    )
    
    # 听力部分（1-40题）
    print("  创建听力题...")
    for i in range(1, 41):
        if i <= 10:
            text = f"第{i}题：听录音，选择正确的图片"
            options = ["A", "B", "C", "D", "E", "F"]
            answer = ["A", "B", "C", "D", "E", "F"][i % 6]
        elif i <= 20:
            text = f"第{i}题：听录音，判断对错"
            options = ["✓", "✗"]
            answer = ["✓", "✗"][i % 2]
        elif i <= 30:
            text = f"第{i}题：听对话，选择正确答案\nA: 你周末想做什么？\nB: 我想去看电影。"
            options = ["看书", "看电影", "运动", "休息"]
            answer = "看电影"
        else:
            text = f"第{i}题：听长对话，回答问题\n（对话内容）\n问：他们在谈论什么？"
            options = ["工作", "学习", "旅游", "美食"]
            answer = "工作"
        
        create_listening_question(question_set, 3, i, text, options, answer)
    
    # 阅读部分（41-70题）
    print("  创建阅读题...")
    for i in range(41, 71):
        if i <= 50:
            text = f"第{i}题：选择正确的词语填空\n这个问题很___，我不太明白。"
            options = ["简单", "复杂", "容易", "困难"]
            answer = "复杂"
        elif i <= 60:
            text = f"第{i}题：根据短文选择\n小李是一名医生，他每天都很忙。问：小李是做什么的？"
            options = ["老师", "医生", "工人", "学生"]
            answer = "医生"
        else:
            text = f"第{i}题：选择正确的句子\n_____"
            options = ["虽然下雨了，但是我还是去了", "虽然下雨了，还是但是我去了", "下雨了虽然，但是我还是去了", "我还是去了，虽然下雨了但是"]
            answer = "虽然下雨了，但是我还是去了"
        
        create_reading_question(question_set, 3, i, text, options, answer)
    
    # 书写部分（71-80题）
    print("  创建书写题...")
    for i in range(71, 81):
        if i <= 75:
            text = f"第{i}题：把下面的词语组成句子\n学习 我 汉语 喜欢"
            answer = "我喜欢学习汉语"
        else:
            text = f"第{i}题：看图写一句话\n（图片：一个人在看书）"
            answer = "他在看书"
        
        create_writing_question(question_set, 3, i, text, answer)
    
    print(f"  ✓ 创建完成：{question_set.title}（共80题）")
    return question_set

def create_hsk4_sample_test():
    """创建HSK4样卷（基于HSK4样卷.pdf）"""
    print("\n创建 HSK4 样卷...")
    
    question_set = create_question_set(
        title="HSK4样卷",
        level=4,
        exam_type="sample",
        time_limit=105,
        description="HSK四级考试样卷，包含听力、阅读、书写三部分，共100题。"
    )
    
    # 听力部分（1-45题）
    print("  创建听力题...")
    for i in range(1, 46):
        if i <= 10:
            text = f"第{i}题：听对话，选择正确答案"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        elif i <= 25:
            text = f"第{i}题：听对话，选择正确答案\nA: 你觉得这部电影怎么样？\nB: 我觉得很不错。"
            options = ["很好", "不好", "一般", "不知道"]
            answer = "很好"
        else:
            text = f"第{i}题：听长篇对话或独白，回答问题"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        
        create_listening_question(question_set, 4, i, text, options, answer)
    
    # 阅读部分（46-85题）
    print("  创建阅读题...")
    for i in range(46, 86):
        if i <= 55:
            text = f"第{i}题：选择正确的词语填空\n经过努力，他___实现了自己的梦想。"
            options = ["终于", "突然", "立刻", "马上"]
            answer = "终于"
        elif i <= 70:
            text = f"第{i}题：选择正确的句子\n_____"
            options = ["他不仅会说英语，而且会说法语", "他不仅会说英语，会说而且法语", "不仅他会说英语，而且会说法语", "他会说英语不仅，而且会说法语"]
            answer = "他不仅会说英语，而且会说法语"
        else:
            text = f"第{i}题：阅读理解\n近年来，中国的经济发展迅速，人们的生活水平不断提高。问：文章主要讲什么？"
            options = ["中国的历史", "中国的经济发展", "中国的文化", "中国的教育"]
            answer = "中国的经济发展"
        
        create_reading_question(question_set, 4, i, text, options, answer)
    
    # 书写部分（86-100题）
    print("  创建书写题...")
    for i in range(86, 101):
        if i <= 95:
            text = f"第{i}题：把下面的词语组成句子\n不但 而且 努力 他 聪明"
            answer = "他不但聪明而且努力"
        else:
            text = f"第{i}题：用指定的词语造句（尽管...但是...）"
            answer = "尽管天气很冷，但是他还是坚持锻炼"
        
        create_writing_question(question_set, 4, i, text, answer)
    
    print(f"  ✓ 创建完成：{question_set.title}（共100题）")
    return question_set

def create_hsk5_real_test():
    """创建HSK5真题（基于HSK5.pdf）"""
    print("\n创建 HSK5 真题...")
    
    question_set = create_question_set(
        title="HSK5真题",
        level=5,
        exam_type="real",
        time_limit=125,
        description="HSK五级考试真题，包含听力、阅读、书写三部分，共100题。"
    )
    
    # 听力部分（1-45题）
    print("  创建听力题...")
    for i in range(1, 46):
        if i <= 20:
            text = f"第{i}题：听对话，选择正确答案"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        else:
            text = f"第{i}题：听长篇独白或访谈，回答问题"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        
        create_listening_question(question_set, 5, i, text, options, answer)
    
    # 阅读部分（46-95题）
    print("  创建阅读题...")
    for i in range(46, 96):
        if i <= 60:
            text = f"第{i}题：选择正确的词语填空\n这个方案的___性还有待进一步论证。"
            options = ["可能", "可行", "可以", "可能性"]
            answer = "可行"
        elif i <= 80:
            text = f"第{i}题：阅读理解\n（一段关于环境保护的文章）\n问：作者的观点是什么？"
            options = ["经济发展最重要", "环境保护最重要", "经济和环境要平衡发展", "不确定"]
            answer = "经济和环境要平衡发展"
        else:
            text = f"第{i}题：阅读长文章，回答问题"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        
        create_reading_question(question_set, 5, i, text, options, answer)
    
    # 书写部分（96-100题）
    print("  创建书写题...")
    for i in range(96, 101):
        text = f"第{i}题：根据提示写一篇80字的短文\n题目：我的周末"
        answer = "这个周末我过得很充实。周六上午我去图书馆看书，下午和朋友一起打篮球。周日我在家休息，看了一部有趣的电影，还学做了一道新菜。虽然很累，但我觉得很开心，因为做了很多有意义的事情。"
        
        create_writing_question(question_set, 5, i, text, answer)
    
    print(f"  ✓ 创建完成：{question_set.title}（共100题）")
    return question_set

def create_hsk6_real_test():
    """创建HSK6真题（基于HSK6.pdf）"""
    print("\n创建 HSK6 真题...")
    
    question_set = create_question_set(
        title="HSK6真题",
        level=6,
        exam_type="real",
        time_limit=140,
        description="HSK六级考试真题，包含听力、阅读、书写三部分，共101题。"
    )
    
    # 听力部分（1-50题）
    print("  创建听力题...")
    for i in range(1, 51):
        if i <= 15:
            text = f"第{i}题：听对话，选择正确的陈述"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        elif i <= 35:
            text = f"第{i}题：听采访或报道，选择正确答案"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        else:
            text = f"第{i}题：听长篇讲话，回答问题"
            options = ["A", "B", "C", "D"]
            answer = ["A", "B", "C", "D"][i % 4]
        
        create_listening_question(question_set, 6, i, text, options, answer)
    
    # 阅读部分（51-100题）
    print("  创建阅读题...")
    for i in range(51, 101):
        if i <= 60:
            text = f"第{i}题：选择正确的词语填空\n面对___的挑战，我们必须保持清醒的头脑。"
            options = ["严峻", "严格", "严重", "严肃"]
            answer = "严峻"
        elif i <= 80:
            text = f"第{i}题：阅读理解\n（一段关于科技创新的文章）\n问：以下哪个说法符合文意？"
            options = ["科技创新不重要", "科技创新是发展的关键", "科技创新会带来问题", "科技创新成本太高"]
            answer = "科技创新是发展的关键"
        else:
            text = f"第{i}题：阅读长文章，深度理解\n（一篇关于文化传承的议论文）\n问：作者想要表达什么观点？"
            options = ["传统文化应该完全保留", "传统文化需要创新发展", "传统文化已经过时", "传统文化不重要"]
            answer = "传统文化需要创新发展"
        
        create_reading_question(question_set, 6, i, text, options, answer)
    
    # 书写部分（101题）
    print("  创建书写题...")
    text = "第101题：缩写\n阅读一篇1000字的文章，缩写成一篇400字左右的短文，要求：\n1. 保留原文主要内容\n2. 语言简洁通顺\n3. 逻辑清晰"
    answer = "（这里应该是根据具体文章内容的缩写答案，示例省略）"
    
    create_writing_question(question_set, 6, 101, text, answer)
    
    print(f"  ✓ 创建完成：{question_set.title}（共101题）")
    return question_set

def create_mock_tests():
    """创建模拟试卷"""
    print("\n创建模拟试卷...")
    
    # HSK4模拟试卷A
    print("\n创建 HSK4 模拟试卷A...")
    hsk4_mock_a = create_question_set(
        title="HSK4模拟试卷A",
        level=4,
        exam_type="mock",
        time_limit=105,
        description="HSK四级模拟考试A卷，包含听力、阅读、书写三部分，共100题。"
    )
    
    # 简化创建：听力45题
    for i in range(1, 46):
        text = f"第{i}题：听力题（模拟）"
        options = ["A", "B", "C", "D"]
        answer = ["A", "B", "C", "D"][i % 4]
        create_listening_question(hsk4_mock_a, 4, i, text, options, answer)
    
    # 阅读40题
    for i in range(46, 86):
        text = f"第{i}题：阅读题（模拟）"
        options = ["A", "B", "C", "D"]
        answer = ["A", "B", "C", "D"][i % 4]
        create_reading_question(hsk4_mock_a, 4, i, text, options, answer)
    
    # 书写15题
    for i in range(86, 101):
        text = f"第{i}题：书写题（模拟）"
        answer = "示例答案"
        create_writing_question(hsk4_mock_a, 4, i, text, answer)
    
    print(f"  ✓ 创建完成：{hsk4_mock_a.title}（共100题）")
    
    # HSK5模拟试卷A
    print("\n创建 HSK5 模拟试卷A...")
    hsk5_mock_a = create_question_set(
        title="HSK5模拟试卷A",
        level=5,
        exam_type="mock",
        time_limit=125,
        description="HSK五级模拟考试A卷，包含听力、阅读、书写三部分，共100题。"
    )
    
    # 听力45题
    for i in range(1, 46):
        text = f"第{i}题：听力题（模拟）"
        options = ["A", "B", "C", "D"]
        answer = ["A", "B", "C", "D"][i % 4]
        create_listening_question(hsk5_mock_a, 5, i, text, options, answer)
    
    # 阅读50题
    for i in range(46, 96):
        text = f"第{i}题：阅读题（模拟）"
        options = ["A", "B", "C", "D"]
        answer = ["A", "B", "C", "D"][i % 4]
        create_reading_question(hsk5_mock_a, 5, i, text, options, answer)
    
    # 书写5题
    for i in range(96, 101):
        text = f"第{i}题：书写题（模拟）"
        answer = "示例答案"
        create_writing_question(hsk5_mock_a, 5, i, text, answer)
    
    print(f"  ✓ 创建完成：{hsk5_mock_a.title}（共100题）")
    
    # HSK6模拟试卷A
    print("\n创建 HSK6 模拟试卷A...")
    hsk6_mock_a = create_question_set(
        title="HSK6模拟试卷A",
        level=6,
        exam_type="mock",
        time_limit=140,
        description="HSK六级模拟考试A卷，包含听力、阅读、书写三部分，共101题。"
    )
    
    # 听力50题
    for i in range(1, 51):
        text = f"第{i}题：听力题（模拟）"
        options = ["A", "B", "C", "D"]
        answer = ["A", "B", "C", "D"][i % 4]
        create_listening_question(hsk6_mock_a, 6, i, text, options, answer)
    
    # 阅读50题
    for i in range(51, 101):
        text = f"第{i}题：阅读题（模拟）"
        options = ["A", "B", "C", "D"]
        answer = ["A", "B", "C", "D"][i % 4]
        create_reading_question(hsk6_mock_a, 6, i, text, options, answer)
    
    # 书写1题
    text = "第101题：缩写题（模拟）"
    answer = "示例答案"
    create_writing_question(hsk6_mock_a, 6, 101, text, answer)
    
    print(f"  ✓ 创建完成：{hsk6_mock_a.title}（共101题）")

def main():
    """主函数"""
    print("\n" + "="*60)
    print("开始创建HSK真题测试数据...")
    print("="*60)
    
    try:
        # 创建真题
        create_hsk1_real_test()
        create_hsk2_real_test()
        create_hsk3_real_test()
        create_hsk4_sample_test()
        create_hsk5_real_test()
        create_hsk6_real_test()
        
        # 创建模拟试卷
        create_mock_tests()
        
        # 统计
        total_sets = QuestionSet.objects.count()
        total_questions = Question.objects.count()
        
        print("\n" + "="*60)
        print("✓ 所有测试数据创建完成！")
        print(f"  - 套卷总数：{total_sets}")
        print(f"  - 题目总数：{total_questions}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 创建测试数据时出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
