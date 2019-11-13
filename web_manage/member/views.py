from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404, FileResponse
from django.conf import settings
import datetime
from . import models
import os
from django.db import IntegrityError
import all.models as all_model
import competition.models as competition_model
import student.models as student_model
import teacher.models as teacher_model
import news.models as news_model
from .forms import ArticleForm


# Create your views here.
# 增加竞赛系列
def add_series(request):
	context = {}
	return render(request, 'member/add_series.html', context)


# 竞赛系列
def my_series(request):
	context = {}
	series_list = competition_model.series_info.objects.all().order_by('name')
	context['series_list'] = series_list
	for series in series_list:
		series.update_com_id()

	paginator = Paginator(series_list, 4)  # 每?篇进行分页
	page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求）
	page_of_series = paginator.get_page(page_num)
	current_page_num = page_of_series.number  # 获取当前页码
	# 获取当前前后各两页的页码范围
	page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
	             list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
	# 加上省略页面标记
	if page_range[0] - 1 >= 2:
		page_range.insert(0, '...')
	if paginator.num_pages - page_range[-1] >= 2:
		page_range.append('...')
	# 加上首页和尾页
	if page_range[0] != 1:
		page_range.insert(0, 1)
	if page_range[-1] != paginator.num_pages:
		page_range.append(paginator.num_pages)

	context['page_of_series'] = page_of_series
	context['page_range'] = page_range

	return render(request, 'member/my_series.html', context)


# 进行中的比赛
def my_com_ing(request):
	context = {}
	com_list = competition_model.com_basic_info.objects.exclude(com_status='3')
	context['com_list'] = com_list
	return render(request, 'member/my_com_ing.html', context)


# 历届比赛
def my_com_ed(request):
	context = {}

	return render(request, 'member/my_com_ed.html', context)


# 比赛详情-参赛名单
def com_apply_detail(request):
	context = {}
	com_id = request.GET.get('p')
	com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
	need_info = get_object_or_404(competition_model.com_need_info, com_id=com_id)

	com_group_list = competition_model.com_group_basic_info.objects.filter(com_id=com_info)
	com_stu_list = student_model.com_stu_info.objects.filter(group_id=com_group_list)
	com_teach_list = teacher_model.com_teach_info.objects.filter(group_id=com_group_list)

	if com_info.type == '0':
		com_group_list = competition_model.com_group_basic_info.objects.filter(com_id=com_info)
		com_apply_list = []
		stu_list = []
		teach_list = []
		for com_group in com_group_list:
			com_stu = student_model.com_stu_info.objects.get(group_id=com_group)
			stu_list.append(com_stu)
			com_teach = teacher_model.com_teach_info.objects.get(group_id=com_group)
			teach_list.append(com_teach)

		com_apply_list = zip(com_group_list, stu_list, teach_list)

	context['com_info'] = com_info
	context['need_info'] = need_info
	context['com_apply_list'] = com_apply_list
	return render(request, 'member/com_apply_detail.html', context)


def com_manage(request):
	context = {}
	com_list = competition_model.com_basic_info.objects.filter()

	context['com_list'] = com_list
	return render(request, 'member/com_management.html', context)


# 学科委员-比赛详情
def com_detail_manage(request):
	context = {}
	com_id = request.GET.get('p')
	com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
	com_need = get_object_or_404(competition_model.com_need_info, com_id=com_id)
	com_publish = get_object_or_404(competition_model.com_publish_info, com_id=com_id)
	if com_info.com_sort_num != 0:
		sort_info = competition_model.com_sort_info.objects.filter(com_id=com_info)
		sort_list = ''
		l = len(sort_info)
		t = 1
		for sort in sort_info:
			sort_name = sort.sort_name
			if t < l:
				sort_list += (sort_name + '/')
			else:
				sort_list += (sort_name)
			t += 1
		context['sort_list'] = sort_list
	context['com_info'] = com_info
	context['com_need'] = com_need
	context['com_publish'] = com_publish
	return render(request, 'member/com_detail.html', context)


