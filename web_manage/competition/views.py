from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, FileResponse, JsonResponse
from django.core.cache import cache
import time
from django.conf import settings
import datetime
from . import models
import os
import all.models as all_model
import student.models as student_model
import teacher.models as teacher_model
from django.core import serializers
import json


# Create your views here.

# 小组总体报名情况
def verify_all_apply(group_id):
	group_info = get_object_or_404(models.com_group_basic_info, group_id=group_id)
	com_stu_list = student_model.com_stu_info.objects.filter(group_id=group_id)
	com_teach_list = teacher_model.com_teach_info.objects.filter(group_id=group_id)
	flag = 1
	for com_stu in com_stu_list:
		if com_stu.status == '0':
			flag = 0
			break
	if flag == 1:
		for com_teach in com_teach_list:
			if com_teach.status == '0':
				flag = 0
				break
	if flag == 1:
		group_info.status = '1'
		group_info.save()


# 竞赛列表
def series_list(request):
	context = {}
	# 没有登录或者还未修改个人信息都无法报名
	try:
		is_login = request.session['is_login']
	except KeyError:
		context['have_login'] = "赶紧登录啦 :("
	else:
		user_num = request.session['user_number']
		user_info = get_object_or_404(all_model.user_login_info, account=user_num)
		if user_info.have_alter == '0':
			context['have_alter'] = "客官还没确认个人信息啦 :( 赶紧滚去修改"
	# 个人赛
	key_1 = 'series_list_one'
	if cache.has_key(key_1):
		temp_series_list_one = cache.get(key_1)
	else:
		temp_series_list_one = models.series_info.objects.filter(type='0')
	l1 = len(temp_series_list_one)
	series_list_one = []
	temp = []
	flag = 1
	for series in temp_series_list_one:
		series.update_com_id()
		temp.append(series)
		if flag == l1:
			series_list_one.append(temp)
			temp = []
		elif flag % 4 == 0:
			series_list_one.append(temp)
			temp = []
		flag += 1
	cache.set(key_1, temp_series_list_one, 3600 - int(time.time() % 3600))
	# 团体赛
	key_2 = 'series_list_all'
	if cache.has_key(key_2):
		temp_series_list_all = cache.get(key_2)
	else:
		temp_series_list_all = models.series_info.objects.filter(type='1')
	l2 = len(temp_series_list_all)
	series_list_all = []
	temp = []
	flag = 1
	for series in temp_series_list_all:
		series.update_com_id()
		temp.append(series)
		if flag == l2:
			series_list_all.append(temp)
			temp = []
		elif flag % 4 == 0:
			series_list_all.append(temp)
			temp = []
		flag += 1
	cache.set(key_2, temp_series_list_all, 3600 - int(time.time() % 3600))

	context['series_list_one'] = series_list_one
	context['series_list_all'] = series_list_all
	return render(request, 'competition/series_list.html', context)


# 比赛列表
def com_list(request):
	context = {}
	# 没有登录或者还未修改个人信息都无法报名
	try:
		is_login = request.session['is_login']
	except KeyError:
		context['have_login'] = "赶紧登录啦 :("
	else:
		user_num = request.session['user_number']
		user_info = get_object_or_404(all_model.user_login_info, account=user_num)
		if user_info.have_alter == '0':
			context['have_alter'] = "客官还没确认个人信息啦 :( 赶紧滚去修改"
	# 个人赛
	key_1 = 'com_list_one'
	if cache.has_key(key_1):
		temp_com_list_one = cache.get(key_1)
	else:
		temp_com_list_one = models.com_basic_info.objects.filter(type='0', com_status='0')
	# temp_com_list_one = models.com_basic_info.objects.filter(type='0', com_status='0')
	l1 = len(temp_com_list_one)
	com_list_one = []
	temp = []
	flag = 1
	for com in temp_com_list_one:
		com.update_status()
		temp.append(com)
		if flag == l1:
			com_list_one.append(temp)
			temp = []
		elif flag % 4 == 0:
			com_list_one.append(temp)
			temp = []
		flag += 1
	cache.set(key_1, temp_com_list_one, 3600 - int(time.time() % 3600))
	# 团体赛

	key_2 = 'com_list_all'
	if cache.has_key(key_2):
		temp_com_list_all = cache.get(key_2)
	else:
		temp_com_list_all = models.com_basic_info.objects.filter(type='1', com_status='0')

	# temp_com_list_all = models.com_basic_info.objects.filter(type='1', com_status='0')
	l2 = len(temp_com_list_all)
	com_list_all = []
	temp = []
	flag = 1
	for com in temp_com_list_all:
		com.update_status()
		temp.append(com)
		if flag == l2:
			com_list_all.append(temp)
			temp = []
		elif flag % 4 == 0:
			com_list_all.append(temp)
			temp = []
		flag += 1
	# cache.set(key_2, temp_com_list_all, 3600 - int(time.time() % 3600))

	context['com_list_one'] = com_list_one
	context['com_list_all'] = com_list_all
	return render(request, 'competition/com_list.html', context)


