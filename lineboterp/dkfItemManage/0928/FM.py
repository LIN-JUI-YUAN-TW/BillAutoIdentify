import mysql.connector
import requests
from datetime import datetime, timedelta
from mysql.connector import errorcode
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import (InvalidSignatureError)
# 載入對應的函式庫
from linebot.models import *
from relevant_information import dbinfo,imgurinfo
import os, io, pyimgur, glob
import manager
from database import product_info
import database
#-------------所有廠商名稱列出(FM)---------------
def test_manufacturers_FM(result):
  if result is not None:
    bubbles = []
    for row in result:
      mid = row[0] #廠商的編號
      mname = row[1]#廠商名稱
      bubble = {
          "type": "bubble",
          "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "xxl",
          "contents": [
              {
              "type": "text",
              "text": "【依廠商】查詢",
              "size": "xl",
              "weight": "bold"},
              {
              "type": "box",
              "layout": "vertical",
              "spacing": "sm",
              "contents": [
              {
              "type": "box",
              "layout": "vertical",
              "contents": [
                  {
                  "type": "text",
                  "text": f"廠商的編號 : {mid}",
                  "weight": "bold",
                  "margin": "xs",
                  "flex": 0},
                  {
                  "type": "text",
                  "text": f"廠商名稱 : {mname}",
                  "flex": 0,
                  "margin": "sm",
                  "weight": "bold"}
                  ]
                  }
                  ]
              },
                  {
                  "type": "separator",
                  "margin": "lg",
                  "color": "#888888"}
                  ]
              },
              "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
              {
              "type": "button",
              "style": "primary",
              "color": "#019858",
              "margin": "none",
              "action": {
                          "type": "message",
                          "label": "選我選我",
                          "text": f"選我選我 {mid}"
                          },
                          "height": "md",
                          "offsetEnd": "none",
                          "offsetBottom": "sm"}
                          ],
                          "spacing": "none",
                          "margin": "none"}
                          }
      bubbles.append(bubble)       
    flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "carousel", "contents": bubbles})
  else:
    flex_message = FlexSendMessage(alt_text="廠商列表", contents={"type": "text", "text": "找不到符合條件的廠商。"})     
  return flex_message
#---------------此廠商所有商品(已變數/FM)-------------------------


def products_manufacturers_FM(result):
  if result is not None:
    bubbles = []
    for row in result:
      pid = row[0]  # '商品ID'
      pname = row[12]  # '商品名稱'
      pphoto = row[14] # '商品圖片'
      stock_num = row[16]  # '庫存數量'
      pname_unit = row[1]  #  '商品單位'
      purchase_price = row[30] #'進貨單價'
      sell_price = row[17]  # '售出單價'
      bubble = {
          "type": "bubble",
          "hero": {
          "type": "image",
          "url": "{}".format(pphoto),
          "size": "full",
          "align": "start",
          "margin": "none",
          "offsetTop": "none",
          "aspectRatio": "20:14",
          "aspectMode": "cover",
          "offsetBottom": "xs"
        },
          "body": {
          "type": "box",
          "layout": "vertical",
          "spacing": "xxl",
          "contents": [
            {
              "type": "text",
              "text": "【商品資訊】",
              "size": "xl",
              "weight": "bold"
            },
            {
              "type": "box",
              "layout": "vertical",
              "spacing": "xl",
              "contents": [
                {
                  "type": "box",
                  "layout": "vertical",
                  "contents": [
                    {
                      "type": "text",
                      "text": f"1.商品ID: {pid}",
                      "weight": "bold",
                      "margin": "xs"
                    },
                    {
                      "type": "text",
                      "text": f"2.商品名稱：{pname}",
                      "flex": 0,
                      "margin": "sm",
                      "weight": "bold",
                      "contents": []
                    },
                    {
                      "type": "text",
                      "text": f"3.庫存數量: {stock_num}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"4.商品單位: {pname_unit}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"5.進貨單價: {purchase_price}",
                      "weight": "bold",
                      "margin": "sm"
                    },
                    {
                      "type": "text",
                      "text": f"6.售出單價: {sell_price}",
                      "weight": "bold",
                      "margin": "sm"
                    }
                  ]
                }
              ],
              "margin": "xs"
            },
            {
              "type": "separator",
              "margin": "lg",
              "color": "#888888"
            }
          ]
        },
        "footer": {
          "type": "box",
          "layout": "horizontal",
          "contents": [
            {
              "type": "button",
              "style": "primary",
              "color": "#FF7575",
              "margin": "none",
              "action": {
                "type": "message",
                "label": "停售",
                "text": "停售"
              },
              "height": "md",
              "offsetEnd": "none",
              "offsetBottom": "sm",
              "offsetStart": "none"
            },
            {
              "type": "button",
              "action": {
                "type": "message",
                "label": "修改商品資訊",
                "text": f"【修改商品資訊】{pid} "
              },
              "style": "primary",
              "color": "#46A3FF",
              "margin": "none",
              "height": "md",
              "offsetBottom": "sm",
              "offsetEnd": "none",
              "offsetStart": "xs"
            }
          ],
          "spacing": "none",
          "margin": "none"
        }
      }
      bubbles.append(bubble)
    flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "carousel", "contents": bubbles})
  else:
    flex_message = FlexSendMessage(alt_text="此廠商商品列表", contents={"type": "text", "text": "找不到符合條件的廠商商品。"})

  return flex_message
