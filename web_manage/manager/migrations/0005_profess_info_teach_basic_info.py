# Generated by Django 2.2.3 on 2019-07-28 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_user_login_info_have_alter'),
    ]

    operations = [
        migrations.CreateModel(
            name='profess_info',
            fields=[
                ('profess_name', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='teach_basic_info',
            fields=[
                ('tea_number', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('tea_name', models.CharField(max_length=25)),
                ('ID_number', models.CharField(max_length=25)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=25, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photo')),
                ('profess', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='manager.profess_info')),
            ],
        ),
    ]
