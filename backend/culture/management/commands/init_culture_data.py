"""
初始化文化学习数据 - 中英双语
"""
from django.core.management.base import BaseCommand
from culture.models import Category, Content


class Command(BaseCommand):
    help = '初始化文化学习数据（中英双语）'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化文化学习数据...')
        
        # 创建分类
        category, created = Category.objects.get_or_create(
            name='饮食文化',
            defaults={
                'description': '了解中国各地特色美食和饮食文化',
                'level': '中级'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'[OK] 创建分类：{category.name}'))
        else:
            self.stdout.write(f'分类已存在：{category.name}')
        
        # 八大菜系数据
        cuisines_data = {
            '鲁菜': {
                'title': '中国八大菜系 - 鲁菜',
                'title_en': 'Chinese Eight Cuisines - Shandong Cuisine',
                'paragraphs': [
                    {
                        'zh': '鲁菜是中国传统四大菜系（也是八大菜系）中唯一的自发型菜系，是历史最悠久、技法最丰富的菜系，也是最难掌握的菜系。',
                        'en': 'Shandong Cuisine is the only spontaneous cuisine among the traditional Four Great Cuisines (and Eight Cuisines) of China. It has the longest history, the richest techniques, and is the most difficult to master.'
                    },
                    {
                        'zh': '鲁菜起源于山东省济南和胶东地区，讲究"食不厌精，脍不厌细"的孔子饮食思想。',
                        'en': 'Shandong Cuisine originated from Jinan and Jiaodong areas in Shandong Province, emphasizing Confucius\' dietary philosophy of "food can never be too refined, and minced meat can never be too finely cut".'
                    },
                    {
                        'zh': '鲁菜的特点包括：选料考究，刀法精细；注重调味，口味鲜咸纯正；烹调技法全面，尤以爆、炒、扒见长；善于制汤，精于用汤。',
                        'en': 'Characteristics of Shandong Cuisine include: careful selection of ingredients and precise knife skills; emphasis on seasoning with fresh and pure salty flavors; comprehensive cooking techniques, especially excelling in quick-frying, stir-frying, and braising; expertise in soup-making and soup usage.'
                    },
                    {
                        'zh': '代表名菜有：葱烧海参、九转大肠、糖醋鲤鱼、四喜丸子等。',
                        'en': 'Representative dishes include: Sea Cucumber with Scallions, Jiuzhuan Large Intestine, Sweet and Sour Carp, and Four-Joy Meatballs.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            },
            '川菜': {
                'title': '中国八大菜系 - 川菜',
                'title_en': 'Chinese Eight Cuisines - Sichuan Cuisine',
                'paragraphs': [
                    {
                        'zh': '川菜取材广泛，调味多变，菜式多样，口味清鲜醇浓并重，以善用麻辣调味著称。',
                        'en': 'Sichuan Cuisine uses a wide variety of ingredients, diverse seasonings, and varied dishes. It emphasizes both light-fresh and rich-intense flavors, and is famous for its skillful use of spicy and numbing seasonings.'
                    },
                    {
                        'zh': '川菜起源于四川省成都和重庆地区，体现了四川人民热情奔放的性格。',
                        'en': 'Sichuan Cuisine originated from Chengdu and Chongqing areas in Sichuan Province, reflecting the passionate and unrestrained character of Sichuan people.'
                    },
                    {
                        'zh': '"麻"与"辣"是川菜的灵魂，"麻"来自花椒，"辣"来自辣椒，二者缺一不可。',
                        'en': '"Numbing" and "Spicy" are the soul of Sichuan Cuisine. "Numbing" comes from Sichuan peppercorn, and "Spicy" comes from chili pepper - both are indispensable.'
                    },
                    {
                        'zh': '代表名菜有：麻婆豆腐、宫保鸡丁、水煮鱼、回锅肉等。',
                        'en': 'Representative dishes include: Mapo Tofu, Kung Pao Chicken, Boiled Fish in Hot Chili Oil, and Twice-Cooked Pork.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            },
            '粤菜': {
                'title': '中国八大菜系 - 粤菜',
                'title_en': 'Chinese Eight Cuisines - Cantonese Cuisine',
                'paragraphs': [
                    {
                        'zh': '粤菜是中国传统四大菜系之一，起源于岭南，由广州菜、潮州菜、东江菜三种地方风味组成。',
                        'en': 'Cantonese Cuisine is one of the Four Great Cuisines of China, originated in Lingnan, consisting of Guangzhou, Chaozhou, and Dongjiang local flavors.'
                    },
                    {
                        'zh': '粤菜注重质和味，口味比较清淡，力求清中求鲜、淡中求美。而且随季节时令的变化而变化，夏秋偏重清淡，冬春偏重浓郁。',
                        'en': 'Cantonese Cuisine emphasizes quality and taste, with relatively light flavors, seeking freshness in lightness and beauty in blandness. It changes with seasons - lighter in summer and autumn, richer in winter and spring.'
                    },
                    {
                        'zh': '代表名菜有：白切鸡、烧鹅、烤乳猪、红烧乳鸽、蜜汁叉烧、脆皮烧肉等。',
                        'en': 'Representative dishes include: White Cut Chicken, Roast Goose, Roast Suckling Pig, Braised Pigeon, Honey Glazed BBQ Pork, and Crispy Roast Pork.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            },
            '苏菜': {
                'title': '中国八大菜系 - 苏菜',
                'title_en': 'Chinese Eight Cuisines - Jiangsu Cuisine',
                'paragraphs': [
                    {
                        'zh': '苏菜是中国传统八大菜系之一，以江苏菜系为主，代表中国东部沿海地区的菜系特色。',
                        'en': 'Jiangsu Cuisine is one of the Eight Great Cuisines of China, mainly based on Jiangsu cuisine, representing the culinary characteristics of the eastern coastal region of China.'
                    },
                    {
                        'zh': '苏菜注重刀工，口味清鲜平和，擅长炖、焖、蒸、炒，重视调汤，保持原汁。',
                        'en': 'Jiangsu Cuisine emphasizes knife skills, with fresh and mild flavors, excelling in stewing, braising, steaming, and stir-frying, with emphasis on soup preparation and preserving original flavors.'
                    },
                    {
                        'zh': '代表名菜有：松鼠鳜鱼、清炖蟹粉狮子头、叫花鸡、水晶肴肉等。',
                        'en': 'Representative dishes include: Squirrel-shaped Mandarin Fish, Braised Pork Ball in Brown Sauce, Beggar\'s Chicken, and Crystal Meat.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            },
            '闽菜': {
                'title': '中国八大菜系 - 闽菜',
                'title_en': 'Chinese Eight Cuisines - Fujian Cuisine',
                'paragraphs': [
                    {
                        'zh': '闽菜是中国八大菜系之一，经历了中原汉族文化和当地古越族文化的混合而形成。',
                        'en': 'Fujian Cuisine is one of the Eight Great Cuisines of China, formed through the integration of Central Plains Han culture and local ancient Yue culture.'
                    },
                    {
                        'zh': '闽菜以烹制山珍海味而著称，在色香味形俱佳的基础上，尤以"香"、"味"见长，其清鲜、和醇、荤香、不腻的风格特色。',
                        'en': 'Fujian Cuisine is famous for cooking delicacies from mountains and seas. Based on excellent color, aroma, taste, and appearance, it especially excels in "aroma" and "taste", featuring fresh, mellow, fragrant but not greasy style.'
                    },
                    {
                        'zh': '代表名菜有：佛跳墙、荔枝肉、醉排骨、红糟鸡等。',
                        'en': 'Representative dishes include: Buddha Jumps Over the Wall, Lychee Pork, Drunken Spare Ribs, and Red Wine Lees Chicken.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            },
            '浙菜': {
                'title': '中国八大菜系 - 浙菜',
                'title_en': 'Chinese Eight Cuisines - Zhejiang Cuisine',
                'paragraphs': [
                    {
                        'zh': '浙菜是中国传统八大菜系之一，有着悠久的历史。浙江菜品味清鲜脆嫩，保持原料的本色和真味。',
                        'en': 'Zhejiang Cuisine is one of the Eight Great Cuisines of China with a long history. Zhejiang dishes taste fresh, crisp, and tender, maintaining the original color and true flavor of ingredients.'
                    },
                    {
                        'zh': '浙菜注重刀工、制作精细、变化较多、富有乡土气息，以爆、炒、烩、炸、烤、蒸见长，讲究清鲜脆嫩。',
                        'en': 'Zhejiang Cuisine emphasizes knife skills, fine preparation, diverse variations, and local flavor, excelling in quick-frying, stir-frying, braising, deep-frying, roasting, and steaming, featuring fresh, crisp, and tender characteristics.'
                    },
                    {
                        'zh': '代表名菜有：西湖醋鱼、龙井虾仁、叫花童鸡、东坡肉等。',
                        'en': 'Representative dishes include: West Lake Vinegar Fish, Longjing Shrimp, Beggar\'s Chicken, and Dongpo Pork.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            },
            '湘菜': {
                'title': '中国八大菜系 - 湘菜',
                'title_en': 'Chinese Eight Cuisines - Hunan Cuisine',
                'paragraphs': [
                    {
                        'zh': '湘菜是中国八大菜系之一，以湖南菜为代表。湘菜制作精细，用料广泛，口味多变，品种繁多。',
                        'en': 'Hunan Cuisine is one of the Eight Great Cuisines of China, represented by Hunan dishes. It features fine preparation, wide range of ingredients, diverse flavors, and rich varieties.'
                    },
                    {
                        'zh': '湘菜的特点是油重色浓，讲求实惠；香辣、香鲜、软嫩。重视原料互相搭配，滋味互相渗透。',
                        'en': 'Hunan Cuisine is characterized by heavy oil and deep color, emphasizing affordability; fragrant-spicy, fragrant-fresh, soft and tender. It emphasizes the matching of ingredients and the penetration of flavors.'
                    },
                    {
                        'zh': '代表名菜有：剁椒鱼头、麻辣子鸡、腊味合蒸、组庵鱼翅等。',
                        'en': 'Representative dishes include: Fish Head with Chopped Chili, Spicy Chicken, Steamed Preserved Meat, and Zu\'an Shark Fin.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            },
            '徽菜': {
                'title': '中国八大菜系 - 徽菜',
                'title_en': 'Chinese Eight Cuisines - Anhui Cuisine',
                'paragraphs': [
                    {
                        'zh': '徽菜是中国八大菜系之一，起源于安徽省徽州地区。徽菜讲究火功，擅长烧、炖、蒸，而爆、炒菜较少。',
                        'en': 'Anhui Cuisine is one of the Eight Great Cuisines of China, originated in Huizhou region of Anhui Province. It emphasizes fire control, excelling in braising, stewing, and steaming, with less quick-frying and stir-frying.'
                    },
                    {
                        'zh': '徽菜重油、重色、重火功，色泽油亮，香气浓郁，滋味醇厚。擅长烹制山珍野味、河鲜家禽。',
                        'en': 'Anhui Cuisine emphasizes heavy oil, deep color, and fire control. Dishes are glossy, aromatic, and rich in flavor. It excels in cooking mountain delicacies, game, river fish, and poultry.'
                    },
                    {
                        'zh': '代表名菜有：臭鳜鱼、火腿炖甲鱼、腌鲜鳜鱼、红烧果子狸等。',
                        'en': 'Representative dishes include: Stinky Mandarin Fish, Ham Stewed Soft-shelled Turtle, Pickled Fresh Mandarin Fish, and Braised Masked Palm Civet.'
                    }
                ],
                'difficulty': 3,
                'duration': 12
            }
        }
        
        # 创建八大菜系总览
        overview_paragraphs = [
            {
                'zh': '中国八大菜系是指鲁菜、川菜、粤菜、苏菜、闽菜、浙菜、湘菜、徽菜。这八大菜系各具特色，展现了中国烹饪艺术的博大精深。',
                'en': 'The Eight Great Cuisines of China refer to Shandong, Sichuan, Cantonese, Jiangsu, Fujian, Zhejiang, Hunan, and Anhui cuisines. Each has its unique characteristics, showcasing the profoundness of Chinese culinary art.'
            },
            {
                'zh': '鲁菜 - 起源于山东，北方菜系之首，历史悠久，技法丰富。',
                'en': 'Shandong Cuisine - Originated in Shandong, the leader of northern cuisines, with a long history and rich techniques.'
            },
            {
                'zh': '川菜 - 起源于四川，以麻辣鲜香著称，百菜百味。',
                'en': 'Sichuan Cuisine - Originated in Sichuan, famous for spicy and numbing flavors, every dish has its unique taste.'
            },
            {
                'zh': '粤菜 - 起源于广东，清淡鲜美，注重原味，精致考究。',
                'en': 'Cantonese Cuisine - Originated in Guangdong, light and fresh, emphasizing original flavors, refined and exquisite.'
            },
            {
                'zh': '苏菜 - 起源于江苏，清鲜平和，刀工精细，造型美观。',
                'en': 'Jiangsu Cuisine - Originated in Jiangsu, fresh and mild, precise knife skills, beautiful presentation.'
            },
            {
                'zh': '闽菜 - 起源于福建，重视汤鲜，善用红糟，味道独特。',
                'en': 'Fujian Cuisine - Originated in Fujian, emphasizes soup freshness, skilled in using red yeast rice, unique flavor.'
            },
            {
                'zh': '浙菜 - 起源于浙江，鲜嫩软滑，清爽利口，讲究原味。',
                'en': 'Zhejiang Cuisine - Originated in Zhejiang, tender and smooth, refreshing taste, emphasizes original flavors.'
            },
            {
                'zh': '湘菜 - 起源于湖南，香辣酸咸，油重色浓，重口味。',
                'en': 'Hunan Cuisine - Originated in Hunan, fragrant-spicy-sour-salty, heavy oil and deep color, strong flavors.'
            },
            {
                'zh': '徽菜 - 起源于安徽，重油重色，擅长烧炖，朴素实惠。',
                'en': 'Anhui Cuisine - Originated in Anhui, heavy oil and color, excels in braising and stewing, simple and affordable.'
            }
        ]
        
        # 创建总览内容
        overview_content, created = Content.objects.get_or_create(
            title='中国八大菜系简介',
            defaults={
                'title_en': 'Introduction to Chinese Eight Great Cuisines',
                'category': category,
                'content': '\n\n'.join([p['zh'] for p in overview_paragraphs]),
                'content_en': '\n\n'.join([p['en'] for p in overview_paragraphs]),
                'paragraphs': overview_paragraphs,
                'difficulty': 3,
                'duration': 15,
                'content_type': 'article'
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'[OK] 创建内容：{overview_content.title}'))
        else:
            # 更新现有内容
            overview_content.title_en = 'Introduction to Chinese Eight Great Cuisines'
            overview_content.content = '\n\n'.join([p['zh'] for p in overview_paragraphs])
            overview_content.content_en = '\n\n'.join([p['en'] for p in overview_paragraphs])
            overview_content.paragraphs = overview_paragraphs
            overview_content.save()
            self.stdout.write(f'更新内容：{overview_content.title}')
        
        # 创建每个菜系的详细内容
        for cuisine_name, cuisine_info in cuisines_data.items():
            content, created = Content.objects.get_or_create(
                title=cuisine_info['title'],
                defaults={
                    'title_en': cuisine_info['title_en'],
                    'category': category,
                    'content': '\n\n'.join([p['zh'] for p in cuisine_info['paragraphs']]),
                    'content_en': '\n\n'.join([p['en'] for p in cuisine_info['paragraphs']]),
                    'paragraphs': cuisine_info['paragraphs'],
                    'difficulty': cuisine_info['difficulty'],
                    'duration': cuisine_info['duration'],
                    'content_type': 'article'
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'[OK] 创建内容：{content.title}'))
            else:
                # 更新现有内容
                content.title_en = cuisine_info['title_en']
                content.content = '\n\n'.join([p['zh'] for p in cuisine_info['paragraphs']])
                content.content_en = '\n\n'.join([p['en'] for p in cuisine_info['paragraphs']])
                content.paragraphs = cuisine_info['paragraphs']
                content.difficulty = cuisine_info['difficulty']
                content.duration = cuisine_info['duration']
                content.save()
                self.stdout.write(f'更新内容：{content.title}')
        
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] 数据初始化完成！'))
        self.stdout.write(f'分类数量: {Category.objects.count()}')
        self.stdout.write(f'内容数量: {Content.objects.count()}')
