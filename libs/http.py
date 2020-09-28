import json

from django.http import HttpResponse
from django.conf import settings


# 将结果渲染成json数据
def render_json(data=None, code=0):
    result = {
        'data': data,
        'code': code,
    }

    # 如果是调试环境 返回格式的结果 否者返回紧凑的结果
    if settings.DEBUG is True:
        json_str = json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        json_str = json.dumps(result, ensure_ascii=False, separators=(',', ':'))

    response = HttpResponse(content=json_str, content_type='application/json')

    return response