#----------------分類下所有商品列表(已變數)------------------------------
def test_categoryate_FM(result):
  if result is not None:
    bubbles = []
    for row in result:
      pid = row[0]  # '商品ID'
      pname = row[12]  # '商品名稱'
      pphoto = row[14] # '商品圖片'
      stock_num = row[16]  # '庫存數量'
      pname_unit = row[1]  #  '商品單位'
      purchase_price = row[30] #'進貨單價'
      sell_price = row[17]  # '售出單價'
      bubble = {
            "type": "bubble",
            "hero": {
            "type": "image",
            "url": "{}".format(pphoto),
            "size": "full",
            "align": "start",
            "margin": "none",
            "offsetTop": "none",
            "aspectRatio": "20:14",
            "aspectMode": "cover",
            "offsetBottom": "xs"
          },
            "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "xxl",
            "contents": [
              {
                "type": "text",
                "text": "【商品資訊】",
                "size": "xl",
                "weight": "bold"
              },
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "xl",
                "contents": [
                  {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                      {
                        "type": "text",
                        "text": f"1.商品ID: {pid}",
                        "weight": "bold",
                        "margin": "xs"
                      },
                      {
                        "type": "text",
                        "text": f"2.商品名稱：{pname}",
                        "flex": 0,
                        "margin": "sm",
                        "weight": "bold",
                        "contents": []
                      },
                      {
                        "type": "text",
                        "text": f"3.庫存數量: {stock_num}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"4.商品單位: {pname_unit}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"5.進貨單價: {purchase_price}",
                        "weight": "bold",
                        "margin": "sm"
                      },
                      {
                        "type": "text",
                        "text": f"6.售出單價: {sell_price}",
                        "weight": "bold",
                        "margin": "sm"
                      }
                    ]
                  }
                ],
                "margin": "xs"
              },
              {
                "type": "separator",
                "margin": "lg",
                "color": "#888888"
              }
            ]
          },
          "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "button",
                "style": "primary",
                "color": "#FF7575",
                "margin": "none",
                "action": {
                  "type": "message",
                  "label": "停售",
                  "text": "停售"
                },
                "height": "md",
                "offsetEnd": "none",
                "offsetBottom": "sm",
                "offsetStart": "none"
              },
              {
                "type": "button",
                "action": {
                  "type": "message",
                  "label": "修該商品資訊",
                  "text":f"【修改商品資訊】商品ID:{pid} "
                },
                "style": "primary",
                "color": "#46A3FF",
                "margin": "none",
                "height": "md",
                "offsetBottom": "sm",
                "offsetEnd": "none",
                "offsetStart": "xs"
              }
            ],
            "spacing": "none",
            "margin": "none"
          }
        }
      bubbles.append(bubble)
    flex_message = FlexSendMessage(
        alt_text="類別下所有商品",
        contents={
            "type": "carousel",
            "contents": bubbles
        }
    )
  else:
    flex_message = FlexSendMessage(
        alt_text="類別下所有商品",
        contents={
            "type": "text",
            "text": "找不到符合條件的資料。"
        }
    )
  
  return flex_message