# 学科委员-比赛编辑
def com_edit(request):
	context = {}
	if request.method == 'GET':
		com_id = request.GET.get('p')
		com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
		com_need = get_object_or_404(competition_model.com_need_info, com_id=com_id)
		com_publish = get_object_or_404(competition_model.com_publish_info, com_id=com_id)
		if com_info.com_sort_num != 0:
			sort_info = competition_model.com_sort_info.objects.filter(com_id=com_info)
			sort_list = ''
			l = len(sort_info)
			t = 1
			for sort in sort_info:
				sort_name = sort.sort_name
				if t < l:
					sort_list += (sort_name + '/')
				else:
					sort_list += (sort_name)
				t += 1
			context['sort_list'] = sort_list
		context['com_info'] = com_info
		context['com_need'] = com_need
		context['com_publish'] = com_publish
		return render(request, 'member/com_edit.html', context)
	if request.method == "POST":
		com_id = request.GET.get('p')
		# 竞赛信息
		name = request.POST.get('com_name')
		begin_regit = request.POST.get('begin_regit', None)
		# begin_regit = datetime.strptime(begin_regit, "%Y-%m-%d %H:%M:%S")
		end_regit = request.POST.get('end_regit', None)
		# end_regit = datetime.strptime(end_regit, "%Y-%m-%d %H:%M:%S")
		begin_time = request.POST.get('begin_time', None)
		# begin_time = datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
		end_time = request.POST.get('end_time', None)
		# end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
		if_com_sort = request.POST.get('if_com_sort', '0')
		sort_list = request.POST.get('sort_list', '0')
		com_web = request.POST.get('com_web', '0')
		num_teach = request.POST.get('num_teach', '0')
		num_stu = request.POST.get('num_stu', '0')
		need_full = request.POST.get('need_full', '0')
		same_stu = request.POST.get('same_stu', '0')

		# 学生信息
		stu_num = request.POST.get('stu_num', '0')
		stu_name = request.POST.get('stu_name', '0')
		ID_number = request.POST.get('ID_number', '0')
		sex = request.POST.get('sex', '0')
		depart = request.POST.get('depart', '0')
		major = request.POST.get('major', '0')
		grade = request.POST.get('grade', '0')
		stu_class = request.POST.get('stu_class', '0')
		email = request.POST.get('email', '0')
		phone_num = request.POST.get('phone_num', '0')
		bank_number = request.POST.get('bank_number', '0')
		else_info = request.POST.get('else_info', '0')

		# 竞赛小组信息
		group_name = request.POST.get('group_name', '0')
		product_name = request.POST.get('product_name', '0')

		# 附件
		com_attach = request.FILES.get("com_attach", None)

		# 报名步骤
		step = request.POST.get('step', None)

		# 竞赛基本信息
		com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
		com_info.com_name = name
		com_info.begin_regit = begin_regit

		com_info.end_regit = end_regit
		com_info.begin_time = begin_time
		com_info.end_time = end_time
		com_info.num_stu = num_stu
		if need_full == '1':
			com_info.need_full = 1
		else:
			com_info.need_full = 0
		if same_stu == '1':
			com_info.same_stu = 1
		else:
			com_info.same_stu = 0
		if sort_list != '0':
			list = sort_list.split("/")
			com_info.com_sort_num = len(list)
		if com_web != '0':
			com_info.if_web = 1
			com_info.com_web = com_web
		com_info.num_teach = num_teach
		com_info.save()

		# 组别信息
		if if_com_sort == '1' and sort_list != '0':
			temp_sort = competition_model.com_sort_info.objects.filter(com_id=com_info)
			for temp in temp_sort:
				temp.delete()
			list = sort_list.split("/")
			for sort in list:
				sort_info = competition_model.com_sort_info.objects.create(com_id=com_info, sort_name=sort)

		com_need = get_object_or_404(competition_model.com_need_info, com_id=com_id)
		com_need.stu_num = stu_num
		com_need.stu_name = stu_name
		com_need.ID_number = ID_number
		com_need.sex = sex
		com_need.depart = depart
		com_need.major = major
		com_need.grade = grade
		com_need.stu_class = stu_class
		com_need.email = email
		com_need.phone_num = phone_num
		if sort_list != '0':
			com_need.com_group = 1
		else:
			com_need.com_group = 0
		com_need.group_name = group_name
		com_need.product_name = product_name
		com_need.tea_num = num_teach
		com_need.bank_number = bank_number
		com_need.else_info = else_info
		com_need.save()

		# 还差公告
		com_publish = get_object_or_404(competition_model.com_publish_info, com_id=com_info)
		if com_attach != None:
			# 取出格式名
			f_name = com_attach.name
			f_name = f_name.split('.')[-1].lower()
			# 重命名文件
			com_publish.com_attachment = "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name
			url = settings.MEDIA_ROOT + 'com_attach\\' + str(com_info.com_id)
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			file_url = open(settings.MEDIA_ROOT + "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name,
			                'wb')
			for chunk in com_attach.chunks():
				file_url.write(chunk)
			file_url.close()
		if step != None or step != "":
			com_publish.apply_step = step
		com_publish.save()

		return redirect('/member/com_manage/')


