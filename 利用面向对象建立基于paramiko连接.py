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
