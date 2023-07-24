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
import lineboterp
#安裝 Python 的 MySQL 連接器及其相依性>pip install mysql-connector-python
#安裝Python 的 pyimgur套件> pip install pyimgur
# Obtain connection string information from the portal

#-------------------取得現在時間----------------------
current_datetime = datetime.now()# 取得當前的日期和時間
modified_datetime = current_datetime + timedelta(hours=8)#時區轉換+8
formatted_datetime = modified_datetime.strftime('%Y-%m-%d %H:%M:%S')# 格式化日期和時間，不包含毫秒部分
formatted_date = modified_datetime.strftime('%Y-%m-%d')#格式化日期
order_date = modified_datetime.strftime('%Y%m%d')#格式化日期，清除-
#-------------------資料庫連線----------------------
def databasetest():
  #取得資料庫資訊
  dbdata = dbinfo()  
  config = {
  'host': dbdata['host'],
  'user': dbdata['user'],
  'password': dbdata['password'],
  'database': dbdata['database']
  }
  # Construct connection string
  try:
    conn = mysql.connector.connect(**config)
    databasetest_msg = '資料庫連接成功'
  except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      databasetest_msg = '使用者或密碼有錯'
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      databasetest_msg = '資料庫不存在或其他錯誤'
    else:
      databasetest_msg = err
  else:
    cursor = conn.cursor()
  return {'databasetest_msg': databasetest_msg, 'conn':conn, 'cursor':cursor, 'config':config}
#-------------------檢查userid是否在資料庫即是否有購物車基本資料----------------------
def member_profile(userid):
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = """SELECT 會員_LINE_ID FROM member_profile;""" #會員資料檢查
  cursor.execute(query)
  member_result = cursor.fetchall()
  query1 = f"""
          SELECT 訂單編號, 會員_LINE_ID ,訂單成立時間
          FROM Order_information 
          WHERE 訂單編號 like'cart%' and 訂單成立時間 <= '{formatted_datetime}'
          ORDER BY 訂單成立時間 DESC;
          """#購物車資料檢查(DESC遞減取得最新)
  cursor.execute(query1)
  Order_result = cursor.fetchall()
  storagememberlist = []#存放查詢到的所有會員列表
  storagecartlist = []#存放查詢到的所有購物車會員列表
  if member_result == []:
    query3 = f"""
        INSERT INTO member_profile (會員_LINE_ID,會員信賴度_取貨率退貨率,加入時間,身分別)
        VALUES ( '{userid}','0.80', '{formatted_datetime}','消費者');
        """
    cursor.execute(query3)
    conn.commit()
  else:
    for row in member_result:
      memberlist = row[0]
      storagememberlist.append(memberlist)
    if userid not in storagememberlist:
      query3 = f"""
        INSERT INTO member_profile (會員_LINE_ID,會員信賴度_取貨率退貨率,加入時間,身分別)
        VALUES ( '{userid}','0.80', '{formatted_datetime}','消費者');
        """
      cursor.execute(query3)
      conn.commit()

  if Order_result == []:
    serial_number = '000001'
    query4 = f"""
          INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單狀態未取已取,訂單成立時間)
          VALUES ( 'cart{order_date}{str(serial_number)}','{userid}','add','dd' ,'{formatted_datetime}');
          """
    cursor.execute(query4)
    conn.commit()
  else:
    checkaddtime = Order_result[0][2]#取得最新一筆購物車序號
    for row1 in Order_result:
      cartlist = row1[1]
      storagecartlist.append(cartlist)
    if userid not in storagecartlist:#最新一筆購物車序號
      if checkaddtime[4:12] == formatted_date:
        serial_number = int(checkaddtime[12:])+1
      else:
        serial_number = '000001'
      query4 = f"""
        INSERT INTO Order_information (訂單編號,會員_LINE_ID,電話,訂單狀態未取已取,訂單成立時間)
        VALUES ( 'cart{order_date}{str(serial_number)}','{userid}','add','dd' ,'{formatted_datetime}');
        """
      cursor.execute(query4)
      conn.commit()
  cursor.close()
  conn.close()

#-------------------查詢預購商品列表----------------------
def preorder_list():
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = """
          SELECT 商品ID, 商品名稱, 現預購商品, 商品圖片, 商品簡介, 
                商品單位, 售出單價, 售出單價2, 預購數量限制_倍數, 
                預購截止時間 
          FROM Product_information 
          WHERE 現預購商品='預購';"""
  cursor.execute(query)
  result = cursor.fetchall()
  if result != []:
    listbuynow = result
  else:
    listbuynow = "找不到符合條件的資料。"
  cursor.close()
  conn.close()
  return listbuynow
