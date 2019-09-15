from __future__ import absolute_import
from celery.decorators import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
import time


# 异步任务
"""
@task
def sendmail(email):
	print('start send email to %s' % email)
	time.sleep(5)  # 休息5秒
	print('success')
	return True


@periodic_task(run_every=10)
def some_task():
	print('periodic task test!!!!!')
	time.sleep(5)
	print('success')
	return True
"""