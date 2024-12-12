import mysql.connector
import os
import logging
import django
from pathlib import Path
from dotenv import load_dotenv
from datetime import date,timedelta
from urllib.parse import urlparse

# load_dotenv()
# IS_DOCKER = os.path.exists('/.dockerenv')
# IS_HEROKU = os.getenv('DYNO') is not None

logging.basicConfig(
    filename='batch/batch_process.log',  # ログファイルの名前
    level=logging.INFO,            # ログレベルをINFOに設定
    format='%(asctime)s - %(levelname)s - %(message)s',  # ログのフォーマット
)

# MySQLに接続してデータを取得
def image_update_mysql(tbl):
    
    load_dotenv()
    IS_DOCKER = os.path.exists('/.dockerenv')
    IS_HEROKU = os.getenv('DYNO') is not None
    
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
        query1 = f"""SELECT word FROM  {tbl} WHERE img = 'images/default.webp'"""
                
        cursor.execute(query1)
        records = cursor.fetchall()
        
        for row in records:
            default_list.append(row[0])
        print(len(default_list))
            
        for wd in default_list:
            query2 = f"""UPDATE {tbl} SET img = 'images/{wd}.webp' WHERE word = '{wd}'"""
            cursor.execute(query2)

        # nullを変更
        null_list = []
        query3 = f"""SELECT word FROM  {tbl} WHERE img IS NULL"""
                
        cursor.execute(query3)
        records = cursor.fetchall()

        for row in records:
            null_list.append(row[0])
        print(len(null_list))
            
        for wd in null_list:
            query4 = f"""UPDATE {tbl} SET img = 'images/{wd}.webp' WHERE word = '{wd}'"""
            cursor.execute(query4)


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
            
    # return word_list

# メイン処理
if __name__ == '__main__':
    tbl = os.getenv('BATCH_CHECK_TABLE')
    tbl = 'wlist_wordsmodel'
    # username="12"

    image_update_mysql(tbl)