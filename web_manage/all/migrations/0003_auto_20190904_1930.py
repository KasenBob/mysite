# Generated by Django 2.2.3 on 2019-09-04 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('all', '0002_auto_20190902_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jurisdiction',
            name='status',
            field=models.CharField(choices=[('0', '学生'), ('1', '指导教师'), ('2', '辅导员'), ('3', '学院领带'), ('4', '学校领导'), ('5', '学科委员')], max_length=10),
        ),
    ]