# 学科委员—发布竞赛
def add_com(request):
	context = {}
	series_list = competition_model.series_info.objects.all().order_by('name')
	context['series_list'] = series_list

	if request.method == "POST":
		# 竞赛信息
		series_id = request.POST.get('com_name', None)
		com_number = request.POST.get('com_number', None)

		series = get_object_or_404(competition_model.series_info, id=series_id)
		com_name = '第' + str(com_number) + '届' + series.name

		object_flag = 0
		try:
			test = competition_model.com_basic_info.objects.get(com_name=com_name)
		except ObjectDoesNotExist:
			object_flag = 1

		if object_flag != 1:
			context['warn'] = "比赛已存在"
			return render(request, 'member/add_com/first.html', context)

		begin_regit = request.POST.get('begin_regit', None)

		end_regit = request.POST.get('end_regit', None)

		begin_time = request.POST.get('begin_time', None)

		end_time = request.POST.get('end_time', None)

		if_com_sort = request.POST.get('if_com_sort')

		sort_list = ''
		if if_com_sort == '1':
			sort_list = request.POST.get('sort_list')

		if_if_web = request.POST.get('if_if_web')
		if if_if_web:
			com_web = request.POST.get('com_web')

		num_teach = request.POST.get('num_teach', '0')

		num_stu = request.POST.get('num_stu', '0')

		need_full = request.POST.get('need_full', '0')

		same_stu = request.POST.get('same_stu', '0')

		# 欠缺处理
		if com_number == "":
			context['warn'] = "竞赛名称要填写啊kora!"
			return render(request, 'member/add_com/first.html', context)
		if begin_regit == "":
			context['warn'] = "报名开始日期要填写啊kora!"
			return render(request, 'member/add_com/first.html', context)
		if end_regit == "":
			context['warn'] = "报名结束日期要填写啊kora!"
			return render(request, 'member/add_com/first.html', context)
		if begin_time == "":
			context['warn'] = "比赛开始日期要填写啊kora!"
			return render(request, 'member/add_com/first.html', context)
		if num_teach == "":
			context['warn'] = "指导教师人数要填写啊kora!"
			return render(request, 'member/add_com/first.html', context)
		if num_stu == "":
			context['warn'] = "参赛学生人数要填写啊kora!"
			return render(request, 'member/add_com/first.html', context)

		# 学生信息
		stu_num = request.POST.get('stu_num', '0')

		stu_name = request.POST.get('stu_name', '0')

		ID_number = request.POST.get('ID_number', '0')

		sex = request.POST.get('sex', '0')

		depart = request.POST.get('depart', '0')

		major = request.POST.get('major', '0')

		grade = request.POST.get('grade', '0')

		stu_class = request.POST.get('stu_class', '0')

		email = request.POST.get('email', '0')

		phone_num = request.POST.get('phone_num', '0')

		bank_number = request.POST.get('bank_number', '0')

		else_info = request.POST.get('else_info', '0')

		# 竞赛小组信息
		group_name = request.POST.get('group_name', '0')

		product_name = request.POST.get('product_name', '0')

		# 输入数据库
		com_info = competition_model.com_basic_info()
		com_info.com_name = com_name
		com_info.series_id = series
		if int(num_stu) > 1:
			com_info.type = 1
		else:
			com_info.type = 0
		com_info.begin_regit = begin_regit
		com_info.end_regit = end_regit
		com_info.begin_time = begin_time
		com_info.end_time = end_time
		com_info.num_stu = num_stu
		if need_full == '1':
			com_info.need_full = 1
		else:
			com_info.need_full = 0
		if same_stu == '1':
			com_info.same_stu = 1
		else:
			com_info.same_stu = 0
		if if_com_sort != '0':
			list = sort_list.split("/")
			com_info.com_sort_num = len(list)
		if if_if_web != '0':
			com_info.if_web = 1
			com_info.com_web = com_web
		com_info.num_teach = num_teach
		com_info.com_status = '0'
		com_info.save()

		if sort_list != '0':
			list = sort_list.split("/")
			for sort in list:
				sort_info = competition_model.com_sort_info.objects.create(com_id=com_info, sort_name=sort)

		com_need = competition_model.com_need_info()
		com_need.com_id = com_info.com_id
		com_need.stu_num = int(stu_num)
		com_need.stu_name = int(stu_name)
		com_need.ID_number = int(ID_number)
		com_need.sex = int(sex)
		com_need.depart = int(depart)
		com_need.major = int(major)
		com_need.grade = int(grade)
		com_need.stu_class = int(stu_class)
		com_need.email = int(email)
		com_need.phone_num = int(phone_num)
		if sort_list != '0':
			com_need.com_group = int(1)
		else:
			com_need.com_group = int(0)
		com_need.group_name = int(group_name)
		com_need.product_name = int(product_name)
		com_need.tea_num = int(num_teach)
		com_need.bank_number = int(bank_number)
		com_need.else_info = int(else_info)
		com_need.save()

	return render(request, 'member/add_com/first.html', context)


