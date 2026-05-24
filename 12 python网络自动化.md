# 网络自动化相关模块
### 1. paramiko基础
```python
# 两种方式打开SSH会话通道
# 1.transport
# 2.SSHclient(集成了transport)

# 默认使用账号密码进行用户认证时，需要先获取服务器的公钥
# 服务器将公钥发送给客户端时，客户端默认不会立即接收该公钥
# 而set_missing_host_key_policy(paramiko.AutoAddPolicy())的作用就是让我们可以不输入yes or no的情况下自动把公钥保存在本地

import time
import paramiko

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname="192.168.100.1", port=22, username="python", password="Huawei@123")
vty = ssh_client.invoke_shell()
res = vty.recv(99999).decode("utf-8")
print(res)
vty.send("N\n")
time.sleep(0.5)
res = vty.recv(99999).decode("utf-8")
print(res)
vty.send("screen-length 0\n")
time.sleep(0.5)
vty.send("dis cu\n")
time.sleep(1)
res = vty.recv(99999).decode("utf-8")
print(res)
```

### 2.SFTP基础
> 建立sftp连接/刷脚本
>

```python
#sftp.txt
# sftp server enable
# ssh user python service-type stelnet sftp
# ssh user python sftp-directory cfcard:
# ssh authorization-type default root
# 两种方式打开SSH会话通道
# 1.transport
# 2.SSHclient(集成了transport)

# 默认使用账号密码进行用户认证时，需要先获取服务器的公钥
# 服务器将公钥发送给客户端时，客户端默认不会立即接收该公钥
# 而set_missing_host_key_policy(paramiko.AutoAddPolicy())的作用就是让我们可以不输入yes or no的情况下自动把公钥保存在本地

import time
# from uu import encode
import paramiko


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
```

```python
1.第一种方式
# 2. 使用transport打开SSH会话通道

tran = paramiko.Transport(("192.168.100.1", 22))
tran.connect(username="python", password="Huawei@123")
sftp = paramiko.SFTPClient.from_transport(tran)  # 从SSH会话的通道中建立sftp会话的通道
sftp.get("/vrpcfg.cfg", r"E:\devops\pythonProject\CE1.cfg")
sftp.put(r"E:\devops\pythonProject\CE1.cfg", "/TEST.cfg")

# 在执行sftp get下载时，如果下载后的名称相同，后面下载的文件会将前面下载的文件覆盖掉

# cfcard:/vrpcfg.cfg

# 注意：在写路径时不要敲额外的字符，否则会报文件不存在的错误

2.第二种方式
def transport():
    ssh_session = paramiko.SSHClient()
    # 在使用口令认证进行ssh连接时，客户端会先向请求服务端的公钥，这一条命令的作用就是
    # 让我们在不输入yes/no的情况下将服务端的公钥保存在本地
    ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_session.connect(hostname="192.168.100.1",port=22,username="python",password="Huawei@123")
    # 在ssh会话通道的基础上，打开命令行交互的通道
    return ssh_session
def download():
    tran = transport()
    res = tran.get_transport()
    sftp = paramiko.SFTPClient.from_transport(res)
    # get方法，将远程的文件下载到本地：remotepath localpath
    remote = "/vrpcfg.cfg"
    local = r"E:\devops\Phase 2\project\自动化编程\自动化相关模块\CE2.txt"
    # sftp.get(remote,local)
    remote_put = "CE1.cfg"
    # sftp.put(local,remote_put)
    sftp.get(remote,local)
    sftp.close()
```



### 3. 补充 OS模块
```python
import os

path_dirs = "files"
if not os.path.exists(path_dirs):
    os.makedirs(path_dirs)

# path = os.path.abspath(__file__)  # 获取当前py文件的绝对路径
# root_path = os.path.dirname(path)  # 获取path路径的上一级目录
# new_path = os.path.join(root_path, "files")  
# 实现路径的拼接,将root_path 与 files进行路径的拼接


path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
print(path)
-------------------------------------------------
import os

# 1.使用os模块来获取当前执行文件的绝对路径
v1 = os.path.abspath(__file__)

# 2. 使用os模块来获取上一级的目录
v2 = os.path.dirname(v1)

# 3. 使用os模块完成路径的拼接
v3 = os.path.join(v2,"CE1.txt")
print(v3)

# 因此，本地路径可以写成这样的形式
local =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"CE1.txt")
```



