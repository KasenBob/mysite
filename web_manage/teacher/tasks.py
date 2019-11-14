from __future__ import absolute_import
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import time
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import datetime
from . import models
import all.models as all_model


# 异步任务
@task
def send_teach_inform(stu_id, title, content):
	inform = models.teach_inform()
	teacher = all_model.user_login_info.objects.get(account=stu_id)
	inform.Recipient_acc = teacher
	inform.title = title
	inform.content = content
	inform.save()


@periodic_task(run_every=crontab(minute='0', hour='4', day_of_week='0'))
def delete_teach_inform():
	inform_list = models.teach_inform.objects.all()
	for inform in inform_list:
		if inform.create_time <= timezone.now() - datetime.timedelta(days=14):
			inform.delete()
