from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Avg
from .models import User
from question.models import AnswerRecord, WrongBook
from culture.models import Favorite
from university.models import University
import json

class UserProgressView(APIView):
    """用户学习进度视图"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. 基础信息
        user_data = {
            'id': user.id,
            'username': user.username,
            'chinese_name': user.chinese_name,
            'english_name': user.english_name,
            'hsk_level': user.hsk_level,
            'nationality': user.nationality,
            'avatar': user.avatar,
        }
        
        # 2. 练习统计
        answer_stats = AnswerRecord.objects.filter(user=user).aggregate(
            total_practice=Count('id'),
            total_correct=Sum('is_correct'),
            total_questions=Count('question', distinct=True)
        )
        
        # 3. 正确率计算
        total_practice = answer_stats['total_practice'] or 0
        total_correct = answer_stats['total_correct'] or 0
        accuracy_rate = 0
        if total_practice > 0:
            accuracy_rate = round((total_correct / total_practice) * 100, 2)
        
        # 4. 错题本统计
        wrong_count = WrongBook.objects.filter(user=user).count()
        
        # 5. 文化学习进度 (功能暂未实现，使用默认值)
        culture_progress = {
            'total_contents': 0,
            'completed_contents': 0,
            'avg_progress': 0
        }
        
        # 6. 收藏统计
        favorite_count = Favorite.objects.filter(user=user).count()
        
        # 7. 练习尝试统计 (功能暂未实现，使用默认值)
        exercise_stats = {
            'total_attempts': 0,
            'correct_attempts': 0
        }
        
        # 8. 构建响应数据
        progress_data = {
            'user': user_data,
            'practice_statistics': {
                'total_practice_count': total_practice,
                'total_correct_count': total_correct,
                'accuracy_rate': accuracy_rate,
                'total_questions': answer_stats['total_questions'] or 0,
                'wrong_book_count': wrong_count,
            },
            'culture_learning': {
                'total_contents': culture_progress['total_contents'] or 0,
                'completed_contents': culture_progress['completed_contents'] or 0,
                'average_progress': round(culture_progress['avg_progress'] or 0, 2),
                'favorite_count': favorite_count,
            },
            'exercise_statistics': {
                'total_attempts': exercise_stats['total_attempts'] or 0,
                'correct_attempts': exercise_stats['correct_attempts'] or 0,
                'exercise_accuracy': round(
                    (exercise_stats['correct_attempts'] or 0) / (exercise_stats['total_attempts'] or 1) * 100, 2
                ) if exercise_stats['total_attempts'] else 0,
            },
            'learning_goals': {
                'target_hsk_level': user.hsk_level + 1 if user.hsk_level < 6 else 6,
                'daily_practice_target': 10,
                'weekly_completion_target': 5,
            },
            'recommendations': {
                'suggested_level': min(user.hsk_level + 1, 6),
                'practice_focus': self.get_practice_focus(user),
            }
        }
        
        return Response(progress_data)
    
    def get_practice_focus(self, user):
        """根据用户表现确定练习重点"""
        # 获取用户各题型的正确率
        from django.db.models import Case, When, Value, IntegerField, Count, Sum
        
        # 简化版本：返回通用的建议
        if user.hsk_level <= 2:
            return "词汇和基础语法"
        elif user.hsk_level <= 4:
            return "阅读理解和听力"
        else:
            return "写作和口语表达"

class UserStudyHistoryView(generics.ListAPIView):
    """用户学习历史视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return AnswerRecord.objects.filter(user=user).order_by('-created_at')
    
    def list(self, request):
        queryset = self.get_queryset()[:20]  # 最近20条记录
        data = []
        
        for record in queryset:
            data.append({
                'id': record.id,
                'question_id': record.question.id,
                'question_content': record.question.content[:50] + '...' if len(record.question.content) > 50 else record.question.content,
                'user_answer': record.user_answer,
                'is_correct': record.is_correct,
                'created_at': record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
        
        return Response({
            'count': len(data),
            'results': data,
        })

class UniversityRecommendationView(APIView):
    """大学推荐视图"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # 获取用户偏好（这里可以扩展为从用户设置中获取）
        user_preferences = {
            'region': request.GET.get('region'),
            'major': request.GET.get('major'),
            'budget': float(request.GET.get('budget', 50000)) if request.GET.get('budget') else None,
        }
        
        # 获取所有大学
        universities = University.objects.all()
        
        # 计算匹配分数
        recommendations = []
        for university in universities:
            score = university.calculate_match_score(user.hsk_level, user_preferences)
            
            recommendations.append({
                'id': university.id,
                'name': university.name,
                'english_name': university.english_name,
                'region': university.region,
                'city': university.city,
                'ranking': university.ranking,
                'min_hsk_level': university.min_hsk_level,
                'tuition_fee': float(university.tuition_fee) if university.tuition_fee else None,
                'match_score': score,
                'logo_url': university.logo_url,
                'website': university.website,
            })
        
        # 按匹配分数排序
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)
        
        # 只返回前10个推荐
        top_recommendations = recommendations[:10]
        
        return Response({
            'user_hsk_level': user.hsk_level,
            'user_preferences': user_preferences,
            'recommendations': top_recommendations,
        })
