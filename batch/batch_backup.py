import os
import dropbox
from subprocess import Popen, PIPE
from dotenv import load_dotenv
import logging
import dj_database_url
from urllib.parse import urlparse

load_dotenv()

dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'))
IS_DOCKER = os.path.exists('/.dockerenv')
IS_HEROKU = os.getenv('DYNO') is not None

logging.basicConfig(
    filename='batch/batch_process.log',  # ログファイルの名前
    level=logging.INFO,            # ログレベルをINFOに設定
    format='%(asctime)s - %(levelname)s - %(message)s',  # ログのフォーマット
)

def create_mysql_backup(backupfile):
    """ JAWS sql server のデータをバックアップ"""
    try:
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
        
        dump_command = f"mysqldump -h {host} -u {user} -p{password} {database}"
        with open(backupfile, 'w') as f:
            process = Popen(dump_command.split(), stdout=f, stderr=PIPE)
            _, error = process.communicate()
            if process.returncode != 0:
                print(f"mysqldump failed: {error.decode()}")
                return False
        
        logging.info("Backup file created successfully.")  
        print("Backup file created successfully.")
        # print(f"Backup file created successfully.")
        return True
    except Exception as e:
        logging.info(f"Error during making MySQL backup file : {str(e)}")
        print(f"Error during making MySQL backup file : {str(e)}")
        # print(f"Error during making MySQL backup file : {str(e)}")
        return False
        

def upload_to_dropbox(file_path):
    """ 無料版では困難だったため使わない"""
    try:
        with open(file_path, 'rb') as f:
            # Dropboxにファイルをアップロード
            dbx.files_upload(f.read(), f'/{file_path}', mode=dropbox.files.WriteMode.overwrite)
        # print(f"File uploaded to Dropbox successfully.")
        logging.info(f"File uploaded to Dropbox successfully.")
        print(f"File uploaded to Dropbox successfully.")  


    except Exception as e:
        logging.info(f"Error during uploading to Dropbox:{str(e)}")  
        print(f"Error during uploading to Dropbox:{str(e)}") 
        # print(f"Error during making MySQL backup file : {str(e)}")

        
if __name__ == "__main__":
    BACKUP_FILE = 'backup.sql'
    create_mysql_backup(BACKUP_FILE)
    # if create_mysql_backup():
    #     upload_to_dropbox(BACKUP_FILE)
