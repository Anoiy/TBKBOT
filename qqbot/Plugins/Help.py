# -*- coding:utf-8 -*-
import re, urllib, nonebot
from datetime import datetime
from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment



@on_command('Help', aliases = ('帮助',))
async def Search(session: CommandSession):
    # seg = MessageSegment(data={'CQ':'image', file : 'https://img.alicdn.com//i4//3077291146//TB2NA3poDnI8KJjSszgXXc8ApXa_!!3077291146.jpg'})
    # urllib.request.urlretrieve('http://img.alicdn.com/i4/3077291146/TB2NA3poDnI8KJjSszgXXc8ApXa_!!3077291146.jpg', 'F:\\qqbot\\image\\1.jpg')
    # urllib.request.urlopen('http:///img.alicdn.com/i4/3077291146/TB2NA3poDnI8KJjSszgXXc8ApXa_!!3077291146.jpg')
    # await session.send('[CQ:image,file=http://img.alicdn.com/i4/3077291146/TB2NA3poDnI8KJjSszgXXc8ApXa_!!3077291146.jpg]')
    # bot = nonebot.get_bot()
    # await bot.send_group_msg(group_id = 211483044, message = '[CQ:image,file=http://img.alicdn.com/i4/3077291146/TB2NA3poDnI8KJjSszgXXc8ApXa_!!3077291146.jpg]')
    # ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
    # print(str(datetime.now()) + '      物料精选    ', file=ErrorLogFile)
    # ErrorLogFile.close()
    await session.send('首先感谢您的使用，指令列表如下: \n \
        输入搜索 + \'空格\' + \'您所需要搜索的商品名称关键词\' \n')







