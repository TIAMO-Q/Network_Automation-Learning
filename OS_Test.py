import os
from datetime import datetime
import paramiko

path_dirs = "files"
if not os.path.exists(path_dirs):
    os.makedirs(path_dirs)


time1 = datetime.now().strftime('%Y-%m-%d')
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"files",time1 +"CE1.txt")
remote = r"1.cfg"
ssh = paramiko.Transport("16.0.0.91",22)
ssh.connect(username="python", password="Huawei@123")
sftp = paramiko.SFTPClient.from_transport(ssh)
sftp.get(remote,path)

