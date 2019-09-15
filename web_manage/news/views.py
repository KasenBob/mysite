from django.shortcuts import render

# Create your views here.
def news_list(request):
	context = {}
	return render(request, 'news/news/news_list.html', context)

def profiles_list(request):
	context = {}
	return render(request, 'news/profile/profile_list.html', context)

def messages_list(request):
	context = {}
	return render(request, 'news/message/message_list.html', context)
