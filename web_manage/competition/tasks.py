from __future__ import absolute_import
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import time
from django.core.cache import cache
from . import models

@periodic_task(run_every=crontab(hour='*'))
def update_com_status():
	key = 'com_list'
	com_list = models.com_basic_info.objects.all()
	for com in com_list:
		com.update_status()
	return True