#------該商品所有資訊(現購/依廠商查詢)--------------------
def Now_Product_Modification_FM(product_id):
  bubble = {
            "type": "bubble",
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "該商品所有資訊",
                  "weight": "bold",
                  "size": "xl",
                  "margin": "sm",
                  "style": "normal",
                  "contents": []
                },
                {
                  "type": "separator",
                  "margin": "sm"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "margin": "md",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品名稱",
                        "text": "【修改商品資訊】商品名稱"
                      },
                      "color": "#B1D3C5",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品簡介",
                        "text": "【修改商品資訊】商品簡介"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價",
                        "text": "【修改商品資訊】售出單價"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價2",
                        "text": "【修改商品資訊】售出單價2"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "更換商品圖片",
                        "text": "【修改商品資訊】更換商品圖片"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    }
                  ],
                  "spacing": "xs"
                }
              ]
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "取消修改動作",
                    "text": "取消修改動作"
                  },
                  "style": "secondary",
                  "color": "#EAD880"
                }
              ],
              "spacing": "xs",
              "margin": "md"
            },
            "styles": {
              "footer": {
                "separator": True
              }
            }
          }
  return FlexSendMessage(alt_text="產品修改選項", contents=bubble)
#------該商品所有資訊(預購/依廠商查詢)---------------------
def Pre_Product_Modification_FM(product_id):
  bubble = {        
            "type": "bubble",
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "該商品所有資訊",
                  "weight": "bold",
                  "size": "xl",
                  "margin": "sm",
                  "style": "normal",
                  "contents": []
                },
                {
                  "type": "separator",
                  "margin": "sm"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "margin": "md",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品名稱",
                        "text": "【修改商品資訊】商品名稱"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品簡介",
                        "text": "【修改商品資訊】商品簡介"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價",
                        "text": "【修改商品資訊】售出單價"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價2",
                        "text": "【修改商品資訊】售出單價2"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品預購倍數",
                        "text": "【修改商品資訊】預購倍數"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品預購截止時間",
                        "text": "【修改商品資訊】預購截止時間"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "更換商品圖片",
                        "text": "【修改商品資訊】更換商品圖片"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    }
                  ],
                  "spacing": "xs"
                }
              ]
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "取消修改動作",
                    "text": "取消修改動作"
                  },
                  "style": "secondary",
                  "color": "#EAD880"
                }
              ],
              "spacing": "xs",
              "margin": "md"
            },
            "styles": {
              "footer": {
                "separator": True
              }
            }
          }
  return FlexSendMessage(alt_text="產品修改選項", contents=bubble)
#------該商品所有資訊(現購/依類別查詢)--------------------
def Now_Product_Modification_CFM():
  bubble = {
            "type": "bubble",
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "該商品所有資訊",
                  "weight": "bold",
                  "size": "xl",
                  "margin": "sm",
                  "style": "normal",
                  "contents": []
                },
                {
                  "type": "separator",
                  "margin": "sm"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "margin": "md",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品名稱",
                        "text": "修改商品名稱"
                      },
                      "color": "#B1D3C5",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品簡介",
                        "text": "修改商品簡介"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價",
                        "text": "修改商品售出單價"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價2",
                        "text": "修改商品售出單價2"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "更換商品圖片",
                        "text": "更換商品圖片"
                      },
                      "style": "secondary",
                      "color": "#B1D3C5"
                    }
                  ],
                  "spacing": "xs"
                }
              ]
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "取消修改動作",
                    "text": "取消修改動作"
                  },
                  "style": "secondary",
                  "color": "#EAD880"
                }
              ],
              "spacing": "xs",
              "margin": "md"
            },
            "styles": {
              "footer": {
                "separator": True
              }
            }
          }
  return FlexSendMessage(alt_text="產品修改選項", contents=bubble)
