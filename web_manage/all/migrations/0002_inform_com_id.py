# Generated by Django 2.2.3 on 2019-11-23 19:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('competition', '0001_initial'),
        ('all', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inform',
            name='com_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='competition.com_basic_info'),
        ),
    ]