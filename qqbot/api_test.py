import top.api

req=top.api.TbkItemRecommendGetRequest()
req.set_app_info(top.appinfo('27993173', '7140594b2cecdf217a667f07ba4c1ff0'))

req.fields="num_iid,title,pict_url,small_images,reserve_price,zk_final_price,user_type,provcity,item_url"
req.num_iid=123
req.count=20
req.platform=1
resp= req.getResponse()