# 学科委员—增加新闻
def add_notices(request):
	context = {}
	form = ArticleForm()
	context['form'] = form

	com_list = competition_model.com_basic_info.objects.all().order_by('-begin_regit')
	context['com_list'] = com_list

	if request.method == "POST":
		com_id = request.POST.get('com_id')
		com_info = get_object_or_404(competition_model.com_basic_info, com_id=com_id)
		com_attach = request.FILES.get('com_attach')

		title = request.POST.get('title')
		apply_form = ArticleForm(request.POST)
		content = ''
		if apply_form.is_valid():
			content = apply_form.cleaned_data['content']

		com_publish = competition_model.com_publish_info()
		com_publish.com_id = com_info
		com_publish.title = title
		com_publish.apply_announce = content
		if com_attach != None:
			# 取出格式名
			f_name = com_attach.name
			f_name = f_name.split('.')[-1].lower()
			# 重命名文件
			com_publish.com_attachment = "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name
			# print(com_publish.com_attachment)
			url = settings.MEDIA_ROOT + 'com_attach\\' + str(com_info.com_id)
			# 判断路径是否存在
			isExists = os.path.exists(url)
			if not isExists:
				os.makedirs(url)
			file_url = open(settings.MEDIA_ROOT + "com_attach\\" + str(com_info.com_id) + "\\" + str(
				com_info.com_id) + "." + f_name,
			                'wb')
			for chunk in com_attach.chunks():
				file_url.write(chunk)
			file_url.close()
		com_publish.save()

	return render(request, 'member/add_com/second.html', context)


# 修改小组信息申请
def apply_application(request):
	context = {}
	temp_group_list = competition_model.temp_com_group_basic_info.objects.all()
	context['temp_group_list'] = temp_group_list
	return render(request, 'member/group_change.html', context)