#------該商品所有資訊(預購/依類別查詢)--------------------
def Pre_Product_Modification_CFM():
  bubble = {
            "type": "bubble",
            "body": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "text",
                  "text": "該商品所有資訊",
                  "weight": "bold",
                  "size": "xl",
                  "margin": "sm",
                  "style": "normal",
                  "contents": []
                },
                {
                  "type": "separator",
                  "margin": "sm"
                },
                {
                  "type": "box",
                  "layout": "vertical",
                  "margin": "md",
                  "contents": [
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品名稱",
                        "text": "修改商品名稱"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品簡介",
                        "text": "修改商品簡介"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價",
                        "text": "修改商品售出單價"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品售出單價2",
                        "text": "修改商品售出單價2"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品預購倍數",
                        "text": "修改商品預購倍數"
                      },
                      "style": "secondary",
                      "color": "#CE8467"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "修改商品預購截止時間",
                        "text": "修改商品預購截止時間"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    },
                    {
                      "type": "button",
                      "action": {
                        "type": "message",
                        "label": "更換商品圖片",
                        "text": "更換商品圖片"
                      },
                      "color": "#CE8467",
                      "style": "secondary"
                    }
                  ],
                  "spacing": "xs"
                }
              ]
            },
            "footer": {
              "type": "box",
              "layout": "vertical",
              "contents": [
                {
                  "type": "button",
                  "action": {
                    "type": "message",
                    "label": "取消修改動作",
                    "text": "取消修改動作"
                  },
                  "style": "secondary",
                  "color": "#EAD880"
                }
              ],
              "spacing": "xs",
              "margin": "md"
            },
            "styles": {
              "footer": {
                "separator": True
              }
            }
          }
  return FlexSendMessage(alt_text="產品修改選項", contents=bubble)

def create_now_purchase_product(id):
  storage = manager.global_Storage
  pname = storage[id+'pname']
  category= storage[id+'category']
  unit= storage[id+'unit']
  introduction= storage[id+'introduction']
  unitPrice= storage[id+'unitPrice']
  unitPrice2= storage[id+'unitPrice2']
  picture= storage[id+'picture']
  returnProduct= storage[id+'returnProduct']
  bubble = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_2_restaurant.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                }
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                },
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{pname}",
                      "text": '修改品名'
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{category}",
                      "text": f"修改商品類別"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unit}",
                      "text": f"修改商品單位"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{introduction}",
                      "text": f"修改商品簡介"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice}",
                      "text": f"修改商品售出單價"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice2}",
                      "text": f"修改商品售出單價2"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{picture}",
                      "text": f"修改商品圖片"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{returnProduct}",
                      "text": f"修改可否退換貨"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "secondary",
                    "color": "#EAD880",
                    "margin": "xs",
                    "action": {
                      "type": "message",
                      "label": "建立商品",
                      "text": "建立商品"
                    },
                    "height": "md"
                  }
                ],
                "spacing": "md",
                "margin": "md"
              }
            }
  screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents = bubble
                            )
  return screen


