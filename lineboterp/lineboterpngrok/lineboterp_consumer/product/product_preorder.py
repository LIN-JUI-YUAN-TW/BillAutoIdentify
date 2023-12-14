from linebot.models import TextSendMessage,FlexSendMessage,QuickReplyButton,MessageAction,QuickReply
import info
from database import preorder_list,multiplesearch,unitsearch
from selection_screen import Order_buynow_preorder_screen
#-------------------預購清單----------------------
def product_preorder_list():
    product_show = ''
    db_preorder_list = preorder_list()
    if db_preorder_list == "找不到符合條件的資料。":
        product_show = TextSendMessage(text=db_preorder_list)
    else:
        pagemin = info.list_page[info.user_id+'預購min']
        pagemax = info.list_page[info.user_id+'預購max']#9
        db_preorder = db_preorder_list[pagemin:pagemax] #最多九個+1more
        show =[]#輸出全部
        product_id = []#商品ID
        product_name = []#商品名稱
        product_img = []#商品圖片
        product_description = []#商品簡介
        product_unit = []#商品單位
        product_price = []#售出單價
        product_price2 = []#售出單價2
        product_multiple = []#預購數量限制_倍數
        product_deadline = []#預購截止時間
        for db_preorder_list in db_preorder:
            if db_preorder_list[0] is None:
                break
            else:
                id = db_preorder_list[0]#商品ID
                product_id.append(id)
                name = db_preorder_list[1]#商品名稱
                #現預購商品
                product_name.append(name)
                if (db_preorder_list[3] is None) or (db_preorder_list[3][:4] != 'http'):
                    img = 'https://i.imgur.com/rGlTAt3.jpg'
                else:
                    img = db_preorder_list[3]#商品圖片
                product_img.append(img)
                description = db_preorder_list[4]#商品簡介
                product_description.append(description)
                unit = db_preorder_list[5]#商品單位
                product_unit.append(unit)
                price = db_preorder_list[6]#售出單價
                product_price.append(price)
                price2 = db_preorder_list[7]#售出單價2
                product_price2.append(price2)
                multiple = db_preorder_list[8]#預購數量限制_倍數
                product_multiple.append(multiple)
                deadline = db_preorder_list[9]#預購截止時間
                product_deadline.append(deadline)


        for i in range(len(product_id)):
            if (product_price2[i] is None) or (product_price2[i] == '') or (product_price2[i] == 0):
                price2 = '暫無其他優惠'
            else:
                price2 = f"2{product_unit[i]}起每{product_unit[i]}{str(product_price2[i])}元"
            show.append({
                "type": "bubble",
                "size": "mega",
                "direction": "ltr",
                "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                    "type": "message",
                    "label": "action",
                    "text": "【商品簡介】"+('\n%s\n%s\n'%(product_name[i],product_description[i]))
                },
                "url": product_img[i]
                },
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": product_name[i],
                    "weight": "bold",
                    "size": "lg",
                    "wrap": True
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": "※",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                            },
                            {
                            "type": "text",
                            "text": f"【截止日期 {product_deadline[i]}】",
                            "wrap": True,
                            "color": "#FF0000",
                            "size": "sm",
                            "flex": 15
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": "※",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                            },
                            {
                            "type": "text",
                            "text": f"預購數量倍數： {product_multiple[i]}",
                            "wrap": True,
                            "color": "#FF0000",
                            "size": "sm",
                            "flex": 15
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": "※",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                            },
                            {
                            "type": "text",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "text": "預購成立後將於預購商品到貨時發送取貨通知訊息",#"預購成立後將於預購截止日發送是否成功訊息"
                            "flex": 15
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": f"1{product_unit[i]}{str(product_price[i])}元",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 15
                            }
                        ],
                        "flex": 20
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": price2,
                            "wrap": True,
                            "size": "md",
                            "flex": 15,
                            "color": "#FF0000"
                            }
                        ],
                        "flex": 20
                        }
                    ]
                    }
                ]
                },
                "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "message",
                        "label": "手刀預購",
                        "text": "【手刀預購】"+product_id[i]+"_"+product_name[i]
                    }
                    }
                ],
                "flex": 0,
                "cornerRadius": "sm"
                }
        })

        if len(show) >= 9:
            show.append({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "flex": 1,
                            "gravity": "center",
                            "action": {
                                "type": "message",
                                "label": "''點我''下一頁",
                                "text": "【預購列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                            }
                        }
                    ]
                }
            })
        else:
            show.append({
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "button",
                            "flex": 1,
                            "gravity": "center",
                            "action": {
                                "type": "message",
                                "label": "已經到底囉！'點我'瀏覽其他商品",
                                "text": "團購商品"
                            }
                        }
                    ]
                }
            })
        product_show = FlexSendMessage(
                        alt_text='【預購商品】列表',
                        contents={
                            "type": "carousel",
                            "contents": show      
                            } 
                        )
    return product_show
#-------------------預購訂單----------------------
def Order_preorder(errormsg):
    user_id = info.user_id
    user_state = info.user_state
    product_id = info.product[user_id+'product_id']
    product = info.product[user_id+'product']
    storage_multiple = info.storage
    product_order_preorder = info.product_order_preorder
    product_order_preorder[user_id] = '預購'
    #Quick Reply 按鈕數量範圍
    quantity_option = []
    multiple = multiplesearch(product_id)
    storage_multiple[user_id+'multiple'] = multiple
    unit = unitsearch(product_id)
    for i in range(10):
        if unit != '無':
            if (i+1) % multiple == 0:
                quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1)+unit, text=str(i+1))))
        else:
            if (i+1) % multiple == 0:
                quantity_option.append(QuickReplyButton(action=MessageAction(label=str(i+1), text=str(i+1))))
    #------------------------
    
    user_state[user_id] = 'preorder'#從user_state轉換預購狀態
     # 建立畫面及Quick Reply 按鈕
    quickreply = QuickReply(items=quantity_option)
    Order_preorder_text = Order_buynow_preorder_screen(product_order_preorder[user_id],product_id,product,quickreply,errormsg)
    return Order_preorder_text