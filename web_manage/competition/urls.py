from django.urls import path
from . import views

urlpatterns = [
	path('series_list/', views.series_list, name='series_list'),
	path('com_detail/', views.com_detail, name='com_detail'),
	path('com_attach_download/', views.com_attach_download, name='com_attach_download'),
	path('com_apply_first/', views.com_apply_first, name='com_apply_first'),
	path('com_apply_second/', views.com_apply_second, name='com_apply_second'),
]