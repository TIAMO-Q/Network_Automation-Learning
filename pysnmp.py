#通过pysnmp获取设备名称，然后进行配置文件的下载
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