def create_preorder(id):
  storage = manager.global_Storage
  pname = storage[id+'pname']
  category= storage[id+'category']
  unit= storage[id+'unit']
  introduction= storage[id+'introduction']
  unitPrice= storage[id+'unitPrice']
  unitPrice2= storage[id+'unitPrice2']
  picture= storage[id+'picture']
  multiple= storage[id+'multiple']
  deadline= storage[id+'deadline']
  bubble = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_2_restaurant.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                }
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "action": {
                  "type": "uri",
                  "uri": "https://linecorp.com"
                },
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{pname}",
                      "text": '修改品名'
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{category}",
                      "text": f"修改商品類別"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unit}",
                      "text": f"修改商品單位"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{introduction}",
                      "text": f"修改商品簡介"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice}",
                      "text": f"修改商品售出單價"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{unitPrice2}",
                      "text": f"修改商品售出單價2"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{picture}",
                      "text": f"修改商品圖片"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{multiple}",
                      "text": f"修改商品預購倍數"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": f"{deadline}",
                      "text": f"修改商品預購截止時間"
                    },
                    "style": "secondary",
                    "color": "#B1D3C5"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "style": "secondary",
                    "color": "#EAD880",
                    "margin": "xs",
                    "action": {
                      "type": "message",
                      "label": "建立商品",
                      "text": "建立商品"
                    },
                    "height": "md"
                  }
                ],
                "spacing": "md",
                "margin": "md"
              }
            }

  screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents = bubble
                            )
  return screen

def showOrder():
    Notpickedup_preordered_history_screen = []
    id = manager.user_id
    global_Storage= manager.global_Storage
    for i in global_Storage[id+'orders'][global_Storage[id+'base']:global_Storage[id+'base'] + 10 ] :        
        orderDetail = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": "高逸嚴選",
                                "weight": "bold",
                                "color": "#1DB446",
                                "size": "sm"
                            },
                            {
                                "type": "text",
                                "text": "購物車訂單確認",
                                "weight": "bold",
                                "size": "xl",
                                "margin": "md",
                                "align": "center"
                            },
                            {
                                "type": "separator",
                                "margin": "xxl"
                            },
                            {
                                "type": "text",
                                "text": "訂單內容",
                                "size": "sm",
                                "margin": "lg",
                                "wrap": True
                            },
                           
                            {
                                "type": "separator",
                                "margin": "xxl"
                            },
                            {
                                "type": "text",
                                "text": f"總額：NT${database.getTotalByOrder(i[0][0])}",
                                "size": "md",
                                "margin": "lg",
                                "align": "center",
                                "weight": "bold"
                            }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "button",
                                "action": {
                                "type": "message",
                                "label": "【1.確認】",
                                "text": "【確認】"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                "type": "message",
                                "label": "【2.取消】",
                                "text": "【取消】"
                                }
                            }
                            ],
                            "spacing": "none",
                            "paddingAll": "sm"
                        },
                        "styles": {
                            "footer": {
                            "separator": True
                            }
                        }
                        }
        count = 5
        for j in i :
                sum = int(j[2])*int(j[3])
                a={
                      "type": "text",
                      "text":f'{j[1]}',
                      "margin": "10px"
                  }
                b={
                    "type": "text",
                    "text": f"{ j[2]}*{j[3]}={sum}$",
                    "align": "end"
                }
                orderDetail['body']['contents'].insert(count,a)
                orderDetail['body']['contents'].insert(count+1,b)
                count += 2
        Notpickedup_preordered_history_screen.append(orderDetail)
    if len(global_Storage[id+'orders'])>global_Storage[id+'base']+10:
          Notpickedup_preordered_history_screen.append({
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
                      "text": "下一頁"
                      }
                    }
                ]
            }
        })
    screen =FlexSendMessage(
                            alt_text='未取/預購/歷史訂單選擇',
                            contents={
                                "type": "carousel",
                                "contents": Notpickedup_preordered_history_screen   
                                } 
                            )
    return screen

def template_message(check_text,datetime):
  template_message = FlexSendMessage(
                            alt_text='預購截止時間選擇',
                            contents={
                                "type": "carousel",
                                "contents": [{
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "選擇日期時間",
                                        "weight": "bold",
                                        "size": "xl"
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{check_text}",
                                        "wrap": True,
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
                                        "type": "datetimepicker",
                                        "label": "點擊選擇日期與時間",
                                        "data": "預購截止時間",
                                        "mode": "datetime",
                                        "min": f"{datetime}"
                                        }
                                    }
                                    ],
                                    "flex": 0
                                }
                                }]   
                                } 
                            )
  return template_message