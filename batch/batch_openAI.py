import os
from openai import OpenAI
import requests

from PIL import Image
import os

import mysql.connector
import os
import logging
import django
from pathlib import Path
from dotenv import load_dotenv
from datetime import date,timedelta
from urllib.parse import urlparse

# 0. ---------ではなく、default.imgとなるwordのリストを取得。  
# 1．リストの全要素において、
# ・フィールド名をdefault.imgから　***.imgに変更。
# ・open AIでimage generateし、media/images0に保存。
# ・画像圧縮し、media/imagesに保存。
# ・media/images0のデータを削除。

logging.basicConfig(
    filename='batch/batch_process.log',  # ログファイルの名前
    level=logging.INFO,            # ログレベルをINFOに設定
    format='%(asctime)s - %(levelname)s - %(message)s',  # ログのフォーマット
)

load_dotenv()
IS_DOCKER = os.path.exists('/.dockerenv')
IS_HEROKU = os.getenv('DYNO') is not None

def get_defaultList(tbl,UPDATE=False):
    
    # output_folder = "media/images"
    # files = os.listdir(output_folder)
    
    try:
        # MySQLに接続
        host='db' if IS_DOCKER and IS_HEROKU else os.getenv('DB_HOST')
        user=os.getenv('DB_USER')
        password=os.getenv('DB_PASSWORD')
        database=os.getenv('DB_NAME')

        DATABASE_URL = os.getenv('JAWSDB_URL')
        if DATABASE_URL:
            url = urlparse(DATABASE_URL)
            host = url.hostname       
            user = url.username       
            password = url.password   
            database = url.path[1:]
  
        conn = mysql.connector.connect(host=host,user=user,
                                       password=password,database=database)      
        cursor = conn.cursor()
        
        # default.webpを変更
        default_list = []
        query1 = f"""SELECT word FROM  {tbl} WHERE img = 'images/default.webp'
        AND mean2 !='-----------------------------'"""
                
        cursor.execute(query1)
        records = cursor.fetchall()
        
        for row in records:
            default_list.append(row[0])
        print(len(default_list))
        
        if UPDATE:
            for wd in default_list:
                query2 = f"""UPDATE {tbl} SET img = 'images/{wd}.webp' WHERE word = '{wd}'"""
                cursor.execute(query2)
            
        conn.commit()
        logging.info("img field update")
    
    except mysql.connector.Error as err:
        conn.rollback()  # ロールバック
        logging.error(f"MySQLエラーが発生しました: {err}")
        print(f"MySQLエラーが発生しました: {err}")
    
    except Exception as e:
        conn.rollback()  # ロールバック
        logging.error(f"予期しないエラーが発生しました: {e}")
        print(f"予期しないエラーが発生しました: {e}")
    
    except Exception as e:
        conn.rollback()  # ロールバック
        logging.error(f"予期しないエラーが発生しました: {e}")
        print(f"予期しないエラーが発生しました: {e}")
    
    finally:
        # カーソルと接続をクローズ
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    return default_list


def resize_and_compress_image(input_path, output_path, new_size=(512, 512), quality=85):
    """
    画像をリサイズして圧縮する
    """
    with Image.open(input_path) as img:
        img = img.resize(new_size, Image.LANCZOS)  # リサイズ
        img.save(output_path, format='WEBP', optimize=True, quality=quality)



def image_generate(default_list):
    
    output_folder0 = '/tmp'  # 圧縮前の画像を保存するフォルダ
    output_folder  = 'media/images'   # 圧縮後の画像を保存するフォルダ
    os.makedirs(output_folder0, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # if not os.path.exists(output_folder):
    #     os.mkdir(output_folder)

    # for i in range(len(word_list)):
    for i in range(len(default_list)):
        
        output_filename = f"{default_list[i]}.webp"
        file_path0 = os.path.join(output_folder0, output_filename)
        file_path  = os.path.join(output_folder,  output_filename)
        
        if not os.path.exists(file_path):
                            
            prompt_template = os.getenv('WORD_PROMPT')
            prompt = prompt_template.format(word=default_list[i])
            print(prompt)
            
            client = OpenAI(api_key=os.getenv('OPEN_AI_KEY'))

            try:
                # OpenAI APIを使用して画像を生成
                response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
                )

                image_url = response.data[0].url
                
                # 画像をダウンロードしてimages0に保存。
                img_data = requests.get(image_url).content
                with open(file_path0, 'wb') as handler:
                    handler.write(img_data)
                
                print(f"画像がimages0に保存されました: {file_path0}")            

            except Exception as e:
                print(f"エラーが発生しました: {e}")
            
        # images0に保存した画像を圧縮しimages処理。
            resize_and_compress_image(file_path0, file_path)
            
            # if os.path.isfile(file_path0):
            #     os.remove(file_path0)
            
            print(f'{output_filename} has been resized,compressed,deleted.')
        

            
# メイン処理
if __name__ == '__main__':
    tbl = os.getenv('BATCH_CHECK_TABLE')
    
    default_list = get_defaultList(tbl,UPDATE=True)
    image_generate(default_list)
    
    print(default_list)
    
    ## images0を削除
