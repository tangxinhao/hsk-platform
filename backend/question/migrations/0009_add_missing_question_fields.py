# Generated migration to add missing fields to Question table

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0008_examattempt_paperimport_and_more'),
    ]

    # 注意：Question 模型在早期迁移中已经包含 explanation 字段，
    # 这里不再重复添加 explanation，以避免在全新数据库上出现
    # "Duplicate column name 'explanation'" 的错误。
    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.questioncategory', verbose_name='题目分类'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='question.questionset', verbose_name='所属套卷'),
        ),
        migrations.AddField(
            model_name='question',
            name='difficulty',
            field=models.IntegerField(choices=[(1, '简单'), (2, '较易'), (3, '中等'), (4, '较难'), (5, '困难')], default=3, verbose_name='难度系数'),
        ),
    ]