# 竞赛详情
def com_detail(request):
	context = {}
	# 没有登录或者还未修改个人信息都无法报名
	try:
		is_login = request.session['is_login']
	except KeyError:
		return redirect("/competition/series_list/")
	else:
		user_num = request.session['user_number']
		user_info = get_object_or_404(all_model.user_login_info, account=user_num)
		if user_info.have_alter == '0':
			return redirect("/competition/series_list/")

	if request.method == 'GET':
		id = request.GET.get('com_id')

		object_flag = 0
		try:
			com_info = models.com_basic_info.objects.get(com_id=id)
		except ObjectDoesNotExist:
			object_flag = 1

		if object_flag != 0:
			context['warn'] = ""
			return redirect('/competition/com_list')

		object_flag = 0
		try:
			com_publish = models.com_publish_info.objects.get(com_id=com_info)
		except ObjectDoesNotExist:
			object_flag = 1

		if object_flag != 0:
			context['warn'] = ""
			return redirect('/competition/com_list')

		context['com_publish'] = com_publish
		context['com_info'] = com_info
	return render(request, 'competition/com_detail.html', context)


# 下载竞赛附件
def com_attach_download(request):
	com_id = request.GET.get('id')
	com_info = get_object_or_404(models.com_basic_info, com_id=com_id)
	com_publish = get_object_or_404(models.com_publish_info, com_id=com_info)
	# 返回下载
	filename = str(com_publish.com_attachment)
	file_path = settings.MEDIA_ROOT + filename
	ext = os.path.basename(file_path).split('.')[-1].lower()
	if ext not in ['py', 'db', 'sqlite3']:
		response = FileResponse(open(file_path, 'rb'))
		response['content_type'] = "application/octet-stream"
		response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
		return response
	else:
		raise Http404


