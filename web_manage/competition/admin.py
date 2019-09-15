from django.contrib import admin
from .models import com_basic_info,series_info


# Register your models here.
@admin.register(com_basic_info)
class com_basic_info_Admin(admin.ModelAdmin):
	list_display = (
	'com_id', 'com_name', 'series_id', 'begin_regit', 'end_regit', 'begin_time', 'end_time', 'num_stu', 'need_full',
	'same_stu'
	, 'com_sort_num', 'com_web', 'if_web', 'num_teach',)


@admin.register(series_info)
class series_info_Admin(admin.ModelAdmin):
	list_display = ('id','name','introduction','photo','now_com_id',)
