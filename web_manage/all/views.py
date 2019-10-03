from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
import datetime
from . import models
import student.models as student_model
import teacher.models as teacher_model
from .tasks import send_email_demo
from .forms import ArticleForm
import os


# Create your views here.
def home(request):
	'''
	if request.session.get('is_login', None):
		if request.session.get('user_power', None) == '0':
			student = get_object_or_404(student_model.stu_basic_info,
			                            stu_number=request.session.get('user_number', None))
			subject = '登录通知'
			message = '您已登录'
			print(student)
		send_email_demo(student, subject, message)
	'''
	context = {}
	# sendmail.delay('test@test.com')
	return render(request, 'home/home.html', context)


# 登录
def login(request):
	context = {}
	if request.session.get('is_login', None):
		return redirect('/home')

	if request.method == "POST":
		t_account = request.POST.get('account', None)
		t_psword = request.POST.get('psword', None)
		context = {}
		message = "请填写正确的账号和密码！"
		if t_account == "":
			context['message'] = "？？？输入账号啊"
			return render(request, 'home/login.html', context)
		if t_psword == "":
			context['message'] = "？？？倒是输密码啊"
			return render(request, 'home/login.html', context)
		if t_account and t_psword:
			t_account = t_account.strip()
			try:
				user = get_object_or_404(models.user_login_info, account=t_account)
				# 权限说明（学生：0; 指导老师：1; 竞赛委员：5;）
				if user.psword == t_psword:
					request.session['is_login'] = True
					request.session['user_number'] = user.account
					judge = get_object_or_404(models.jurisdiction, account=user)
					request.session['user_power'] = judge.status
					# print(request.session['user_power'])
					# print(type(request.session['user_power']))
					# 初次登录需要修改个人信息
					# 学生
					# 权限修改
					if user.have_alter == '0' and judge.status == '0':
						return redirect('/student/alter_info_stu')
					# 指导老师
					if user.have_alter == '0' and judge.status == '1':
						return redirect('/teacher/alter_info_teach')
					return redirect('/home')
				else:
					context['message'] = "???连密码都输不对吗？？？"
					return render(request, 'home/login.html', context)
			except:
				context['message'] = "账号不存在！"
				return render(request, 'home/login.html', context)
		return render(request, 'home/home.html', context)
	return render(request, 'home/login.html', context)


# 注销
def logout(request):
	if not request.session.get('is_login', None):
		return redirect("/home/")
	request.session.flush()
	return redirect("/home/")


# test
def article(request):
	context = {}
	form = ArticleForm()
	context['form'] = form
	return render(request, 'test.html', context)
