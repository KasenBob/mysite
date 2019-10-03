from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class news(models.Model):
	title = models.CharField(max_length=25)
	content = RichTextUploadingField()
	author = models.ForeignKey('all.depart_info', to_field='depart_name', on_delete=models.SET_NULL, null=True,
	                           blank=True)
	created_time = models.DateTimeField(auto_now_add=True)
	last_update_time = models.DateTimeField(auto_now=True)
	new_photo = models.ImageField(upload_to='news', null=True, blank=True)