+ 利用os模块自动获取当前路径，以及使用datetime模块修改文件名称

```python
import os
from datetime import datetime

path_dirs = "files"
if not os.path.exists(path_dirs):
    os.makedirs(path_dirs)

# path = os.path.abspath(__file__)  # 获取当前py文件的绝对路径
# root_path = os.path.dirname(path)  # 获取path路径的上一级目录
# new_path = os.path.join(root_path, "files")  # 实现路径的拼接,将root_path 与 files进行路径的拼接
time_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", time_now + "-CE1.cfg")


tran = paramiko.Transport(("192.168.100.1", 22))
tran.connect(username="python", password="Huawei@123")
sftp = paramiko.SFTPClient.from_transport(tran)  # 从SSH会话的通道中建立sftp会话的通道
sftp.get("/vrpcfg.cfg", path)
# sftp.put(r"E:\devops\pythonProject\CE1.cfg", "/TEST.cfg")
```



### 4. 批量配置
```python
import os
import time
from datetime import datetime
import paramiko


def ssh_connect(ip, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, port=port, username=username, password=password)
    return ssh_client


def ssh_config(ip, port, username, password, file):
    ssh_client = ssh_connect(ip, port, username, password)
    vty = ssh_client.invoke_shell()
    vty.send("N\n")
    time.sleep(0.5)
    vty.send("system-view im \n")
    time.sleep(0.5)
    with open(file, "r", encoding="utf-8") as f:
        for i in f.readlines():
            vty.send(i)
            time.sleep(0.5)
    return vty.recv(65535).decode("utf-8")


# data_list = ["192.168.100.{}".format(i) for i in range(1, 4)]
def run(num):
    data_list = [{f"CE{i}": {"ip": f"192.168.100.{i}", "port": 22, "username": "python", "password": "Huawei@123"}} for
                 i in
                 range(1, 4)]
    for i in data_list:
        res = ssh_config(i[f"CE{num}"]["ip"], 22, "python", "Huawei@123", "sftp.txt")
        print(res)
        num += 1


run(num=1)
```

```python
import os
import time
from datetime import datetime
import paramiko


def ssh_connect(ip, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip, port=port, username=username, password=password)
    return ssh_client


def ssh_config(ip, port, username, password, file):
    ssh_client = ssh_connect(ip, port, username, password)
    vty = ssh_client.invoke_shell()
    vty.send("N\n")
    time.sleep(0.5)
    vty.send("system-view im \n")
    time.sleep(0.5)
    with open(file, "r", encoding="utf-8") as f:
        for i in f.readlines():
            vty.send(i)
            time.sleep(0.5)
    return vty.recv(65535).decode("utf-8")


def download(ip, port, username, password, sysname):
    time_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", time_now + f"-{sysname}.cfg")
    tran = paramiko.Transport((ip, port))
    tran.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(tran)
    sftp.get("/vrpcfg.cfg", path)


# data_list = ["192.168.100.{}".format(i) for i in range(1, 4)]
# def run(num):
#     data_list = [{f"CE{i}": {"ip": f"192.168.100.{i}", "port": 22, "username": "python", "password": "Huawei@123"}} for
#                  i in
#                  range(1, 4)]
#     for i in data_list:
#         res = ssh_config(i[f"CE{num}"]["ip"], 22, "python", "Huawei@123", "sftp.txt")
#         print(res)
#         num += 1


data_list = [{"ip": f"192.168.100.{i}", "sysname": f"CE{i}", "username": "python", "password": "Huawei@123"} for i in
             range(1, 4)]
for i in data_list:
    download(ip=i["ip"], port=22, sysname=i["sysname"], username=i["username"], password=i["password"])
```



### 5.paramiko进阶
+ 第一期

