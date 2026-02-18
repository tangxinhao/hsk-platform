"""
初始化大学推荐数据 - 中英双语
"""
from django.core.management.base import BaseCommand
from university.models import University


class Command(BaseCommand):
    help = '初始化大学推荐数据（中英双语）'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化大学推荐数据...')
        
        # 清华、北大、复旦等顶级大学数据
        universities_data = [
            {
                'name': '北京大学',
                'english_name': 'Peking University',
                'region': '北京',
                'city': '北京市',
                'ranking': 1,
                'ranking_national': 1,
                'ranking_world': 12,
                'description': '北京大学创办于1898年，初名京师大学堂，是中国第一所国立综合性大学，也是当时中国最高教育行政机关。北京大学是中国近代以来唯一以国家最高学府身份创立的学校，最初也是国家最高教育行政机关，行使教育部职能。',
                'description_en': 'Peking University was founded in 1898 as the Imperial University of Peking. It is the first national comprehensive university in China and was also the highest educational administrative organ at that time.',
                'history': '北京大学创办于1898年，初名京师大学堂，是中国第一所国立综合性大学。',
                'history_en': 'Peking University was founded in 1898 as the Imperial University of Peking, the first national comprehensive university in China.',
                'features': '综合性、研究型、世界一流',
                'features_en': 'Comprehensive, Research-oriented, World-class',
                'advantages': [
                    {'zh': '历史悠久，是中国第一所国立综合性大学', 'en': 'Long history, first national comprehensive university'},
                    {'zh': '学科齐全，涵盖文理工医等多个领域', 'en': 'Comprehensive disciplines covering arts, sciences, engineering, medicine'},
                    {'zh': '师资力量雄厚，拥有众多知名学者', 'en': 'Strong faculty with many renowned scholars'},
                    {'zh': '国际交流广泛，与世界顶尖大学合作', 'en': 'Extensive international exchange with top universities'}
                ],
                'campus_life': [
                    {'zh': '位于北京海淀区，交通便利', 'en': 'Located in Haidian District, Beijing, convenient transportation'},
                    {'zh': '校园环境优美，设施齐全', 'en': 'Beautiful campus with complete facilities'},
                    {'zh': '丰富的社团活动和学术讲座', 'en': 'Rich club activities and academic lectures'},
                    {'zh': '多元文化氛围，国际学生众多', 'en': 'Multicultural atmosphere with many international students'}
                ],
                'min_hsk_level': 5,
                'language_requirements': 'HSK 5级及以上，部分专业要求6级',
                'tuition_fee': 26000,
                'scholarship': '中国政府奖学金、北京大学国际学生奖学金',
                'website': 'https://www.pku.edu.cn',
                'majors': ['中国语言文学', '历史学', '哲学', '经济学', '法学', '数学', '物理学', '化学', '生物学', '计算机科学'],
                'popular_majors': ['中国语言文学', '经济学', '法学', '计算机科学'],
                'international_students': 8000,
                'total_students': 45000,
                'tags': ['985工程', '211工程', '双一流', 'C9联盟']
            },
            {
                'name': '清华大学',
                'english_name': 'Tsinghua University',
                'region': '北京',
                'city': '北京市',
                'ranking': 2,
                'ranking_national': 2,
                'ranking_world': 17,
                'description': '清华大学的前身清华学堂始建于1911年，1912年更名为清华学校。1928年更名为国立清华大学。清华大学是中国乃至亚洲最著名的高等学府之一，在长达百年的办学历史中，2位共和国主席、7位中央政治局常委、14名两弹一星获得者。',
                'description_en': 'Tsinghua University originated from Tsinghua School founded in 1911. Renamed Tsinghua University in 1928. It is one of the most prestigious universities in China and Asia, with a century-long history of producing numerous leaders and scientists.',
                'history': '清华大学的前身清华学堂始建于1911年，1912年更名为清华学校，1928年更名为国立清华大学。',
                'history_en': 'Tsinghua University originated from Tsinghua School founded in 1911, renamed Tsinghua University in 1928.',
                'features': '理工见长，综合发展，世界一流',
                'features_en': 'Strong in engineering and science, comprehensive development, world-class',
                'advantages': [
                    {'zh': '工科实力雄厚，多个学科全国领先', 'en': 'Strong engineering programs, leading in multiple disciplines'},
                    {'zh': '科研成果丰硕，创新能力突出', 'en': 'Rich research achievements, outstanding innovation capability'},
                    {'zh': '就业率高，毕业生深受企业欢迎', 'en': 'High employment rate, graduates highly welcomed by companies'},
                    {'zh': '国际化程度高，国际合作广泛', 'en': 'High internationalization, extensive international cooperation'}
                ],
                'campus_life': [
                    {'zh': '位于北京海淀区，毗邻北京大学', 'en': 'Located in Haidian District, adjacent to Peking University'},
                    {'zh': '校园风景优美，被誉为最美大学之一', 'en': 'Beautiful campus, known as one of the most beautiful universities'},
                    {'zh': '体育氛围浓厚，体育设施完善', 'en': 'Strong sports atmosphere, complete sports facilities'},
                    {'zh': '学术氛围严谨，创新创业氛围活跃', 'en': 'Rigorous academic atmosphere, active innovation and entrepreneurship'}
                ],
                'min_hsk_level': 5,
                'language_requirements': 'HSK 5级及以上，理工科专业要求较低',
                'tuition_fee': 26000,
                'scholarship': '中国政府奖学金、清华大学国际学生奖学金',
                'website': 'https://www.tsinghua.edu.cn',
                'majors': ['计算机科学', '电子工程', '自动化', '建筑学', '土木工程', '机械工程', '经济管理', '物理学', '数学', '化学'],
                'popular_majors': ['计算机科学', '电子工程', '自动化', '经济管理'],
                'international_students': 7000,
                'total_students': 48000,
                'tags': ['985工程', '211工程', '双一流', 'C9联盟']
            },
            {
                'name': '复旦大学',
                'english_name': 'Fudan University',
                'region': '上海',
                'city': '上海市',
                'ranking': 3,
                'ranking_national': 3,
                'ranking_world': 34,
                'description': '复旦大学创建于1905年，原名复旦公学，1917年定名为复旦大学，是中国人自主创办的第一所高等院校。学校已经成为一所包括人文科学、自然科学、技术科学以及管理科学在内的多科性研究型综合大学。',
                'description_en': 'Fudan University was founded in 1905, originally named Fudan Public School. Renamed Fudan University in 1917. It is the first higher education institution independently established by Chinese people, now a comprehensive research university.',
                'history': '复旦大学创建于1905年，原名复旦公学，1917年定名为复旦大学，是中国人自主创办的第一所高等院校。',
                'history_en': 'Founded in 1905 as Fudan Public School, renamed Fudan University in 1917, the first higher education institution independently established by Chinese.',
                'features': '文理并重，多学科协调发展',
                'features_en': 'Equal emphasis on liberal arts and sciences, coordinated multi-disciplinary development',
                'advantages': [
                    {'zh': '文理医工学科齐全，实力均衡', 'en': 'Complete disciplines in arts, sciences, medicine, engineering with balanced strength'},
                    {'zh': '位于上海，经济发达，机会众多', 'en': 'Located in Shanghai, economically developed with numerous opportunities'},
                    {'zh': '国际化水平高，国际交流频繁', 'en': 'High level of internationalization, frequent international exchanges'},
                    {'zh': '人文传统深厚，校园文化丰富', 'en': 'Rich humanistic tradition and campus culture'}
                ],
                'campus_life': [
                    {'zh': '位于上海市区，交通便利，生活丰富', 'en': 'Located in downtown Shanghai, convenient transportation, rich life'},
                    {'zh': '校园环境优美，历史建筑众多', 'en': 'Beautiful campus with many historical buildings'},
                    {'zh': '社团活动丰富，学生组织活跃', 'en': 'Rich club activities, active student organizations'},
                    {'zh': '国际化氛围浓厚，留学生众多', 'en': 'Strong international atmosphere, many international students'}
                ],
                'min_hsk_level': 5,
                'language_requirements': 'HSK 5级及以上，部分专业要求6级',
                'tuition_fee': 23000,
                'scholarship': '中国政府奖学金、上海市政府奖学金、复旦大学国际学生奖学金',
                'website': 'https://www.fudan.edu.cn',
                'majors': ['中国语言文学', '新闻传播学', '经济学', '国际关系', '数学', '物理学', '化学', '生物学', '医学', '管理学'],
                'popular_majors': ['新闻传播学', '经济学', '国际关系', '医学'],
                'international_students': 6000,
                'total_students': 35000,
                'tags': ['985工程', '211工程', '双一流']
            }
        ]
        
        created_count = 0
        updated_count = 0
        
        for uni_data in universities_data:
            uni, created = University.objects.update_or_create(
                name=uni_data['name'],
                defaults=uni_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'[OK] 创建大学：{uni.name}'))
            else:
                updated_count += 1
                self.stdout.write(f'更新大学：{uni.name}')
        
        self.stdout.write(self.style.SUCCESS(f'\n[SUCCESS] 数据初始化完成！'))
        self.stdout.write(f'创建：{created_count}所大学')
        self.stdout.write(f'更新：{updated_count}所大学')
        self.stdout.write(f'总计：{University.objects.count()}所大学')
