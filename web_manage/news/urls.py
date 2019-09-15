from django.urls import path
from . import views

# start with blog
urlpatterns = [
	# http://localhost:8000/news/
	path('news_list/', views.news_list, name='news_list'),
	path('profiles_list/', views.profiles_list, name='profiles_list'),
	path('messages_list/', views.messages_list, name='messages_list'),
]