```python
# 1. 在使用paramiko进行ssh登录时，可能会存在网络或者设备故障的问题
# 2. 如何判断设备登录成功
# 3. 如何保证回显完毕
# 4. 如何判断进入了系统视图
# 5. 如何判断命令执行成功
# 6. 命令执行成功之后，如何判断正确的返回了用户视图
import re
import time

import paramiko


class LoginError(Exception):
    def __init__(self, ip):
        self.ip = ip

    def __str__(self):
        return f"{self.ip}链接失败"


class GetMarkError(Exception):
    def __str__(self):
        return "GetMarkError"


class SSH:
    def __init__(self, ip: str, port: int, username: str, password: str) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.session = None
        self.vty = None
        self.login = False
        self.config = False
        self.old_mark = None

    def transport(self) -> None:
        ssh_session = paramiko.SSHClient()
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_session.connect(hostname=self.ip, port=self.port, username=self.username, password=self.password)
        self.session = ssh_session

    def open_vty(self) -> None:
        self.vty = self.session.invoke_shell()

    def get_mark(self, output: str) -> None:
        pat = re.compile("<.+?>")  # 创建一个正则表达式的对象
        res = pat.findall(output)
        if res.__len__() != 1:
            raise GetMarkError
        else:
            self.mark = self.old_mark = res[0]

    def login_device(self) -> None:
        try:
            self.transport()
            self.open_vty()
        except Exception:
            raise LoginError(self.ip)
        time.sleep(1)
        output = self.vty.recv(65535).decode("utf-8")
        self.get_mark(output)
        self.login = True

    def recv_result(self, nbytes, interval=1):
        pat = re.compile(self.mark)
        ret = ""
        while True:
            res = self.vty.recv(nbytes).decode("utf-8")
            # print(res)
            ret += res
            if not pat.search(res):
                self.vty.send(" ")
                time.sleep(interval)
                continue
            else:
                break
        return ret

    def test_command(self, command: str) -> str:
        if not self.login:
            self.login_device()
        self.vty.send(command + "\n")
        res = self.recv_result(65535)
        return res

    def config_mode(self):
        if not self.login:
            self.login_device()
        self.mark = "\[.+?\]"
        self.test_command("system-view")
        self.config = True

    def exit(self):
        self.mark = self.old_mark
        return self.test_command("return")

    def send_command(self, command: list):
        if not self.config:
            self.config_mode()
        ret = ""
        for i in command:
            res = self.test_command(i)
            ret += res
        ret += self.test_command("commit")
        ret += self.exit()
        return 


if __name__ == "__main__":
    ssh_client = SSH(ip="192.168.100.1", port=22, username="python", password="Admin@123")
    res = ssh_client.send_command(["interface GE1/0/0", "des ytedu"])
    print(res)
```

+ 第二期

