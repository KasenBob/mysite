from django.urls import path
from . import views

# start with blog
urlpatterns = [
	# http://localhost:8000/news/
	path('news_list/', views.news_list, name='news_list'),
	path('news_detail/', views.news_detail, name='news_detail'),
]
