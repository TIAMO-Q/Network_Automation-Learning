import time
# from uu import encode

import paramiko

# 两种方式打开SSH会话通道
# 1.transport
# 2.SSHclient(集成了transport)

# 默认使用账号密码进行用户认证时，需要先获取服务器的公钥
# 服务器将公钥发送给客户端时，客户端默认不会立即接收该公钥
# 而set_missing_host_key_policy(paramiko.AutoAddPolicy())的作用就是让我们可以不输入yes or no的情况下自动把公钥保存在本地
def transport():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname="16.0.0.5", port=22, username="python", password="Huawei@123")
    return ssh_client
def ssh_config():
    with open("sftp.txt", 'r',encoding= "utf-8" )as f:
        res = f.readlines()
    ssh_client = transport()
    vty = ssh_client.invoke_shell()
    vty.send("N\n")
    time.sleep(0.5)
    print(res)
    vty.send("sys\n")
    time.sleep(0.5)
    for i in res:
        vty.send(i)
        time.sleep(0.5)
        vty.send("com\n")
        res = vty.recv(99999).decode("utf-8")
        print(res)

    vty.send("screen-length 0\n")
    vty.send("com\n")
    time.sleep(0.5)
    vty.send("dis cu\n")
    time.sleep(1)
    res = vty.recv(99999).decode("utf-8")
    print(res)

if __name__ == '__main__':
    ssh_config()
