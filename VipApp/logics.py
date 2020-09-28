from UserApp.models import User
from common import errors


def perm_required(perm_name):
    '''权限检查'''

    def outer(api_func):
        def inner(request, *args, **kwargs):
            # 检查当前用户vip的权限
            user = User.objects.get(id=request.uid)
            if user.vip.has_perm(perm_name):
                return api_func(request, *args, **kwargs)
            else:
                raise errors.PermissionErr

        return inner

    return outer