# 报名参加比赛第一步
def com_apply_first(request):
	context = {}
	if request.method == 'GET':
		id = request.GET.get('id')
		leader_id = request.session.get('user_number')
		leader = get_object_or_404(student_model.stu_basic_info, stu_number=leader_id)
		# 获取竞赛组别信息
		group_list = models.com_sort_info.objects.filter(com_id=id)
		# 获取竞赛报名所需信息
		info_list = get_object_or_404(models.com_need_info, com_id=id)
		# 获取竞赛信息
		com_info = get_object_or_404(models.com_basic_info, com_id=id)

		context['leader'] = leader
		context['com_info'] = com_info
		context['info_list'] = info_list
		context['group_list'] = group_list
		context['tea_num'] = range(1, info_list.tea_num + 1)
		num = com_info.num_stu
		context['stu_num'] = range(1, num + 1)
		return render(request, 'competition/apply/com_apply_first.html', context)

	if request.method == "POST":
		id = request.GET.get('id')
		com_info = get_object_or_404(models.com_basic_info, com_id=id)
		info_list = get_object_or_404(models.com_need_info, com_id=id)
		group_list = models.com_sort_info.objects.filter(com_id=id)

		# 人数
		# 是否需要满员(1；需要， 0：不需要)
		# 成员能否重复（同上）
		# 作品名称不能为空
		# 还有组别信息和备注
		# 小组名称
		num = com_info.num_stu
		flag_full = com_info.need_full
		flag_same = com_info.same_stu
		flag_proname = info_list.product_name
		flag_teanum = com_info.num_teach
		flag_group = info_list.com_group
		flag_else = info_list.else_info
		flag_groupname = info_list.group_name

		# 获取页面姓名输入
		stu_list = []
		for i in range(1, num + 1):
			name = str("stu_num" + str(i))
			temp = request.POST.get(name)
			temp = temp.strip()
			if temp != None and temp != "":
				stu_list.append(temp)

		teach_list = []
		if flag_teanum:
			for i in range(1, flag_teanum + 1):
				name = str('tea_name' + str(i))
				temp = request.POST.get(name)
				teach_list.append(temp)

		# 获取学生信息
		stu_info_list = []
		for stu in stu_list:
			try:
				name = student_model.stu_basic_info.objects.get(stu_number=stu)
			except ObjectDoesNotExist:
				# 回到first页面
				context['message'] = '无法搜索到学号对应学生信息，请确认学号无误'
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'competition/apply/com_apply_first.html', context)
			else:
				stu_info_list.append(name)

		# 判断是否符合条件，不符合则跳回first页面

		# 判断是够重复报名
		flag = 1
		if flag_same == 0:
			for stu in stu_info_list:
				com_list = student_model.com_stu_info.objects.filter(stu_id=stu)
				for com in com_list:
					if com.com_id == com_info:
						flag = 0
						break
		elif flag_same == 1:
			num = 1
			for stu in stu_info_list:
				com_list = student_model.com_stu_info.objects.filter(stu_id=stu)
				if num == 1:
					for com in com_list:
						if com.com_id == com_info:
							flag = 0
							break
				else:
					for com in com_list:
						if com.is_leader == 1:
							flag = 0
							break
				num = num + 1
		if flag == 0:
			# 回到first页面
			context['message'] = '参赛成员不符合规定哦 :('
			context['com_info'] = com_info
			context['info_list'] = info_list
			context['group_list'] = group_list
			context['tea_num'] = range(1, info_list.tea_num + 1)
			num = com_info.num_stu
			context['stu_num'] = range(1, num + 1)
			return render(request, 'competition/apply/com_apply_first.html', context)

		# 判断满员
		student_num = com_info.num_stu
		len_stu = len(stu_info_list)
		if flag_full == 1:
			if len_stu != student_num:
				# 回到first页面
				context['message'] = '队伍人数不足 :('
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'competition/apply/com_apply_first.html', context)
		# 判断学号重复
		list1 = stu_info_list
		list2 = list(set(list1))
		if len(list1) != len(list2):
			# 回到first页面
			context['message'] = '有重复人员的哦 :('
			context['com_info'] = com_info
			context['info_list'] = info_list
			context['group_list'] = group_list
			context['tea_num'] = range(1, info_list.tea_num + 1)
			num = com_info.num_stu
			context['stu_num'] = range(1, num + 1)
			return render(request, 'competition/apply/com_apply_first.html', context)
		# 判断作品名称是否为空
		if flag_proname == 1:
			prodect_name = request.POST.get('product_name')
			if prodect_name == "":
				context['message'] = "作品名称没有填哦 X D "
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'competition/apply/com_apply_first.html', context)
			prodect_name = prodect_name.strip()
			context['product_name'] = prodect_name
		# 判断小组名称是否为空
		if flag_groupname == 1:
			group_name = request.POST.get('group_name')
			if group_name == "":
				context['message'] = "小组名称没有填哦 X D "
				context['com_info'] = com_info
				context['info_list'] = info_list
				context['group_list'] = group_list
				context['tea_num'] = range(1, info_list.tea_num + 1)
				num = com_info.num_stu
				context['stu_num'] = range(1, num + 1)
				return render(request, 'competition/apply/com_apply_first.html', context)
			group_name = group_name.strip()
			context['group_name'] = group_name
		# 对指导教师进行判断
		teach_list = []
		if flag_teanum:
			for i in range(1, flag_teanum + 1):
				name = str('tea_name' + str(i))
				temp = request.POST.get(name)
				temp = temp.strip()
				teach = teacher_model.teach_basic_info.objects.filter(tea_number=temp)
				if len(teach) == 0:
					# 回到first页面
					context['message'] = '无法搜索到对应指导教师信息，请确认姓名无误'
					context['com_info'] = com_info
					context['info_list'] = info_list
					context['group_list'] = group_list
					context['tea_num'] = range(1, info_list.tea_num + 1)
					num = com_info.num_stu
					context['stu_num'] = range(1, num + 1)
					return render(request, 'competition/apply/com_apply_first.html', context)
				else:
					# 教师信息列表中也是一个列表
					teach_list.append(teach)

			teach_list = zip(teach_list, range(1, info_list.tea_num + 1))
			context['teach_list'] = teach_list
		# 对组别信息进行判断
		if flag_group == 1:
			group = request.POST.get("group")
			group_list = models.com_sort_info.objects.filter(com_id=id, sort_name=group)
			context['group'] = group_list[0]
		# 备注信息
		if flag_else == 1:
			else_info = request.POST.get("else_info")
			else_info = else_info.strip()
			context['else_info'] = else_info

		# 跳转确认页面
		#print(stu_info_list)
		#print(info_list)
		context['stu_list'] = stu_info_list
		context['info_list'] = info_list
		return render(request, 'competition/apply/com_apply_second.html', context)

	return render(request, 'competition/apply/com_apply_first.html', context)


