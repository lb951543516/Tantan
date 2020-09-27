import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tantan.settings')

# 加载settings里定义的模块
django.setup()

'''----------------------------------------------'''
