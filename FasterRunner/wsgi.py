"""
WSGI config for FasterRunner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FasterRunner.settings')

application = get_wsgi_application()
# Django会先根据settings中的WSGI_APPLICATION来获取handler；在创建project的时候
# Django会默认创建一个wsgi.py文件，而settings中的WSGI_APPLICATION配置也会默认指向这个文件。
# 看一下这个wsgi.py文件，其实它也和上面的逻辑一样，最终调用get_wsgi_application实现。
