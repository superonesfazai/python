from fzutils.common_utils import json_2_dict
from fzutils.ocr_utils import yundama_ocr_captcha

with open('/Users/afa/myFiles/pwd/yundama_pwd.json', 'r') as f:
    yundama_info = json_2_dict(f.read())

username = yundama_info['username']
pwd = yundama_info['pwd']
app_key = yundama_info['app_key']
res = yundama_ocr_captcha(
    username=username,
    pwd=pwd,
    app_key=app_key,
    img_path='./data/captcha.jpg')
print('识别结果:{}'.format(res))