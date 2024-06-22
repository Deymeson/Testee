import os
import time
from ftplib import FTP
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configurações do FTP
FTP_SERVER = 'ftpupload.net'
FTP_USER = 'if0_36724093'
FTP_PASSWORD = 'abSCSpqguEz'
FTP_DIR = '/private/anime'

# Diretório local para monitorar
LOCAL_DIR = '/animes/'

class FTPUploader:
    def __init__(self, server, user, password, remote_dir):
        self.server = server
        self.user = user
        self.password = password
        self.remote_dir = remote_dir

    def upload_file(self, local_file_path, remote_file_path):
        with FTP(self.server) as ftp:
            ftp.login(self.user, self.password)
            ftp.cwd(self.remote_dir)
            with open(local_file_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_file_path}', file)
            print(f'Arquivo {local_file_path} enviado para {remote_file_path}.')

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, uploader):
        self.uploader = uploader

    def on_created(self, event):
        if event.is_directory:
            return
        local_path = event.src_path
        remote_path = os.path.basename(local_path)
        self.uploader.upload_file(local_path, remote_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        local_path = event.src_path
        remote_path = os.path.basename(local_path)
        self.uploader.upload_file(local_path, remote_path)

def main():
    uploader = FTPUploader(FTP_SERVER, FTP_USER, FTP_PASSWORD, FTP_DIR)
    event_handler = ChangeHandler(uploader)
    observer = Observer()
    observer.schedule(event_handler, LOCAL_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()