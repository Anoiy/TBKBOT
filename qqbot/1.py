# s = '{"warnings":{"main":{"*":"Unrecognized parameters: ver, tdsourcetag."}},"parse":{"title":"ItemSearch","pageid":89365,"text":{"*":"<div class=\"mw-parser-output\"><p>\u6ca1\u6709\u627e\u5230\u7b26\u5408\u6761\u4ef6\u7684\u7269\u54c1\u3002</p>\n</div>"}}}'
# b = '\u6ca1\u6709\u627e\u5230\u7b26\u5408\u6761\u4ef6\u7684\u7269\u54c1\u3002'
# a = s.find(b)
# print(a)
# print(1)




# import sys

# print(sys.path)




# import socket

# # 创建一个socket:
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 建立连接:
# s.bind(('www.baidu.com', 9999))



# # -*- coding: utf-8 -*-
# import top.api

# req = top.api.TbkDgMaterialOptionalRequest('www.gw.api.tbsandbox.com/router/rest', 80)
# req.set_app_info(top.appinfo('27993173', '7140594b2cecdf217a667f07ba4c1ff0'))

# req.q="123"
# req.adzone_id=123
# try:
#     resp = req.getResponse()
#     print(resp)
# except Exception as e:
#     print(e)


# import urllib.request

# urllib.request.urlretrieve('http://img.alicdn.com/i4/3077291146/TB2NA3poDnI8KJjSszgXXc8ApXa_!!3077291146.jpg', 'F:\\qqbot\\image\\1.jpg')


# import requests

# content = requests.get('http://mrw.so/api.php?url=urlencode("www.baidu.com")&key=5db055e9d3c38104fcaa9552@df049a56ac3bb8e7cc87cd5d9099a71e')
# print(content.text)


# from datetime import datetime
# import pytz

# print(datetime.now(pytz.timezone('Asia/Shanghai')).minute)

# a = -1

# def num():
#     global a
#     if not a:
#         return 1
    # return 2

if __name__ == "__main__":
    a = [1, 2, 3]
    print(a.pop(0))
    print(a)
    print(a.pop(0))
    print(a)
