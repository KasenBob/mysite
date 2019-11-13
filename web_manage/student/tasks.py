from __future__ import absolute_import
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import time
from django.core.mail import send_mail
from django.conf import settings
from . import models
import all.models as all_model


# 异步任务
@task
def send_stu_inform(stu_id, title, content):
	inform = models.stu_inform()
	stu = all_model.user_login_info.objects.get(account=stu_id)
	inform.Recipient_acc = stu
	inform.title = title
	inform.content = content
	inform.save()
