from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_merge_0002_initial_add_updated_at_field'),
    ]

    operations = [
        # 不再尝试添加options字段，只是一个空的迁移
        # migrations.AddField(
        #    model_name='question',
        #    name='options',
        #    field=models.TextField(blank=True, default='', verbose_name='选项'),
        # ),
    ] 