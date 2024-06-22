import os
import time
from ftplib import FTP

# Configurações do FTP
FTP_SERVER = 'ftpupload.net'
FTP_USER = 'if0_36724093'
FTP_PASSWORD = 'abSCSpqguEz'
FTP_DIR = '/private/anime'

# Diretório local para monitorar
LOCAL_DIR = '/animes/'

def upload_file(ftp, local_file_path, remote_file_path):
    with open(local_file_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_file_path}', file)
    print(f'Arquivo {local_file_path} enviado para {remote_file_path}.')

def sync_files():
    uploaded_files = set()

    while True:
        ftp = FTP(FTP_SERVER)
        ftp.login(FTP_USER, FTP_PASSWORD)
        ftp.cwd(FTP_DIR)
        
        for filename in os.listdir(LOCAL_DIR):
            local_file_path = os.path.join(LOCAL_DIR, filename)
            if os.path.isfile(local_file_path) and filename not in uploaded_files:
                upload_file(ftp, local_file_path, filename)
                uploaded_files.add(filename)
        
        ftp.quit()
        time.sleep(10)  # Espera 10 segundos antes de verificar novamente

if __name__ == "__main__":
    sync_files()
