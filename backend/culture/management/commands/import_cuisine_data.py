from django.core.management.base import BaseCommand
from culture.models import Category, Content

class Command(BaseCommand):
    help = '导入八大菜系详细数据到数据库'

    def handle(self, *args, **options):
        # 获取或创建饮食文化分类
        category, created = Category.objects.get_or_create(
            name='饮食文化',
            defaults={
                'name_en': 'Chinese Cuisine',
                'description': '中国传统饮食文化',
                'description_en': 'Traditional Chinese Cuisine Culture',
                'level': '中级'
            }
        )
        
        # 八大菜系详细数据
        cuisines_data = [
            {
                'name': '鲁菜',
                'name_en': 'Lu Cuisine',
                'title': '中国八大菜系 - 鲁菜',
                'title_en': 'Eight Major Cuisines - Lu Cuisine',
                'subtitle': '起源于山东，历史悠久，影响广泛',
                'subtitle_en': 'Originated from Shandong, with a long history and wide influence',
                'description': '鲁菜是中国传统四大菜系（也是八大菜系）中唯一的自发型菜系，是历史最悠久、技法最丰富的菜系，也是最难掌握的菜系。',
                'description_en': 'Lu Cuisine is the only spontaneous cuisine among the traditional four major cuisines (also eight major cuisines) in China, with the longest history, richest techniques, and most difficult to master.',
                'structured_data': {
                    'origin': {'zh': '山东省济南和胶东地区', 'en': 'Jinan and Jiaodong area of Shandong Province'},
                    'characteristics': {
                        'zh': ['选料考究，刀法精细', '注重调味，口味鲜咸纯正', '烹调技法全面，尤以爆、炒、扒见长', '善于制汤，精于用汤'],
                        'en': ['Meticulous ingredient selection, precise knife skills', 'Emphasis on seasoning, fresh and salty taste', 'Comprehensive cooking techniques, especially explosion, stir-frying, and braising', 'Excellent at making and using soup']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '葱烧海参', 'en': 'Braised Sea Cucumber with Scallions'}, 'desc': {'zh': '选用上等海参，配以大葱爆炒，鲜香浓郁', 'en': 'Premium sea cucumber with scallions, fragrant and rich'}},
                        {'name': {'zh': '九转大肠', 'en': 'Nine-Turn Large Intestine'}, 'desc': {'zh': '将猪大肠烧至外焦里嫩，酸甜咸辣香五味俱全', 'en': 'Pork intestine cooked to crispy outside and tender inside, with five flavors'}},
                        {'name': {'zh': '糖醋鲤鱼', 'en': 'Sweet and Sour Carp'}, 'desc': {'zh': '以黄河鲤鱼为主料，外焦里嫩，酸甜可口', 'en': 'Yellow River carp as main ingredient, crispy outside, tender inside'}},
                        {'name': {'zh': '四喜丸子', 'en': 'Four-Joy Meatballs'}, 'desc': {'zh': '象征人生四喜，肉质鲜嫩，营养丰富', 'en': 'Symbolizing four joys of life, tender and nutritious'}}
                    ],
                    'culture': {
                        'zh': '鲁菜讲究"食不厌精，脍不厌细"的孔子饮食思想，强调原汁原味和健康养生。',
                        'en': 'Lu Cuisine follows Confucius\' philosophy of "food should be refined and never tire of precision", emphasizing authenticity and health.'
                    },
                    'tips': {
                        'zh': '品尝鲁菜时，要注意其浓郁的北方风味，特别是葱姜蒜的运用非常讲究。',
                        'en': 'When tasting Lu Cuisine, pay attention to its rich northern flavor, especially the sophisticated use of scallions, ginger, and garlic.'
                    }
                }
            },
            {
                'name': '川菜',
                'name_en': 'Sichuan Cuisine',
                'title': '中国八大菜系 - 川菜',
                'title_en': 'Eight Major Cuisines - Sichuan Cuisine',
                'subtitle': '麻辣鲜香，味型丰富，川味之魂',
                'subtitle_en': 'Spicy and numbing, rich flavors, the soul of Sichuan taste',
                'description': '川菜以麻、辣、鲜、香为特色，味型多样，有"一菜一格，百菜百味"的美誉。',
                'description_en': 'Sichuan cuisine is characterized by numbing, spicy, fresh, and fragrant flavors, with diverse taste types and the reputation of "one dish, one style, hundred dishes, hundred flavors".',
                'structured_data': {
                    'origin': {'zh': '四川盆地', 'en': 'Sichuan Basin'},
                    'characteristics': {
                        'zh': ['善用麻辣，麻而不木，辣而不燥', '调味多样，有"七滋八味"之说', '取材广泛，烹调方法多样', '注重火候，讲究刀工'],
                        'en': ['Skilled use of numbing and spicy, numb but not dull, spicy but not dry', 'Diverse seasonings with "seven flavors and eight tastes"', 'Wide range of ingredients and cooking methods', 'Attention to heat control and knife skills']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '麻婆豆腐', 'en': 'Mapo Tofu'}, 'desc': {'zh': '豆腐嫩滑，麻辣鲜香，色泽红亮', 'en': 'Tender tofu, spicy and numbing, bright red color'}},
                        {'name': {'zh': '回锅肉', 'en': 'Twice-Cooked Pork'}, 'desc': {'zh': '肥而不腻，香气四溢，是川菜代表', 'en': 'Fat but not greasy, aromatic, representative of Sichuan cuisine'}},
                        {'name': {'zh': '水煮鱼', 'en': 'Boiled Fish with Chili'}, 'desc': {'zh': '鱼肉滑嫩，辣油红亮，麻辣过瘾', 'en': 'Fish tender and smooth, red spicy oil, very satisfying'}},
                        {'name': {'zh': '宫保鸡丁', 'en': 'Kung Pao Chicken'}, 'desc': {'zh': '鸡肉嫩滑，花生香脆，咸甜适中', 'en': 'Tender chicken, crispy peanuts, balanced sweet and salty'}}
                    ],
                    'culture': {
                        'zh': '川菜的麻辣味道源于四川盆地湿热的气候，当地人用辣椒和花椒驱湿除寒，形成了独特的饮食文化。',
                        'en': 'The spicy and numbing flavor of Sichuan cuisine originates from the hot and humid climate of the Sichuan Basin, where locals use chili and Sichuan pepper to dispel dampness and cold.'
                    },
                    'tips': {
                        'zh': '初次品尝川菜，建议从微辣开始，逐渐适应麻辣口味。注意花椒的"麻"和辣椒的"辣"是两种不同的感觉。',
                        'en': 'For first-time tasters, start with mild spicy and gradually adapt to the numbing and spicy taste. Note that the "numbing" from Sichuan pepper and the "spicy" from chili are two different sensations.'
                    }
                }
            },
            {
                'name': '粤菜',
                'name_en': 'Cantonese Cuisine',
                'title': '中国八大菜系 - 粤菜',
                'title_en': 'Eight Major Cuisines - Cantonese Cuisine',
                'subtitle': '清淡鲜美，注重食材本味',
                'subtitle_en': 'Light and fresh, emphasizing natural flavors',
                'description': '粤菜以清淡、鲜嫩、滑爽、原汁原味为特色，选料精细，烹调技法多样。',
                'description_en': 'Cantonese cuisine is characterized by lightness, tenderness, smoothness, and natural flavor, with careful ingredient selection and diverse cooking techniques.',
                'structured_data': {
                    'origin': {'zh': '广东省广州及周边地区', 'en': 'Guangzhou and surrounding areas of Guangdong Province'},
                    'characteristics': {
                        'zh': ['选料精细，讲究鲜活', '清淡适口，保持原味', '烹调技法多样，尤以蒸、炒为主', '注重调味，讲究火候'],
                        'en': ['Careful ingredient selection, emphasis on freshness', 'Light and palatable, preserving natural flavors', 'Diverse cooking techniques, especially steaming and stir-frying', 'Attention to seasoning and heat control']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '白切鸡', 'en': 'White Cut Chicken'}, 'desc': {'zh': '鸡皮爽滑，肉质鲜嫩，保持原汁原味', 'en': 'Smooth skin, tender meat, preserving natural flavor'}},
                        {'name': {'zh': '烧鹅', 'en': 'Roast Goose'}, 'desc': {'zh': '皮脆肉嫩，香气扑鼻，色泽红亮', 'en': 'Crispy skin, tender meat, aromatic, bright red color'}},
                        {'name': {'zh': '虾饺', 'en': 'Shrimp Dumplings'}, 'desc': {'zh': '皮薄馅鲜，晶莹剔透，是粤式早茶经典', 'en': 'Thin skin, fresh filling, translucent, classic Cantonese dim sum'}},
                        {'name': {'zh': '清蒸石斑鱼', 'en': 'Steamed Grouper'}, 'desc': {'zh': '鱼肉鲜嫩，清淡爽口，保持鱼的原汁原味', 'en': 'Tender fish, light and refreshing, preserving natural fish flavor'}}
                    ],
                    'culture': {
                        'zh': '粤菜注重"食不厌精"，讲究食材的新鲜和烹饪的精致，体现了广东人精致生活的态度。',
                        'en': 'Cantonese cuisine emphasizes "food should be refined", focusing on ingredient freshness and cooking refinement, reflecting Guangdong people\'s attitude towards refined living.'
                    },
                    'tips': {
                        'zh': '品尝粤菜时，注意细细品味食材的原汁原味，不要加太多调料。早茶文化是粤菜的重要组成部分。',
                        'en': 'When tasting Cantonese cuisine, carefully savor the natural flavors of ingredients, don\'t add too much seasoning. Dim sum culture is an important part of Cantonese cuisine.'
                    }
                }
            },
            {
                'name': '苏菜',
                'name_en': 'Jiangsu Cuisine',
                'title': '中国八大菜系 - 苏菜',
                'title_en': 'Eight Major Cuisines - Jiangsu Cuisine',
                'subtitle': '清鲜平和，甜咸适中',
                'subtitle_en': 'Fresh and mild, balanced sweet and salty',
                'description': '苏菜以清鲜平和、浓而不腻为特色，选料严谨，制作精细。',
                'description_en': 'Jiangsu cuisine is characterized by freshness and mildness, rich but not greasy, with strict ingredient selection and fine preparation.',
                'structured_data': {
                    'origin': {'zh': '江苏省苏州、扬州、南京等地', 'en': 'Suzhou, Yangzhou, Nanjing and other areas of Jiangsu Province'},
                    'characteristics': {
                        'zh': ['选料严谨，讲究刀工', '注重火候，精于炖焖', '口味清鲜，甜咸适中', '造型美观，讲究摆盘'],
                        'en': ['Strict ingredient selection, emphasis on knife skills', 'Attention to heat control, skilled in stewing', 'Fresh taste, balanced sweet and salty', 'Beautiful presentation, emphasis on plating']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '松鼠桂鱼', 'en': 'Squirrel-Shaped Mandarin Fish'}, 'desc': {'zh': '造型独特，外脆里嫩，酸甜可口', 'en': 'Unique shape, crispy outside tender inside, sweet and sour'}},
                        {'name': {'zh': '狮子头', 'en': 'Lion\'s Head Meatballs'}, 'desc': {'zh': '肉质松软，肥而不腻，入口即化', 'en': 'Soft meat, fat but not greasy, melts in mouth'}},
                        {'name': {'zh': '盐水鸭', 'en': 'Salt-Water Duck'}, 'desc': {'zh': '皮白肉嫩，肥而不腻，鲜香味美', 'en': 'White skin, tender meat, fat but not greasy, fresh and delicious'}},
                        {'name': {'zh': '扬州炒饭', 'en': 'Yangzhou Fried Rice'}, 'desc': {'zh': '粒粒分明，色香味俱全，是苏菜代表', 'en': 'Distinct grains, excellent color, aroma and taste, representative of Jiangsu cuisine'}}
                    ],
                    'culture': {
                        'zh': '苏菜讲究"淮扬细点"，体现了江南水乡的精致文化和富庶生活。',
                        'en': 'Jiangsu cuisine emphasizes "Huaiyang fine cuisine", reflecting the refined culture and prosperous life of the Jiangnan water towns.'
                    },
                    'tips': {
                        'zh': '品尝苏菜时，注意其甜咸适中的口味特点，不要期待强烈的刺激感，而是细品其清鲜平和的韵味。',
                        'en': 'When tasting Jiangsu cuisine, note its balanced sweet and salty taste, don\'t expect strong stimulation, but savor its fresh and mild charm.'
                    }
                }
            },
            {
                'name': '闽菜',
                'name_en': 'Fujian Cuisine',
                'title': '中国八大菜系 - 闽菜',
                'title_en': 'Eight Major Cuisines - Fujian Cuisine',
                'subtitle': '重视汤鲜，善用海鲜',
                'subtitle_en': 'Emphasis on soup freshness, skilled in seafood',
                'description': '闽菜以海鲜为主要原料，注重调汤，口味清鲜、淡爽。',
                'description_en': 'Fujian cuisine uses seafood as main ingredients, emphasizes soup preparation, with fresh and light taste.',
                'structured_data': {
                    'origin': {'zh': '福建省福州、闽南等地', 'en': 'Fuzhou, southern Fujian and other areas of Fujian Province'},
                    'characteristics': {
                        'zh': ['以海鲜为主，讲究鲜活', '注重调汤，汤鲜味美', '刀工精细，色彩艳丽', '口味清淡，注重原汁原味'],
                        'en': ['Seafood-based, emphasis on freshness', 'Attention to soup preparation, fresh soup', 'Fine knife skills, bright colors', 'Light taste, emphasis on natural flavors']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '佛跳墙', 'en': 'Buddha Jumps Over the Wall'}, 'desc': {'zh': '食材丰富，汤汁浓郁，营养丰富', 'en': 'Rich ingredients, thick soup, nutritious'}},
                        {'name': {'zh': '荔枝肉', 'en': 'Lychee Pork'}, 'desc': {'zh': '形似荔枝，酸甜可口，色泽鲜艳', 'en': 'Shaped like lychee, sweet and sour, bright color'}},
                        {'name': {'zh': '醉排骨', 'en': 'Drunken Spareribs'}, 'desc': {'zh': '酒香浓郁，肉质酥软，咸甜适中', 'en': 'Rich wine aroma, soft meat, balanced salty and sweet'}},
                        {'name': {'zh': '福州鱼丸', 'en': 'Fuzhou Fish Balls'}, 'desc': {'zh': '鱼肉Q弹，汤汁鲜美，是福州特色', 'en': 'Bouncy fish meat, fresh soup, Fuzhou specialty'}}
                    ],
                    'culture': {
                        'zh': '闽菜深受福建沿海地理环境影响，善于利用海鲜资源，形成了独特的海洋饮食文化。',
                        'en': 'Fujian cuisine is deeply influenced by Fujian\'s coastal geography, skilled in using seafood resources, forming a unique marine food culture.'
                    },
                    'tips': {
                        'zh': '品尝闽菜时，一定要品汤，闽菜的精华在汤中。注意品尝海鲜的鲜美原味。',
                        'en': 'When tasting Fujian cuisine, be sure to taste the soup, the essence of Fujian cuisine is in the soup. Pay attention to the fresh taste of seafood.'
                    }
                }
            },
            {
                'name': '浙菜',
                'name_en': 'Zhejiang Cuisine',
                'title': '中国八大菜系 - 浙菜',
                'title_en': 'Eight Major Cuisines - Zhejiang Cuisine',
                'subtitle': '鲜嫩软滑，清香味美',
                'subtitle_en': 'Tender and smooth, fragrant and delicious',
                'description': '浙菜以鲜嫩软滑、清香味美为特色，注重原汁原味。',
                'description_en': 'Zhejiang cuisine is characterized by tenderness and smoothness, fragrant and delicious, emphasizing natural flavors.',
                'structured_data': {
                    'origin': {'zh': '浙江省杭州、宁波、绍兴等地', 'en': 'Hangzhou, Ningbo, Shaoxing and other areas of Zhejiang Province'},
                    'characteristics': {
                        'zh': ['选料讲究，品种丰富', '注重刀工，讲究火候', '口味清鲜，鲜嫩软滑', '注重原汁原味，清香味美'],
                        'en': ['Careful ingredient selection, rich variety', 'Attention to knife skills and heat control', 'Fresh taste, tender and smooth', 'Emphasis on natural flavors, fragrant and delicious']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '西湖醋鱼', 'en': 'West Lake Fish in Vinegar Gravy'}, 'desc': {'zh': '鱼肉鲜嫩，酸甜适口，是杭州名菜', 'en': 'Tender fish, sweet and sour, famous Hangzhou dish'}},
                        {'name': {'zh': '东坡肉', 'en': 'Dongpo Pork'}, 'desc': {'zh': '肥而不腻，入口即化，色泽红亮', 'en': 'Fat but not greasy, melts in mouth, bright red color'}},
                        {'name': {'zh': '龙井虾仁', 'en': 'Longjing Shrimp'}, 'desc': {'zh': '虾仁鲜嫩，茶香扑鼻，清淡雅致', 'en': 'Tender shrimp, tea fragrance, light and elegant'}},
                        {'name': {'zh': '叫化童鸡', 'en': 'Beggar\'s Chicken'}, 'desc': {'zh': '鸡肉酥烂，香气四溢，别具风味', 'en': 'Tender chicken, aromatic, unique flavor'}}
                    ],
                    'culture': {
                        'zh': '浙菜源于江南水乡，受西湖美景影响，讲究"色、香、味、形"俱佳，体现了江南文化的优雅。',
                        'en': 'Zhejiang cuisine originates from Jiangnan water towns, influenced by West Lake scenery, emphasizing excellent "color, aroma, taste, and shape", reflecting the elegance of Jiangnan culture.'
                    },
                    'tips': {
                        'zh': '品尝浙菜时，注意其清淡雅致的特点，特别是杭州菜系，融入了西湖的秀美景色和文化底蕴。',
                        'en': 'When tasting Zhejiang cuisine, note its light and elegant characteristics, especially Hangzhou cuisine, which incorporates the beautiful scenery and cultural heritage of West Lake.'
                    }
                }
            },
            {
                'name': '湘菜',
                'name_en': 'Hunan Cuisine',
                'title': '中国八大菜系 - 湘菜',
                'title_en': 'Eight Major Cuisines - Hunan Cuisine',
                'subtitle': '香辣酸咸，口味浓重',
                'subtitle_en': 'Spicy, sour and salty, strong flavors',
                'description': '湘菜以香辣著称，注重酸辣、香鲜、软嫩，口味浓重。',
                'description_en': 'Hunan cuisine is famous for its spiciness, emphasizing sour, spicy, fragrant, fresh and tender, with strong flavors.',
                'structured_data': {
                    'origin': {'zh': '湖南省长沙、湘潭等地', 'en': 'Changsha, Xiangtan and other areas of Hunan Province'},
                    'characteristics': {
                        'zh': ['善用辣椒，香辣酸咸', '注重刀工，讲究火候', '口味浓重，色泽鲜艳', '选料广泛，品种繁多'],
                        'en': ['Skilled use of chili, spicy, sour and salty', 'Attention to knife skills and heat control', 'Strong flavors, bright colors', 'Wide ingredient selection, many varieties']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '剁椒鱼头', 'en': 'Steamed Fish Head with Chopped Chili'}, 'desc': {'zh': '鱼肉鲜嫩，辣椒香浓，色泽鲜艳', 'en': 'Tender fish, rich chili flavor, bright color'}},
                        {'name': {'zh': '毛氏红烧肉', 'en': 'Mao\'s Braised Pork'}, 'desc': {'zh': '肥而不腻，色泽红亮，香甜软糯', 'en': 'Fat but not greasy, bright red color, sweet and soft'}},
                        {'name': {'zh': '湘西外婆菜', 'en': 'Xiangxi Grandma Vegetables'}, 'desc': {'zh': '酸辣开胃，咸香可口，是湘菜经典', 'en': 'Sour and spicy appetizer, salty and delicious, Hunan cuisine classic'}},
                        {'name': {'zh': '辣椒炒肉', 'en': 'Stir-Fried Pork with Chili'}, 'desc': {'zh': '辣椒脆嫩，肉质鲜香，是家常名菜', 'en': 'Crispy chili, fresh pork, famous home-style dish'}}
                    ],
                    'culture': {
                        'zh': '湘菜的辣椒文化源于湖南湿热的气候，当地人用辣椒驱湿除寒，形成了浓郁的辣文化。',
                        'en': 'The chili culture of Hunan cuisine originates from Hunan\'s hot and humid climate, where locals use chili to dispel dampness and cold, forming a rich spicy culture.'
                    },
                    'tips': {
                        'zh': '湘菜的辣不同于川菜的麻辣，是纯粹的辣，伴随着酸香。初次品尝建议从微辣开始。',
                        'en': 'The spiciness of Hunan cuisine is different from Sichuan cuisine\'s numbing spiciness, it\'s pure spiciness accompanied by sour aroma. First-time tasters should start with mild spicy.'
                    }
                }
            },
            {
                'name': '徽菜',
                'name_en': 'Anhui Cuisine',
                'title': '中国八大菜系 - 徽菜',
                'title_en': 'Eight Major Cuisines - Anhui Cuisine',
                'subtitle': '重油重色，注重火功',
                'subtitle_en': 'Rich in oil and color, emphasis on heat control',
                'description': '徽菜以烹制山珍野味著称，重油重色，讲究火功。',
                'description_en': 'Anhui cuisine is famous for cooking mountain delicacies and game, rich in oil and color, emphasizing heat control.',
                'structured_data': {
                    'origin': {'zh': '安徽省徽州地区', 'en': 'Huizhou area of Anhui Province'},
                    'characteristics': {
                        'zh': ['善烹山珍野味，讲究食材', '重油重色，口味浓郁', '注重火功，擅长炖焖', '保持原汁原味，鲜咸适度'],
                        'en': ['Skilled in cooking mountain delicacies, emphasis on ingredients', 'Rich in oil and color, strong flavors', 'Emphasis on heat control, skilled in stewing', 'Preserving natural flavors, moderately fresh and salty']
                    },
                    'famous_dishes': [
                        {'name': {'zh': '臭鳜鱼', 'en': 'Stinky Mandarin Fish'}, 'desc': {'zh': '闻着臭吃着香，鱼肉鲜嫩，是徽菜代表', 'en': 'Smells stinky but tastes fragrant, tender fish, representative of Anhui cuisine'}},
                        {'name': {'zh': '火腿炖甲鱼', 'en': 'Stewed Turtle with Ham'}, 'desc': {'zh': '汤汁浓郁，肉质软烂，营养丰富', 'en': 'Rich soup, soft meat, nutritious'}},
                        {'name': {'zh': '黄山炖鸽', 'en': 'Huangshan Stewed Pigeon'}, 'desc': {'zh': '鸽肉鲜嫩，汤汁清香，滋补养生', 'en': 'Tender pigeon, fragrant soup, nourishing'}},
                        {'name': {'zh': '问政山笋', 'en': 'Wenzheng Mountain Bamboo Shoots'}, 'desc': {'zh': '笋质脆嫩，清香爽口，是徽菜特色', 'en': 'Crispy bamboo shoots, fragrant and refreshing, Anhui cuisine specialty'}}
                    ],
                    'culture': {
                        'zh': '徽菜源于徽州山区，就地取材，善用山珍野味，体现了徽州商人的文化和饮食智慧。',
                        'en': 'Anhui cuisine originates from Huizhou mountain area, uses local ingredients, skilled in mountain delicacies and game, reflecting the culture and culinary wisdom of Huizhou merchants.'
                    },
                    'tips': {
                        'zh': '品尝徽菜时，注意其重油重色的特点，不要被外表吓到，味道其实很鲜美。臭鳜鱼是必尝之菜。',
                        'en': 'When tasting Anhui cuisine, note its rich oil and color characteristics, don\'t be scared by appearance, the taste is actually very delicious. Stinky Mandarin Fish is a must-try.'
                    }
                }
            }
        ]
        
        # 导入数据
        for cuisine_data in cuisines_data:
            content, created = Content.objects.update_or_create(
                title=cuisine_data['title'],
                defaults={
                    'title_en': cuisine_data['title_en'],
                    'subtitle': cuisine_data['subtitle'],
                    'subtitle_en': cuisine_data['subtitle_en'],
                    'description': cuisine_data['description'],
                    'description_en': cuisine_data['description_en'],
                    'category': category,
                    'content_type': 'article',
                    'difficulty': 3,  # 中等难度
                    'structured_data': cuisine_data['structured_data'],
                    'content': cuisine_data['description']  # 简单内容，详细内容在structured_data中
                }
            )
            
            action = '创建' if created else '更新'
            self.stdout.write(self.style.SUCCESS(f'{action}菜系: {cuisine_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n成功导入 {len(cuisines_data)} 个菜系数据！'))
