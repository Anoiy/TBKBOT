# -*- coding:utf-8 -*-
from datetime import datetime
import nonebot
import pytz, requests, sys
import top.api
from aiocqhttp.exceptions import Error as CQHttpError


'''
    全局变量定义：
        Loop_Num：循环便利返回的数据数组下标
        Optimus：返回的数据，Dict类型
        No_Duplicate：对返回内容的每个项目ID进行存储，如遇到重复则重新获取
'''
Loop_Num = 0
Optimus = {}
No_Duplicate = []


# 计划任务发送精选信息
@nonebot.scheduler.scheduled_job('cron', hour = '*', minute = '*', second = '*/10')
async def _():
    # 获取全局变量，以及时间
    global Loop_Num, Optimus
    # now = datetime.now(pytz.timezone('Asia/Shanghai'))

    # 获取机器人本身
    bot = nonebot.get_bot()
    try:
        # print(Search_Result_List)

        Result_Content = await Remove_Duplicate()

        # print(Result_Content)

        # 图片和标题
        Send_Img_URL = 'http:' + Result_Content['pict_url']
        Send_Content = '[CQ:image,cache=0,file=' + Send_Img_URL + ']' + '\n' + Result_Content['title']

        # 优惠券信息
        if Result_Content.__contains__('coupon_info'):
            Send_Content += '\n' + Result_Content['coupon_info']

        # 券后价
        if Result_Content.__contains__('zk_final_price') and Result_Content.__contains__('coupon_amount'):
            Final_Price = float(Result_Content['zk_final_price']) - float(Result_Content['coupon_amount'])
            Send_Content += '\n' + '券后价 ' + str(round(Final_Price, 2)) + '元'

        # 商品描述
        if Result_Content.__contains__('item_description'):
            Send_Content += '\n' + Result_Content['item_description']

        # 优惠券链接
        if Result_Content.__contains__('coupon_share_url'):
            TPWD = await Create_TPWD(Result_Content['coupon_share_url'], Result_Content['title'])
            Short_URL = await Get_Short_URL(Result_Content['coupon_share_url'])
            if Short_URL:
                Send_Content += '\n' + Short_URL
            if TPWD:
                Send_Content += '\n' + TPWD
            
        await bot.send_group_msg(group_id = 839514524,
                                 message = Send_Content)

    except Exception as e:
        ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
        print(str(datetime.now()) + '      计划任务    ', file=ErrorLogFile)
        print(e, file=ErrorLogFile)
        print('\n', file=ErrorLogFile)
        ErrorLogFile.close()


# 物料精选
async def Choose():
    # API请求设置
    req = top.api.TbkDgOptimusMaterialRequest()
    req.set_app_info(top.appinfo('27993173', '7140594b2cecdf217a667f07ba4c1ff0'))

    # API请求信息设置
    global Loop_Num
    req.adzone_id = '109623550249'
    req.material_id = '3756'
    req.page_size = 100

    # 提交返回结果
    try:
        Search_Result = req.getResponse()
    except Exception as e:
        ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
        print(str(datetime.now()) + '      物料精选    ', file=ErrorLogFile)
        print(e, file=ErrorLogFile)
        print('\n', file=ErrorLogFile)
        ErrorLogFile.close()

    # 数据处理
    # Result_Process = json.loads(Search_Result)
    if Search_Result.__contains__('error_response'):
        print('物料精选')
        print(Search_Result)
        return ''
    Result_List = Search_Result['tbk_dg_optimus_material_response']['result_list']['map_data']

    return Result_List


# 淘口令生成
async def Create_TPWD(Initial_URL, Tittle_Text):

    if not Initial_URL:
        return ''

    # API请求设置
    req = top.api.TbkTpwdCreateRequest()
    req.set_app_info(top.appinfo('27993173', '7140594b2cecdf217a667f07ba4c1ff0'))

    # API请求信息设置
    req.url = 'https:' + Initial_URL
    req.text = Tittle_Text
    
    # 提交返回结果
    try:
        Create_Result = req.getResponse()
    except Exception as e:
        ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
        print(str(datetime.now()) + '      物料精选淘口令生成    ', file=ErrorLogFile)
        print(e, file=ErrorLogFile)
        print('\n', file=ErrorLogFile)
        ErrorLogFile.close()

    # 数据处理
    if Create_Result.__contains__('error_response'):
        print('淘口令生成')
        print(Create_Result)
        return ''
    return '复制这条信息，打开「手机淘宝」领券后下单' + Create_Result['tbk_tpwd_create_response']['data']['model']


# 短链接生成
async def Get_Short_URL(Initial_URL):
    # # API请求设置
    # req = taobao.top.api.TbkSpreadGetRequest()
    # req.set_app_info(taobao.top.appinfo('27993173', '7140594b2cecdf217a667f07ba4c1ff0'))

    # # API请求信息设置
    # req.requests = Initial_URL

    # # 提交返回结果
    # try:
    #     Create_Result = req.getResponse()
    # except Exception as e:
    #     print(e)

    # # 数据处理
    # if Create_Result.__contains__('error_response'):
    #     print('短链接生成')
    #     print(Create_Result)
    #     return ''
    # return '点击链接，立即领券下单: ' + Create_Result['tbk_spread_get_response']['results']['tbk_spread']['content']
    try:
        content = requests.get('http://mrw.so/api.php?url=http:' + Initial_URL + '&key=5db055e9d3c38104fcaa9552@df049a56ac3bb8e7cc87cd5d9099a71e')
    except Exception as e:
        ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
        print(str(datetime.now()) + '      物料精选短链接生成    ', file=ErrorLogFile)
        print(e, file=ErrorLogFile)
        print('\n', file=ErrorLogFile)
        ErrorLogFile.close()
    return '抢购链接:  ' + content.text


# 获取去重后数据
async def Remove_Duplicate():
    global Loop_Num, Optimus, No_Duplicate
    Func_Loop_Num = 0

    # 如果第一次运行，或者索引达到最大，将获取相应数据，并重置，如果循环次数大于20次还未获取到数据，则自动终止
    if Loop_Num == 99 or Loop_Num == 0:
        while not Optimus:
            Func_Loop_Num += 1
            if Func_Loop_Num == 20:
                ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
                print('多次没有获取到相应数据，自动终止', file=ErrorLogFile)
                ErrorLogFile.close()
                sys.exit(0)
            Optimus = await Choose()
        Func_Loop_Num = 0
        Loop_Num = 0

    Result_Content = Optimus[Loop_Num]

    # 当No_Duplicate数组的元素数量等于300个时，则删除前面200个元素
    if len(No_Duplicate) == 300:
        for i in range(0, 200):
            No_Duplicate.pop(i)

    # 如果没有item_id这个值，将取下一个值
    if not Result_Content.__contains__('item_id'):
        Loop_Num += 1
        return await Remove_Duplicate()

    Content_ID = Result_Content['item_id']

    # 如果没有在No_Duplicate数组中发现重复的id，则在数组中添加进去，并返回该id的数据，如果有发现重复，则遍历下一个值
    if not No_Duplicate.count(Content_ID):
        No_Duplicate.append(Content_ID)
        # Loop_Num += 1
        return Result_Content
    else:
        Loop_Num += 1
        return await Remove_Duplicate()

        

                    




















