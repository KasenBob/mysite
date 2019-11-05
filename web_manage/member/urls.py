from django.urls import path
from . import views

urlpatterns = [
	path('add_series/', views.add_series, name='add_series'),
	path('my_series/', views.my_series, name='my_series'),
	path('my_com_ing/', views.my_com_ing, name='my_com_ing'),
	path('my_com_ed/', views.my_com_ed, name='my_com_ed'),
	path('add_com/', views.add_com, name='add_com'),
	path('add_news/', views.add_news, name='add_news'),
	path('com_manage/', views.com_manage, name='com_manage'),
	path('com_detail_manage/', views.com_detail_manage, name='com_detail_manage'),
	path('com_edit/', views.com_edit, name='com_edit'),
	path('apply_application/', views.apply_application, name='apply_application'),
	path('apply_application_agree/', views.apply_application_agree, name='apply_application_agree'),
	path('apply_application_disagree/', views.apply_application_disagree, name='apply_application_disagree'),
]
