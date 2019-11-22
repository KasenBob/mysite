"""
Django settings for web_manage project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-o0-g!(a=)%b%!(4r+e)mu5kn!6x7nma4rfn0_&+_vk%#5ebe$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True     
    
TEMPLATE_DEBUG = False

# HOST settings
ALLOWED_HOSTS = ['49.234.197.105','172.17.0.14','127.0.0.1']

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'all',
	'student',
	'teacher',
	'competition',
	'member',
	'news',
	'djcelery',
	'ckeditor',
	'ckeditor_uploader',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_manage.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'templates'),
			# 模板地址
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'web_manage.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',  # 设置数据库
		'NAME': 'com_manage',
		'USER': 'com_manage',
		'PASSWORD': '!ab2223601',
		'HOST': 'rm-wz9kc0k65b8bx8p1a4o.mysql.rds.aliyuncs.com',
		'PORT': '3306'
	}
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

CACHES = {
	'default': {
		'BACKEND': 'django_redis.cache.RedisCache',
		'LOCATION': 'redis://127.0.0.1:6379',
		"OPTIONS": {
			"CLIENT_CLASS": "django_redis.client.DefaultClient",
		},
	},
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = 'C:/project/mysite/web_manage/collectstatic'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
	os.path.join(BASE_DIR, 'static').replace('\\', '/'),
	# 资源地址
]

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'static\\media\\').replace('\\', '/')
MEDIA_URL = '/media/'
CKEDITOR_UPLOAD_PATH = "article_images"

# Celery settings
import djcelery

djcelery.setup_loader()  # 加载djcelery

CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

BROKER_URL = 'redis://127.0.0.1:6379/0'  # redis作为中间件
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
BROKER_TRANSPORT = 'redis'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'  # Backend数据库
CELERY_WORKER_CONCURRENCY = 2
# celery 的 worker 执行多少个任务后进行重启操作
CELERY_WORKER_MAX_TASKS_PER_CHILD = 20

# Email settings
# 邮件发送配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
# 发送邮件的邮箱
EMAIL_HOST_USER = 'hzuyzk@163.com'
# 在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = 'Ab2223601'
# 收件人看到的发件人
EMAIL_FROM = 'KasenBob<hzuyzk@163.com>'  # 需要和邮箱号码一致

# editor
CKEDITOR_CONFIGS = {
	'default': {
		'toolbar': (
			['div', 'Source', '-', 'Save', 'NewPage', 'Preview', '-', 'Templates'],
			['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Print', 'SpellChecker', 'Scayt'],
			['Undo', 'Redo', '-', 'Find', 'Replace', '-', 'SelectAll', 'RemoveFormat'],
			['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField'],
			['Bold', 'Italic', 'Underline', 'Strike', '-', 'Subscript', 'Superscript'],
			['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', 'Blockquote'],
			['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
			['Link', 'Unlink', 'Anchor'],
			['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak'],
			['Styles', 'Format', 'Font', 'FontSize'],
			['TextColor', 'BGColor'],
			['Maximize', 'ShowBlocks', '-', 'About', 'pbckcode'],
		),
	}
}

