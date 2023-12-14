from linebot.models import TextSendMessage
from database  import inquiry_list
import info

def manager_inquiry_list(): 
    inquiry_show = []
    db_inquiry_list = inquiry_list()

    if db_inquiry_list == '找不到符合條件的資料。':
        inquiry_show = TextSendMessage(text=db_inquiry_list)
    else:
        pagemin = info.list_page[info.user_id+'庫存min']
        pagemax = info.list_page[info.user_id+'庫存max']#9
        db_inquiry = db_inquiry_list[pagemin:pagemax]     
        product = [] #庫存產品名
        productID = [] #商品ID
        productStatus = [] #庫存狀態
        productStatusColor = [] #庫存狀態顏色
        amount = [] #庫存產品數量
        stapro = []#現預購商品
        unit = []#商品單位
        payment = []#付款方式
        


        #預購訂單賦值
        for db_inquiry_list in db_inquiry:
            product.append(db_inquiry_list[0])
            productID.append(db_inquiry_list[1])
            amount.append(db_inquiry_list[2])
            stapro.append(db_inquiry_list[3])
            unit.append(db_inquiry_list[4])
            payment.append(db_inquiry_list[5])
            if db_inquiry_list[2]<10:
                productStatus.append("庫存過低")
                productStatusColor.append("#db4d4d")
                # productStatusColor.append("#FF5151")
            else:
                productStatus.append("庫存稍微不足")
                productStatusColor.append("#FF8040")
        #列表
        for i in range(len(product)):
            inquiry_show.append({
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "【庫存快速查詢】",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※商品ID：",
                            "size": "sm",
                            "flex": 1,
                            "color": "#3b5a5f",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"{productID[i]}",
                            "wrap": True,
                            "color": "#666666",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※商品名稱：",
                            "size": "sm",
                            "flex": 1,
                            "color": "#3b5a5f",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"{product[i]}",
                            "wrap": True,
                            "color": "#666666",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※庫存狀態：",
                            "size": "sm",
                            "flex": 1,
                            "color": "#3b5a5f",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"{productStatus[i]}",
                            "wrap": True,
                            "color": f"{productStatusColor[i]}",
                            "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "※數量：",
                            "size": "sm",
                            "flex": 1,
                            "color": "#3b5a5f",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": f"{amount[i]}",
                            "wrap": True,
                            "color": "#666666",
                             "size": "md",
                            "flex": 5,
                            "weight": "bold"
                        }
                        ]
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
                    "style": "primary",
                    "height": "sm",
                    "action": {
                    "type": "message",
                    "label": "下訂",
                    "text": f"二次進貨-{stapro[i][:2]}~{productID[i]}!{unit[i]}@{payment[i]}"
                    },
                    "color": "#db4d4d"
                }
                ],
                "flex": 0
            }
            })
        if len(inquiry_show) >= 9:
              inquiry_show.append({
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
                                "text": "【庫存警示列表下一頁】"+ str(pagemax+1) +"～"+ str(pagemax+9)
                              }
                          }
                      ]
                  }
              })
        else:
              inquiry_show.append({
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
                                "label": "已經到底囉！'點我'【查詢】庫存警示",
                                "text": "【查詢】庫存警示",
                            }
                        }
                    ]
                }
            })
    return inquiry_show