# 报名参加比赛第二步
def com_apply_second(request):
	context = {}
	if request.method == 'POST':
		id = request.GET.get('id')
		com_info = get_object_or_404(models.com_basic_info, com_id=id)
		info_list = get_object_or_404(models.com_need_info, com_id=id)
		group_list = models.com_sort_info.objects.filter(com_id=id)

		num = com_info.num_stu
		flag_full = com_info.need_full
		flag_same = com_info.same_stu
		flag_proname = info_list.product_name
		flag_teanum = com_info.num_teach
		flag_group = info_list.com_group
		flag_else = info_list.else_info
		flag_groupname = info_list.group_name

		# 优化
		stu_list = []
		for i in range(1, num + 1):
			stu_number = request.POST.get('stu_num' + str(i))
			if stu_number != None and stu_number != "":
				stu_list.append(stu_number)
		len_stu = len(stu_list)
		stu_info_list = []
		for stu in stu_list:
			name = student_model.stu_basic_info.objects.get(stu_number=stu)
			stu_info_list.append(name)

		group_name = request.POST.get('group_name')
		group = request.POST.get('group')
		product_name = request.POST.get('product_name')
		else_info = request.POST.get('else_info')

		# 分批保存信息，包括：竞赛小组信息、小组成员信息
		# 保存竞赛小组信息
		com_group = models.com_group_basic_info()
		# id
		com_group.com_id = get_object_or_404(models.com_basic_info, com_id=id)
		# 小组名字
		if flag_groupname == 1:
			com_group.group_name = group_name
		# 小组人数
		com_group.group_num = len_stu
		# 竞赛组别
		if flag_group == 1:
			group_list = models.com_sort_info.objects.filter(com_id=id, sort_name=group)
			com_group.com_group = group_list[0]
		# 作品名字
		if flag_proname == 1:
			com_group.product_name = product_name
		# 备注
		if flag_else == 1:
			com_group.else_info = else_info
		com_group.save()
		group_id = com_group.group_id
		# 保存小组成员信息
		number = 1
		for i in stu_info_list:
			stu = student_model.com_stu_info()
			stu.com_id = get_object_or_404(models.com_basic_info, com_id=id)
			stu.group_id = get_object_or_404(models.com_group_basic_info, group_id=group_id)
			stu.stu_id = i
			if number == 1:
				stu.is_leader = 1
				stu.status = '1'
			else:
				stu.status = '0'
			number += 1
			stu.save()

		teach_list = []
		if flag_teanum:
			for i in range(1, flag_teanum + 1):
				name = str('tea_name' + str(i))
				temp = request.POST.get(name)
				if temp != "" and temp != None:
					teach = teacher_model.teach_basic_info.objects.get(tea_number=temp)
					teach_list.append(teach)
			for i in teach_list:
				teach = teacher_model.com_teach_info()
				teach.com_id = get_object_or_404(models.com_basic_info, com_id=id)
				teach.group_id = get_object_or_404(models.com_group_basic_info, group_id=group_id)
				teach.teach_id = i
				teach.status = '0'
				teach.save()
		return render(request, 'competition/apply/com_apply_succeed.html', context)


# 确认报名信息
def verify_apply(request):
	context = {}
	user_id = request.GET.get('p1')
	group_id = request.GET.get('p2')

	group = get_object_or_404(models.com_group_basic_info, group_id=group_id)

	if user_id == '1':
		stu = get_object_or_404(student_model.stu_basic_info, stu_number=request.session['user_number'])
		com_stu_list = student_model.com_stu_info.objects.filter(group_id=group, stu_id=stu)
		for com_stu in com_stu_list:
			com_stu.status = '1'
			com_stu.save()
		verify_all_apply(group_id)
		return redirect('/student/personal_center_stu_apply')
	else:
		teach = get_object_or_404(teacher_model.teach_basic_info, tea_number=request.session['user_number'])
		com_teach_list = teacher_model.com_stu_info.objects.filter(group_id=group, teach_id=teach)
		for com_teach in com_teach_list:
			com_teach.status = '1'
			com_teach.save()
		verify_all_apply(group_id)
		return redirect('/student/personal_center_stu_apply')


# 选学生
def select_mate_first(request):
	context = {}
	name = request.GET.get('name')
	#print(name)
	mate_list = student_model.stu_basic_info.objects.filter(stu_name=name)
	mate_list = json.loads(serializers.serialize('json', mate_list))
	context['mate_list'] = mate_list
	return JsonResponse(context)


# 选指导教师
def select_mate_second(request):
	context = {}
	name = request.GET.get('name')
	#print(name)
	mate_list = teacher_model.teach_basic_info.objects.filter(tea_name=name)
	#print(mate_list)
	mate_list = json.loads(serializers.serialize('json', mate_list))
	context['mate_list2'] = mate_list
	return JsonResponse(context)
