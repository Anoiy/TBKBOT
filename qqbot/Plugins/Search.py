# -*- coding:utf-8 -*-
import re, json, requests
import top.api
from datetime import datetime
from nonebot import on_command, CommandSession


# 查找命令实现
@on_command('Search', aliases = ('搜索','查询','查找',))
async def Search(session: CommandSession):
    Search_Content = session.state['Search']
    print(Search_Content)
    Search_Result_List = await ForSearch(Search_Content)
    # print(Search_Result_FI)

    try:
        # 数据加工
        Result_Len = len(Search_Result_List)

        if Result_Len <= 0:
            await session.send('未搜索到结果，请重新输入关键词')
        elif Result_Len > 0 and Result_Len < 3:
            for i in range(0, Result_Len):
                Result_Content = Search_Result_List[i]
                # print(Result_Content)

                # 图片和标题
                Send_Img_URL = Result_Content['pict_url']
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

                await session.send(Send_Content)
        else:
            for i in range(0, 3):
                Result_Content = Search_Result_List[i]

                # print(Result_Content)

                # 图片和标题
                Send_Img_URL = Result_Content['pict_url']
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

                await session.send(Send_Content)
    except Exception as e:
        ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
        print(str(datetime.now()) + '      物料搜索指令    ', file=ErrorLogFile)
        print(e, file=ErrorLogFile)
        print('\n', file=ErrorLogFile)
        ErrorLogFile.close()


# 获取相应参数
@Search.args_parser
async def _(session: CommandSession):
    strrip_args = session.current_arg_text.strip()

    # session.state[session.current_key] = strrip_args
    session.state['Search'] = strrip_args


# 连接API获取相应信息，并进行数据处理
async def ForSearch(Search_Content):
    # API请求设置
    req = top.api.TbkDgMaterialOptionalRequest()
    req.set_app_info(top.appinfo('27993173', '7140594b2cecdf217a667f07ba4c1ff0'))

    # API请求信息设置
    req.q = Search_Content
    req.adzone_id ='109623550249'

    # 提交返回结果
    try:
        Search_Result = req.getResponse()
    except Exception as e:
        ErrorLogFile = open('ErrorLog.txt', 'a+', encoding='utf-8')
        print(str(datetime.now()) + '      物料搜索    ', file=ErrorLogFile)
        print(e, file=ErrorLogFile)
        print('\n', file=ErrorLogFile)
        ErrorLogFile.close()

    # 数据处理
    # Result_Process = json.loads(Search_Result)
    if Search_Result.__contains__('error_response'):
        print('搜索物料')
        print(Search_Result)
        return ''
    Result_List = Search_Result['tbk_dg_material_optional_response']['result_list']['map_data']

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
        print(str(datetime.now()) + '      物料搜索淘口令生成    ', file=ErrorLogFile)
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
        print(str(datetime.now()) + '      物料搜索短链接生成    ', file=ErrorLogFile)
        print(e, file=ErrorLogFile)
        print('\n', file=ErrorLogFile)
        ErrorLogFile.close()
    return '抢购链接:  ' + content.text



