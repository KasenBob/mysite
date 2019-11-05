from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
# 院系信息
class depart_info(models.Model):
	depart_name = models.CharField(max_length=25, primary_key=True)


# 专业信息
class major_info(models.Model):
	major_name = models.CharField(max_length=25, primary_key=True)
	depart = models.ForeignKey('depart_info', to_field='depart_name', on_delete=models.CASCADE)


# 年级信息
class grade_info(models.Model):
	grade_name = models.CharField(max_length=25, primary_key=True)


# 班级信息
class class_info(models.Model):
	class_name = models.CharField(max_length=10, primary_key=True)


# 用户登录信息
class user_login_info(models.Model):
	account = models.CharField(max_length=25, primary_key=True)
	psword = models.CharField(max_length=25)
	have_login = models.CharField(max_length=5, default='0')
	have_alter = models.CharField(max_length=5, default='0')
	ip = models.CharField(max_length=25)


# 权限信息
class jurisdiction(models.Model):
	account = models.ForeignKey('user_login_info', to_field='account', on_delete=models.CASCADE)
	status = models.CharField(max_length=10,
	                          choices=(
		                          ("0", "学生"), ("1", "指导教师"), ("2", "辅导员"), ("3", "学院领带"), ("4", "学校领导"),
		                          ("5", "学科委员")))


class Article(models.Model):
	content = RichTextUploadingField()


class inform(models.Model):
	Recipient_acc = models.ForeignKey('user_login_info', related_name="Recipient_acc", to_field='account', on_delete=models.CASCADE)
	From_acc = models.ForeignKey('user_login_info', related_name="From_acc", to_field='account', on_delete=models.CASCADE)
	title = models.CharField(max_length=225, null=True, blank=True)
	content = models.TextField(max_length=500, null=True, blank=True )
	create_time = models.DateTimeField(auto_now=True)


