from django.utils.deprecation import MiddlewareMixin
from common import errors
from libs.http import render_json


class AuthMiddleware(MiddlewareMixin):
    '''登录验证中间件'''

    white_list = [
        '/api/user/vcode/fetch',
        '/api/user/vcode/submit',
        '/qiniu/callback',
        '/',
    ]

    def process_request(self, request):
        # 如果当前路径在白名单，跳过
        if request.path in self.white_list:
            return

        # 如果当前路径不在白名单,检查是否登录
        uid = request.session.get('uid')
        if not uid:
            return render_json(data='用户未登录', code=errors.LOGIN_REQUIRED)
        else:
            request.uid = uid
