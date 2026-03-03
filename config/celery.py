import os
from celery import Celery

# BUG FIX: os.environ.setdefault PHẢI đứng trước Celery() init
# Nếu đứng sau → Celery khởi động mà không biết Django settings → ImproperlyConfigured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# BUG FIX: Bỏ 2 dòng duplicate config_from_object + autodiscover_tasks ở cuối file cũ
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()