'''程序逻辑配置，及第三方平台配置'''

# 赛迪云通信
SD_APPID = '54745'
SD_APPKEY = '22d3eee0e3fc90c6c12467a407fd32d7'
SD_PROJECT = 'irWcU4'  # 短信模版id
SD_SIGN_TYPE = 'md5'  # md5 or sha1 or normal
SD_API = 'https://api.mysubmail.com/message/xsend.json'

# 七牛云配置
QN_DOMAIN = 'qh5gl9fcp.hd-bkt.clouddn.com'  # 七牛云存储空间的域名
QN_BUCKET = 'lb951543516'  # 存储空间的名字
QN_ACCESS_KEY = '3YwQK559BQapza4FgCmh7Rjy3WcpwhYDR_f039QO'
QN_SECRET_KEY = '52DEJaAoWROrefGKMrUqjKQnQO2xX-ufTfHrYBCY'
QN_CALLBACK_URL = '119.45.201.6:8000/qiniu/callback/'
QN_CALLBACK_DOMAIN = '119.45.201.6'
