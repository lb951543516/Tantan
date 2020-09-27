'''程序错误码'''
OK = 0  # 正常
VCODE_FAILD = 1000  # 验证码发送失败
VCODE_ERR = 1001  # 验证码错误
LOGIN_REQUIRED = 1002  # 需要⽤户登陆
PROFILE_ERR = 1003  # ⽤户资料表单数据错误
SDD_ERR = 1004  # SID 错误
SLIDE_TYPE_ERR = 1005  # 滑动类型错误
REPEAT_SLIDE = 1006  # 重复滑动
REWIND_LIMIT = 1007  # 反悔次数达到限制
REWIND_OVERTIME = 1008  # 反悔超时
NO_SLIDE_RECORD = 1009  # 当前还没有滑动记录
Permission_DENIED = 1010  # ⽤户不具有某权限
