from django.db import models

class University(models.Model):
    """大学模型"""
    # 基本信息
    name = models.CharField(max_length=255, verbose_name='大学名称')
    english_name = models.CharField(max_length=255, blank=True, verbose_name='英文名称')
    region = models.CharField(max_length=100, blank=True, null=True, verbose_name='地区')
    city = models.CharField(max_length=100, blank=True, verbose_name='城市')
    ranking = models.IntegerField(blank=True, null=True, verbose_name='排名')
    ranking_national = models.IntegerField(blank=True, null=True, verbose_name='国内排名')
    ranking_world = models.IntegerField(blank=True, null=True, verbose_name='世界排名')
    
    # 详细描述
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    description_en = models.TextField(blank=True, null=True, verbose_name='英文描述')
    history = models.TextField(blank=True, verbose_name='历史沿革')
    history_en = models.TextField(blank=True, null=True, verbose_name='英文历史沿革')
    features = models.TextField(blank=True, verbose_name='特色')
    features_en = models.TextField(blank=True, null=True, verbose_name='英文特色')
    advantages = models.JSONField(blank=True, null=True, verbose_name='优势特点(中英对照)')
    campus_life = models.JSONField(blank=True, null=True, verbose_name='校园生活(中英对照)')
    
    # 学习条件
    min_hsk_level = models.IntegerField(default=1, verbose_name='最低HSK要求')
    language_requirements = models.TextField(blank=True, verbose_name='语言要求')
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='学费')
    scholarship = models.TextField(blank=True, verbose_name='奖学金')
    
    # 联系信息
    website = models.URLField(max_length=500, blank=True, verbose_name='官方网站')
    email = models.EmailField(blank=True, verbose_name='联系邮箱')
    phone = models.CharField(max_length=50, blank=True, verbose_name='联系电话')
    address = models.TextField(blank=True, verbose_name='地址')
    
    # 图片
    logo_url = models.URLField(max_length=500, blank=True, verbose_name='校徽URL')
    campus_image_url = models.URLField(max_length=500, blank=True, verbose_name='校园图片URL')
    
    # 专业信息（使用JSON存储）
    majors = models.JSONField(blank=True, null=True, verbose_name='专业列表')
    popular_majors = models.JSONField(blank=True, null=True, verbose_name='热门专业')
    
    # 统计信息
    international_students = models.IntegerField(default=0, verbose_name='国际学生数量')
    total_students = models.IntegerField(default=0, verbose_name='学生总数')
    
    # 标签
    tags = models.JSONField(blank=True, null=True, verbose_name='标签')
    
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '大学'
        verbose_name_plural = '大学'
        ordering = ['ranking']
    
    def __str__(self):
        return self.name
    
    def get_majors_list(self):
        """获取专业列表"""
        return self.majors if self.majors else []
    
    def get_popular_majors_list(self):
        """获取热门专业列表"""
        return self.popular_majors if self.popular_majors else []
    
    def get_tags_list(self):
        """获取标签列表"""
        return self.tags if self.tags else []
    
    def calculate_match_score(self, user_hsk_level, user_preferences):
        """
        计算匹配分数
        user_hsk_level: 用户的HSK水平
        user_preferences: 用户偏好（字典，包含region, major, budget等）
        """
        score = 0
        
        # 1. HSK水平匹配（权重：40%）
        if user_hsk_level >= self.min_hsk_level:
            score += 40
        else:
            # 每差一级扣10分
            score += max(0, 40 - (self.min_hsk_level - user_hsk_level) * 10)
        
        # 2. 地区匹配（权重：30%）
        if user_preferences.get('region') and user_preferences['region'] == self.region:
            score += 30
        
        # 3. 专业匹配（权重：20%）
        if user_preferences.get('major'):
            user_major = user_preferences['major']
            if self.majors and user_major in self.majors:
                score += 20
            elif self.popular_majors and user_major in self.popular_majors:
                score += 15
        
        # 4. 学费匹配（权重：10%）
        if user_preferences.get('budget') and self.tuition_fee:
            user_budget = user_preferences['budget']
            if self.tuition_fee <= user_budget:
                score += 10
            else:
                # 超出预算，按比例扣分
                over_ratio = (self.tuition_fee - user_budget) / user_budget
                score += max(0, 10 - over_ratio * 10)
        
        return min(100, score)  # 确保分数不超过100