```python
# 1. 在使用paramiko进行ssh登录时，可能会存在网络或者设备故障的问题
# 2. 如何判断设备登录成功
# 3. 如何保证回显完毕
# 4. 如何判断进入了系统视图
# 5. 如何判断命令执行成功
# 6. 命令执行成功之后，如何判断正确的返回了用户视图
import re
import time

import paramiko


class LoginError:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def __str__(self) -> str:
        return f"{self.ip} Login Error"


class GetMarkError:
    def __init__(self, ip: str) -> None:
        self.ip = ip

    def __str__(self) -> str:
        return f"{self.ip} GetMarkError"


class SSH:
    # 初始化方法
    def __init__(self, ip: str, port: int, username: str, password: str) -> None:
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.ssh_session = None
        self.vty = None
        self.login = False
        self.config = False

    def transport(self) -> None:
        # 创建SSH会话，并设置SSH会话的标识符
        ssh_session = paramiko.SSHClient()
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_session.connect(hostname=self.ip, port=self.port, username=self.username,
                            password=self.password)
        self.ssh_session = ssh_session

    def open_vty(self) -> None:
        # 基于SSH会话建立命令行交互的会话，并设置标识符
        if not self.ssh_session:
            self.transport()
        self.vty = self.ssh_session.invoke_shell()

    def get_mark(self, arg: str):
        # 创建正则对象，匹配<设备名称>，如果匹配到说明登录成功，没有匹配到说明登陆失败，抛出异常
        # 设置mark标识符，此时代表是设备名称
        pat = re.compile('<.+?>')
        res = pat.findall(arg)
        if res.__len__() == 1:
            self.mark = self.old_mark = res[0]
            # print(self.mark)
        else:
            raise GetMarkError(self.ip)

    def login_device(self) -> None:
        # 创建设备登录的方法，并判断登录是否成功
        try:
            self.transport()
            self.open_vty()
        except Exception:
            raise LoginError(self.ip)
        time.sleep(1)
        content = self.vty.recv(99999).decode("utf-8")
        # 将回显信息传入get_mark函数进行判断登录是否成功
        self.get_mark(content)
        self.login = True

    def recv_result(self) -> str:
        # 创建正则对象，匹配<设备名称>，如果匹配到说明回显完整，没有匹配到说明回显不完整，继续敲空格
        # 将完整的回显返回出来
        pat = re.compile(self.mark)
        ret = ""
        while True:
            time.sleep(1)
            content = self.vty.recv(99999).decode("utf-8")
            print(content)
            ret += content
            if pat.search(content):
                break
            self.vty.send(" ")
        return ret

    def send_command(self, command: str) -> str:
        # 创建一个执行命令的方法，并调用recv_result()判断回显是否完整，并接收返回出的完整回显
        if not self.login:
            self.login_device()
        self.vty.send(command + "\n")
        res = self.recv_result()
        return res

    def config_mode(self):
        # 创建一个进入系统视图的方法，并修改mark标识符匹配[~设备名]，如果匹配到说明成功进入系统视图
        if not self.login:
            self.login_device()
        self.mark = "\[.+?\]"
        self.send_command("system-view")
        self.config = True

    def exit(self):
        # 创建一个返回用户视图的方法，修改mark标识符为<设备名称>，如果能匹配到则表明回到了用户视图
        self.mark = self.old_mark
        return self.send_command("return")

    def config_command(self, command: list):
        # 创建一个执行命令的方法，执行完每一条命令都将结果拼接在ret变量中，最终返回完整的回显
        if not self.config:
            self.config_mode()
        ret = ""
        for i in command:
            ret += self.send_command(i)
        ret += self.send_command("commit")
        ret += self.exit()
        return ret


if __name__ == '__main__':
    a = SSH(ip="192.168.100.1", port=22, username="python", password="Admin@123")
    res = a.config_command(["interface G1/0/0", "des ytedu"])
    print(res)
```



### 6.pysnmp
```python
g = getCmd(SnmpEngine(),
           UsmUserData(userName="admin", authKey="Huawei@123", privKey="Huawei@123",
                       authProtocol=usmHMACSHAAuthProtocol, 
                       privProtocol=usmAesCfb128Protocol),
           UdpTransportTarget(("192.168.100.1", 161)),
           ContextData(),
           ObjectType(ObjectIdentity("1.3.6.1.2.1.1.5.0")))
errorIndication, errorStatus, errorIndex, varBinds =next(g)
for i in varBinds:
    print(str(i).split("=")[1].strip())
```

+ 通过pysnmp获取设备名称，然后进行配置文件的下载

```python
def download(name):
    tran = paramiko.Transport(('192.168.100.1', 22))
    tran.connect(username="python",password="Huawei@123")
    sftp = paramiko.SFTPClient.from_transport(tran)
    # get方法，将远程的文件下载到本地：remotepath localpath
    now = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+f"_{name}"
    remote = "/vrpcfg.cfg"

    local = os.path.join(os.path.dirname(os.path.abspath(__file__)),now)
    remote_put = "CE1.cfg"
    # sftp.put(local,remote_put)
    sftp.get(remote,local)
    sftp.close()

def snmp():
    get = getCmd(SnmpEngine(),
                 UsmUserData(userName="admin",
                             authKey="Huawei@123",
                             privKey="Huawei@123",
                             authProtocol=usmHMACSHAAuthProtocol,
                             privProtocol=usmAesCfb128Protocol),
                 UdpTransportTarget(("192.168.100.1",161)),
                                    ContextData(),
                             ObjectType(ObjectIdentity('1.3.6.1.2.1.1.5.0')))
    a, b, c, d = next(get)
    for i in d:
        res = str(i).split("=")[1].strip()
    return res

if __name__ == '__main__':
    arg = snmp()
    download(arg)
```