#-------------------查詢現購商品列表----------------------
def buynow_list():
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = """
          SELECT 商品ID,商品名稱,現預購商品,商品圖片,商品簡介,
                  商品單位,售出單價,售出單價2,庫存數量 
          FROM Product_information 
          WHERE 現預購商品='現購' and 庫存數量>0;"""
  cursor.execute(query)
  result = cursor.fetchall()
  if result != []:
    listpreorder = result
  else:
    listpreorder = "找不到符合條件的資料。"
  cursor.close()
  conn.close()
  return listpreorder
#查詢資料SELECT
def test_datasearch():
  #測試讀取資料庫願望清單(所有)
  implement = databasetest()
  conn = implement['conn']
  cursor = implement['cursor']
  query = "SELECT * FROM wishlist;"
  cursor.execute(query)
  result = cursor.fetchall()
  if result is not None:
    testmsg = "願望清單讀取內容：\n"
    for row in result:
      # 透過欄位名稱獲取資料
      uid = row[0]#'UID'
      name = row[1]#'商品名稱'
      #商品圖片
      reason = row[3]#'推薦原因'
      time = row[4]#'願望建立時間'
      member = row[5]#'會員_LINE_ID'
      # 在這裡進行資料處理或其他操作
      testmsg += ('第%s筆\n推薦會員:\n%s\n商品名稱：\n%s\n推薦原因：\n%s\n願望建立時間：\n%s\n---\n' %(uid,member,name,reason,time))
  else:
    testmsg = "找不到符合條件的資料。"
  # 關閉游標與連線
  testmsg += "(end)"
  cursor.close()
  conn.close()
  return testmsg

#修改資料UPDATE
def test_dataUPDATE():
  return

#-------------------圖片取得並發送----------------------
def imagesent():
    implement = databasetest()  # 定義 databasetest() 函式並返回相關物件
    img = []
    send = []
    conn = implement['conn']
    cursor = implement['cursor']
    #query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 1 OFFSET 0;"#0開始1筆
    query = "SELECT 商品名稱, 商品圖片 FROM Product_information LIMIT 2 OFFSET 0;"
    cursor.execute(query)
    result = cursor.fetchall()
    
    if result != []:
        for row in result:
            productname = row[0] # 圖片商品名稱
            output_path = row[1] # 圖片連結
            # 發送圖片
            text_msg = TextSendMessage(text=productname)
            image_msg = ImageSendMessage(
                original_content_url=output_path,  # 圖片原圖
                preview_image_url=output_path  # 圖片縮圖
            )
            img.append(text_msg)
            img.append(image_msg)
    else:
        img.append(TextSendMessage(text='找不到符合條件的資料。'))
    
    # 關閉游標與連線
    cursor.close()
    conn.close()
    send = tuple(img)  # 將列表轉換為元組最多五個
    return send

#-------------------刪除images資料夾中所有----------------------
def delete_images():
    folder_path = 'images'  # 資料夾路徑
    file_list = os.listdir(folder_path)
    
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"已刪除圖片檔案：{file_path}")

#-------------------images資料夾中圖片轉連結----------------------
def imagetolink():
  imgurdata = imgurinfo()
  image_storage = []
  folder_path = 'images'# 設定資料夾路徑
  # 使用 glob 模組取得資料夾中的 JPG 和 PNG 圖片檔案
  image_files = glob.glob(f"{folder_path}/*.jpg") + glob.glob(f"{folder_path}/*.png")
  # 讀取所有圖片檔案
  for file in image_files:
    # 獲取檔案名稱及副檔名
    filename, file_extension = os.path.splitext(file)
    filename = filename+file_extension# 檔案位置加副檔名
    image_storage.append(filename)

  #執行轉換連結
  for img_path in image_storage:
    CLIENT_ID = imgurdata['CLIENT_ID_data']
    PATH = img_path #A Filepath to an image on your computer"
    title = img_path
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    #image = uploaded_image.title + "連結：" + uploaded_image.link
    imagetitle = uploaded_image.title
    imagelink = uploaded_image.link
    print( imagetitle + "連結：" + imagelink)
    #delete_images()#刪除images檔案圖片
  return {'imagetitle':imagetitle,'imagelink':imagelink}

