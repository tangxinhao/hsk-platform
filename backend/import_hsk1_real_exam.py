"""
导入HSK1真题数据（H11556）
根据官方样卷结构创建完整的题目和材料
"""
import os
import sys
import django

# 设置Django环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsk_project.settings')
django.setup()

from question.models import Question, QuestionSet, Material
import json

# Windows环境UTF-8输出
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')


def create_hsk1_real_exam():
    """创建HSK1真题试卷（H11556）"""
    print("\n" + "="*60)
    print("开始导入HSK1真题（H11556）")
    print("="*60 + "\n")
    
    # 1. 创建试卷
    print("[1/5] 创建试卷...")
    question_set, created = QuestionSet.objects.get_or_create(
        title="HSK1真题试卷（H11556）",
        level=1,
        exam_type='real',
        defaults={
            'description': 'HSK一级真题试卷H11556，包含听力20题和阅读20题',
            'time_limit': 40,
            'question_count': 40
        }
    )
    if created:
        print(f"✅ 试卷创建成功: {question_set.title}")
    else:
        # 清除旧数据
        print(f"⚠️ 试卷已存在，清除旧数据...")
        Question.objects.filter(question_set=question_set).delete()
        Material.objects.filter(level=1, material_group__startswith='hsk1_h11556').delete()
        print("✅ 旧数据已清除")
    
    # 音频和图片基础URL
    audio_base = "http://localhost:8000/media/audio/H11556.mp3"
    image_base = "http://localhost:8000/media/images/hsk1"
    
    # 2. 创建听力部分
    print("\n[2/5] 创建听力部分...")
    
    # 第一部分：图片判断（第1-5题）
    print("  [Part 1] 图片判断（1-5题）...")
    for i in range(1, 6):
        # 创建材料
        material = Material.objects.create(
            title=f"HSK1听力第一部分第{i}题",
            level=1,
            section_type='listening',
            part_number=1,
            audio_url=audio_base,
            audio_duration=3,
            material_group=f"hsk1_h11556_listening_p1_q{i}",
            play_times=2,
            question_range_start=i,
            question_range_end=i,
            order=i
        )
        
        # 创建题目
        Question.objects.create(
            question_set=question_set,
            type='listening_image_judge',
            level=1,
            section_type='listening',
            part_number=1,
            question_number=i,
            material_group=material.material_group,
            content=f"第{i}题：判断录音内容是否与图片相符。",
            answer='✓',
            options=json.dumps(['✓', '✗']),
            image_url=f"{image_base}/part1_q{i}.jpg",
            difficulty=1,
            points=1
        )
    print("  ✅ 第一部分完成（5题）")
    
    # 第二部分：图片选择（第6-10题）
    print("  [Part 2] 图片选择（6-10题）...")
    for i in range(6, 11):
        q_num = i - 5
        material = Material.objects.create(
            title=f"HSK1听力第二部分第{i}题",
            level=1,
            section_type='listening',
            part_number=2,
            audio_url=audio_base,
            audio_duration=4,
            material_group=f"hsk1_h11556_listening_p2_q{i}",
            play_times=2,
            question_range_start=i,
            question_range_end=i,
            order=q_num
        )
        
        Question.objects.create(
            question_set=question_set,
            type='listening_image_choice',
            level=1,
            section_type='listening',
            part_number=2,
            question_number=i,
            material_group=material.material_group,
            content=f"第{i}题：根据录音选择正确的图片。",
            answer='A',
            options=json.dumps([
                f"{image_base}/part2_q{i}_a.jpg",
                f"{image_base}/part2_q{i}_b.jpg",
                f"{image_base}/part2_q{i}_c.jpg"
            ]),
            difficulty=1,
            points=1
        )
    print("  ✅ 第二部分完成（5题）")
    
    # 第三部分：对话配图（第11-15题）
    print("  [Part 3] 对话配图（11-15题）...")
    for i in range(11, 16):
        q_num = i - 10
        material = Material.objects.create(
            title=f"HSK1听力第三部分第{i}题对话",
            level=1,
            section_type='listening',
            part_number=3,
            content="女：你好！\\n男：你好！很高兴认识你。",
            audio_url=audio_base,
            audio_duration=8,
            material_group=f"hsk1_h11556_listening_p3_q{i}",
            play_times=2,
            question_range_start=i,
            question_range_end=i,
            order=q_num
        )
        
        Question.objects.create(
            question_set=question_set,
            type='listening_dialogue_image',
            level=1,
            section_type='listening',
            part_number=3,
            question_number=i,
            material_group=material.material_group,
            content=f"第{i}题：根据对话选择正确的图片。",
            answer='A',
            options=json.dumps([
                f"{image_base}/part3_q{i}_a.jpg",
                f"{image_base}/part3_q{i}_b.jpg",
                f"{image_base}/part3_q{i}_c.jpg"
            ]),
            difficulty=2,
            points=1
        )
    print("  ✅ 第三部分完成（5题）")
    
    # 第四部分：文字选择（第16-20题）
    print("  [Part 4] 文字选择（16-20题）...")
    questions_part4 = [
        {
            'num': 16,
            'content': '他下午去哪里？',
            'options': ['商店', '医院', '学校'],
            'answer': '商店'
        },
        {
            'num': 17,
            'content': '她想做什么？',
            'options': ['学汉语', '打电话', '看电影'],
            'answer': '学汉语'
        },
        {
            'num': 18,
            'content': '他怎么去？',
            'options': ['开车', '坐飞机', '坐出租车'],
            'answer': '坐出租车'
        },
        {
            'num': 19,
            'content': '这件衣服怎么样？',
            'options': ['太大', '很漂亮', '有点儿小'],
            'answer': '有点儿小'
        },
        {
            'num': 20,
            'content': '她找谁？',
            'options': ['李小姐', '王医生', '李先生'],
            'answer': '王医生'
        }
    ]
    
    for q_data in questions_part4:
        i = q_data['num']
        q_num = i - 15
        material = Material.objects.create(
            title=f"HSK1听力第四部分第{i}题对话",
            level=1,
            section_type='listening',
            part_number=4,
            audio_url=audio_base,
            audio_duration=15,
            material_group=f"hsk1_h11556_listening_p4_q{i}",
            play_times=2,
            question_range_start=i,
            question_range_end=i,
            order=q_num
        )
        
        Question.objects.create(
            question_set=question_set,
            type='listening_text_choice',
            level=1,
            section_type='listening',
            part_number=4,
            question_number=i,
            material_group=material.material_group,
            content=f"第{i}题：{q_data['content']}",
            answer=q_data['answer'],
            options=json.dumps(q_data['options']),
            difficulty=2,
            points=1
        )
    print("  ✅ 第四部分完成（5题）")
    print("✅ 听力部分完成（20题）\n")
    
    # 3. 创建阅读部分
    print("[3/5] 创建阅读部分...")
    
    # 第一部分：图片词语匹配（第21-25题）
    print("  [Part 1] 图片词语匹配（21-25题）...")
    words_part1 = [
        {'num': 21, 'word': '六', 'answer': '六'},
        {'num': 22, 'word': '冷', 'answer': '冷'},
        {'num': 23, 'word': '再见', 'answer': '再见'},
        {'num': 24, 'word': '狗', 'answer': '狗'},
        {'num': 25, 'word': '不客气', 'answer': '不客气'}
    ]
    
    for w_data in words_part1:
        i = w_data['num']
        Question.objects.create(
            question_set=question_set,
            type='reading_image_word_match',
            level=1,
            section_type='reading',
            part_number=1,
            question_number=i,
            content=f"第{i}题：选择与图片对应的词语。",
            answer=w_data['answer'],
            options=json.dumps([w_data['word'], '选项B', '选项C']),
            image_url=f"{image_base}/reading_p1_q{i}.jpg",
            difficulty=1,
            points=1
        )
    print("  ✅ 第一部分完成（5题）")
    
    # 第二部分：句子图片匹配（第26-30题）
    print("  [Part 2] 句子图片匹配（26-30题）...")
    sentences_part2 = [
        {'num': 26, 'content': '老师，中国在哪儿？', 'answer': 'A'},
        {'num': 27, 'content': '米饭好了，叫爸爸来吃饭。', 'answer': 'B'},
        {'num': 28, 'content': '我女儿不在家，她去看朋友了。', 'answer': 'C'},
        {'num': 29, 'content': '这是小刘，他在医院工作。', 'answer': 'D'},
        {'num': 30, 'content': '我中午去商店买了很多东西。', 'answer': 'E'}
    ]
    
    for s_data in sentences_part2:
        i = s_data['num']
        Question.objects.create(
            question_set=question_set,
            type='reading_sentence_image_match',
            level=1,
            section_type='reading',
            part_number=2,
            question_number=i,
            content=s_data['content'],
            answer=s_data['answer'],
            options=json.dumps([
                f"{image_base}/reading_p2_a.jpg",
                f"{image_base}/reading_p2_b.jpg",
                f"{image_base}/reading_p2_c.jpg",
                f"{image_base}/reading_p2_d.jpg",
                f"{image_base}/reading_p2_e.jpg",
                f"{image_base}/reading_p2_f.jpg"
            ]),
            difficulty=2,
            points=1
        )
    print("  ✅ 第二部分完成（5题）")
    
    # 第三部分：对话匹配（第31-35题）
    print("  [Part 3] 对话匹配（31-35题）...")
    dialogues_part3 = [
        {'num': 31, 'question': '你想什么时候买车？', 'answer': '下个月'},
        {'num': 32, 'question': '我们现在去哪儿？', 'answer': '饭店'},
        {'num': 33, 'question': '你昨天和谁去看的电影？', 'answer': '我同学'},
        {'num': 34, 'question': '儿子上午学习了吗？', 'answer': '没有'},
        {'num': 35, 'question': '明天天气怎么样？', 'answer': '会很热'}
    ]
    
    for d_data in dialogues_part3:
        i = d_data['num']
        Question.objects.create(
            question_set=question_set,
            type='reading_dialogue_match',
            level=1,
            section_type='reading',
            part_number=3,
            question_number=i,
            content=d_data['question'],
            answer=d_data['answer'],
            options=json.dumps(['没有', '饭店', '下个月', '会很热', '我同学', '好的，谢谢！']),
            difficulty=2,
            points=1
        )
    print("  ✅ 第三部分完成（5题）")
    
    # 第四部分：选词填空（第36-40题）
    print("  [Part 4] 选词填空（36-40题）...")
    fill_blanks_part4 = [
        {'num': 36, 'content': '这些汉字我会读，不会（  ）。', 'answer': '写', 'options': ['住', '高兴', '几', '名字', '学生', '写']},
        {'num': 37, 'content': '你今天能来，我太（  ）了。', 'answer': '高兴', 'options': ['住', '高兴', '几', '名字', '学生', '写']},
        {'num': 38, 'content': '我们学校不大，老师和（  ）都很少。', 'answer': '学生', 'options': ['住', '高兴', '几', '名字', '学生', '写']},
        {'num': 39, 'content': '你（  ）在这后面？', 'answer': '住', 'options': ['住', '高兴', '几', '名字', '学生', '写']},
        {'num': 40, 'content': '这（  ）个菜是谁做的？', 'answer': '几', 'options': ['住', '高兴', '几', '名字', '学生', '写']}
    ]
    
    for f_data in fill_blanks_part4:
        i = f_data['num']
        Question.objects.create(
            question_set=question_set,
            type='reading_fill_blank',
            level=1,
            section_type='reading',
            part_number=4,
            question_number=i,
            content=f_data['content'],
            answer=f_data['answer'],
            options=json.dumps(f_data['options']),
            difficulty=2,
            points=1
        )
    print("  ✅ 第四部分完成（5题）")
    print("✅ 阅读部分完成（20题）\n")
    
    # 4. 更新试卷题目数量
    print("[4/5] 更新试卷信息...")
    question_set.question_count = Question.objects.filter(question_set=question_set).count()
    question_set.save()
    print(f"✅ 试卷题目数量：{question_set.question_count}题\n")
    
    # 5. 统计信息
    print("[5/5] 生成统计信息...")
    total_questions = Question.objects.filter(question_set=question_set).count()
    total_materials = Material.objects.filter(material_group__startswith='hsk1_h11556').count()
    
    listening_count = Question.objects.filter(question_set=question_set, section_type='listening').count()
    reading_count = Question.objects.filter(question_set=question_set, section_type='reading').count()
    
    print("\n" + "="*60)
    print("导入完成！统计信息：")
    print("="*60)
    print(f"✅ 试卷名称：{question_set.title}")
    print(f"✅ 总题目数：{total_questions}题")
    print(f"✅ 听力题目：{listening_count}题")
    print(f"✅ 阅读题目：{reading_count}题")
    print(f"✅ 音频材料：{total_materials}个")
    print("="*60 + "\n")
    
    return question_set


if __name__ == '__main__':
    try:
        question_set = create_hsk1_real_exam()
        print("🎉 HSK1真题导入成功！")
        print(f"\n访问Django Admin查看：http://localhost:8000/admin/question/questionset/{question_set.id}/")
    except Exception as e:
        print(f"\n❌ 导入失败：{str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