# 同意小组信息修改
def apply_application_agree(request):
	temp_id = request.GET.get('id')
	temp_info = get_object_or_404(competition_model.temp_com_group_basic_info, temp_id=temp_id)
	group_info = temp_info.group_id

	if temp_info.apply_type == '1':
		# 修改小组信息
		group_info.group_name = temp_info.group_name
		group_info.group_num = temp_info.group_num
		group_info.com_group = temp_info.com_group
		group_info.product_name = temp_info.product_name
		group_info.else_info = temp_info.else_info
		group_info.save()

		# 修改小组学生信息
		temp_stu_list = student_model.temp_com_stu_info.objects.filter(temp_id=temp_info)
		pre_stu_list = student_model.com_stu_info.objects.filter(group_id=group_info)
		for pre_stu in pre_stu_list:
			pre_stu.delete()
		for temp_stu in temp_stu_list:
			new_stu = student_model.com_stu_info()
			new_stu.com_id = group_info.com_id
			new_stu.group_id = group_info
			new_stu.stu_id = temp_stu.stu_id
			new_stu.is_leader = temp_stu.is_leader
			new_stu.save()
			temp_stu.delete()

		# 修改指导教师信息
		temp_teach_list = teacher_model.temp_com_teach_info.objects.filter(temp_id=temp_info)
		pre_teach_list = teacher_model.com_teach_info.objects.filter(group_id=group_info)
		for pre_teach in pre_teach_list:
			pre_teach.delete()
		for temp_teach in temp_teach_list:
			new_teach = teacher_model.com_teach_info()
			new_teach.com_id = group_info.com_id
			new_teach.group_id = group_info
			new_teach.teach_id = temp_teach.teach_id
			new_teach.save()
			temp_teach.delete()

		temp_info.delete()
	else:
		temp_stu_list = student_model.temp_com_stu_info.objects.filter(temp_id=temp_info)
		pre_stu_list = student_model.com_stu_info.objects.filter(group_id=group_info)
		for pre_stu in pre_stu_list:
			pre_stu.delete()
		for temp_stu in temp_stu_list:
			temp_stu.delete()

		temp_teach_list = teacher_model.temp_com_teach_info.objects.filter(temp_id=temp_info)
		pre_teach_list = teacher_model.com_teach_info.objects.filter(group_id=group_info)
		for pre_teach in pre_teach_list:
			pre_teach.delete()
		for temp_teach in temp_teach_list:
			temp_teach.delete()

		temp_info.delete()
		group_info.delete()

	return redirect('/member/apply_application/')


# 驳回小组信息修改
def apply_application_disagree(request):
	temp_id = request.GET.get('id')
	temp_info = get_object_or_404(competition_model.temp_com_group_basic_info, temp_id=temp_id)

	temp_stu_list = student_model.temp_com_stu_info.objects.filter(temp_id=temp_info)
	for temp_stu in temp_stu_list:
		temp_stu.delete()
	temp_teach_list = teacher_model.temp_com_teach_info.objects.filter(temp_id=temp_info)
	for temp_teach in temp_teach_list:
		temp_teach.delete()

	return redirect('/member/apply_application/')


# 个人信息修改申请
def msg_application(request):
	context = {}
	msg_stu_list = student_model.temp_stu_basic_info.objects.all()
	context['msg_stu_list'] = msg_stu_list
	msg_teach_list = teacher_model.temp_teach_basic_info.objects.all()
	context['msg_teach_list'] = msg_teach_list
	return render(request, 'member/audit_change.html', context)


# 通过个人信息修改申请
def msg_application_agree(request):
	context = {}
	# type_id=0:学生；type_id=1:指导教师
	type_id = request.GET.get('p1')
	temp_id = request.GET.get('p2')
	if type_id == '0':
		temp_stu = get_object_or_404(student_model.temp_stu_basic_info, pk=temp_id)
		pre_stu = temp_stu.stu_number
		pre_stu.stu_name = temp_stu.stu_name
		pre_stu.department = temp_stu.department
		pre_stu.major = temp_stu.major
		pre_stu.grade = temp_stu.grade
		pre_stu.stu_class = temp_stu.stu_class
		pre_stu.sex = temp_stu.sex
		pre_stu.ID_number = temp_stu.ID_number
		pre_stu.save()
		temp_stu.delete()
	else:
		temp_teach = get_object_or_404(teacher_model.temp_teach_basic_info, pk=temp_id)
		pre_teach = temp_teach.teach_number
		pre_teach.tea_name = temp_teach.tea_name
		pre_teach.profess = temp_teach.profess
		pre_teach.department = temp_teach.department
		pre_teach.save()
		temp_teach.delete()
	return redirect('/member/msg_application/')


# 驳回个人信息修改申请
def msg_application_disagree(request):
	# type_id=0:学生；type_id=1:指导教师
	type_id = request.GET.get('p1')
	temp_id = request.GET.get('p2')
	if type_id == '0':
		temp_stu = get_object_or_404(student_model.temp_stu_basic_info, pk=temp_id)
		temp_stu.delete()
	else:
		temp_teach = get_object_or_404(teacher_model.temp_teach_basic_info, pk=temp_id)
		temp_teach.delete()
	return redirect('/member/msg_application/')


# 新闻管理
def release_manage(request):
	context = {}
	news_list = news_model.news.objects.all()
	context['news_list'] = news_list
	return render(request, 'member/release_manage.html', context)