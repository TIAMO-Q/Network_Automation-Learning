# NETCONF与YANG编程
### 1. 实现自动化必要的趋势
#### 1.1 缩短部署时间
```python
自动化可以帮助减少部署时间。可编程性有助于快速验证新的功能、部署新的服务并且立即升级路由器。这要求网络设备具有一致和完整的应用编程接口(API)，最终目标是使网络运维工作中所有可以自动化的工作全部自动化。
```



#### 1.2 CLI无法作为标准
```python
虽然CLI不是API，但不幸的是不得不将其视为一个API，因为必须长期依赖它。然而，使用CLI进行自动化既不可靠，也不具有成本效益。
首先，许多与服务相关的配置更改会涉及一个以上的设备，配置更改变得越来越复杂
其次，虽然CLI是人性化的，但却不适合自动化，原因如下：
1.CLI没有标准化。虽然网络设备配置CLI是相似的，但从语法和语义的角度来看，不同厂商或特定厂商的操作系统并不一致。
2.通过CLI配置设备时存在依赖性问题。某些情况下，配置VLAN之前必须输入用于配置接口的CLI命令。如果这些步骤未按正确的顺序执行，则配置失败，或者更糟糕的是，配置仅部分完成
3.CLI只提供有限的错误报告，还不能以易于使用的脚本格方式报告错误
4.CLI不产生任何结构化的输出。因此，从display命令中提取信息的唯一方法是通过“屏幕抓取”，或使用正则表达式模式匹配从输出中提取数据。最后，"display命令"经常更改以显示更多功能、更多计数器等。问题是即使对display命令
进行更小的更改（例如在输出中添加空格）也可能会破坏对于特定值的提取
5.必须清楚设备的特征，例如用telnet登录必须匹配到某段字符串，然而你在真正了解此型号的设备之前，是无法预知会出现怎样的显示信息的
6.依赖命令行限制了网络的发展，例如害怕升级设备会导致自动化脚本的中断，所以推迟或不去部署必要的安全补丁。而这种升级的恐惧也解释了以数据模型来作为驱动的自动化速度很缓慢
```



#### 1.3  硬件与软件的解耦
```python
行业越来越倾向于将软件和硬件进行分离，最终目标是将白盒组装成统一的硬件，以Linux为操作系统，并针对不同网络功能使用特定的应用程序---可能从一个供应商购买BGP功能，从另一个供应商购买OSPF协议，再从第三个供应商购买RADIUS和管理功能。这样做的优势显而易见：
1.全部使用Linux模糊了服务器和网络管理之间的界限，并降低了支持成本。不仅“路由器”和“交换机”都在Linux上运行，Linux环境还提供了许多工具和应用程序，包括管理操作
2.使用Linux意味着更广泛的共识：人们直接从学校开始接受更好的培训。在硬件商品化的情况下联网不再困难，因为厂商的CLI不是唯一的。换句话说，不同的设备厂商在CLI方面不再竞争。更多的不再需要专门懂某个厂商设备的人，而转向具有linux和脚本技能的人选。因此，高级网络工程师应该少关注厂商的具体内容，多关注更广泛的网络架构和技术基础。而对于厂商来说，除了关注认证以及部分基于CLI的知识，还应该更加关注独立于CLI之外的网络编程和操作方面的内容
3.在网络中使用相同的硬件，而不是特殊的专用硬件，可以降低网络的复杂性（缺点是硬件bug会影响到所有平台）
4.网络和服务工程师可以专注于面向业务的任务，而不仅仅是网络运营和维护。网络开始成为业务的推动者，而业务和网络之间的链接正是软件。随着自动化所节约的时间，工程师将成为推动网络创新以满足业务需求的关键推动力
```



#### 1.4 数据模型驱动的管理
```python
良好的脚本需要基于良好的API
1.可编程API应该抽象化底层实现的复杂性。Devops工程师不需要知道不必要的详细信息，例如网元的特定配置顺序，或者在发生故障时需要采取的具体步骤。如果上述信息对人类来说不直观，那么配置引擎的命令排序就会更加复杂。配置的功能应该更像是填写高级检查清单（这些是你需要的设置；现在系统可以确定如何正确分组和排序）
2.API关键工作（无论是软件API还是网络API）是为数据提供规格。首先，它回答了数据是什么的问题----整数、字符串或其他类型的值？接下来，它指定了该数据的组织方式。在传统编程中这被称为数据结构，在网络可编程性和数据库的世界中更常见的术语是架构，也称为数据模型
3.访问数据的方法：API需要为如何读取和操作数据提供标准化的框架
4.将API应用于复杂的环境时，关键是供应商以基于标准的方式实施API。不同设备和供应商之间定义和访问数据应该有一种通用方法，运维人员不必为网络中的每个不同设备和功能学习单独的专有接口
```



案例1：使用netconf配置日志主机位

```python
from ncclient.xml_ import to_ele


# ncclient  模块  很多东西都补全不了

def netconf():
    return manager.connect(host="192.168.100.1",
                           port=830,
                           username="netconf",
                           password="Huawei12#$",
                           look_for_keys=False,
                           allow_agent=False,
                           hostkey_verify=False,
                           device_params={"name": "huawei"})


if __name__ == '__main__':
    CONFIG = """
    <edit-config>
    <target>
      <running/>
    </target>
    <default-operation>merge</default-operation>
    <error-option>rollback-on-error</error-option>
    <config>
      <syslog xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <syslogServers>
          <syslogServer operation="merge">
            <ipType>ipv4</ipType>
            <serverIp>10.1.60.2</serverIp>
            <isDefaultVpn>false</isDefaultVpn>
            <vrfName>_public_</vrfName>
            <timestamp>UTC</timestamp>
            <transportMode>tcp</transportMode>
          </syslogServer>
        </syslogServers>
      </syslog>
    </config>
  </edit-config>
    """
    try:
        m = netconf()
        # 将字符串转换成XML文件对象
        content = to_ele(CONFIG)
        res = m.rpc(content)
        if "<ok/>" in str(res):
            print("execute successfully")
        else:
            print("execute fail")
    except Exception as e:
        print(e)
```

+ 使用Netconf查询日志主机位

```python
from ncclient import manager
from ncclient.xml_ import to_ele


# ncclient  模块  很多东西都补全不了

def netconf():
    return manager.connect(host="192.168.100.1",
                           port=830,
                           username="netconf",
                           password="Huawei12#$",
                           look_for_keys=False,
                           allow_agent=False,
                           hostkey_verify=False,
                           device_params={"name": "huawei"})


if __name__ == '__main__':
    CONFIG = """
  <get>
    <filter type="subtree">
      <syslog xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
        <syslogServers>
          <syslogServer>
            <ipType></ipType>
            <serverIp></serverIp>
            <isDefaultVpn></isDefaultVpn>
            <vrfName></vrfName>
            <timestamp></timestamp>
            <transportMode></transportMode>
            <sslPolicyName></sslPolicyName>
            <isBriefFmt></isBriefFmt>
          </syslogServer>
        </syslogServers>
      </syslog>
    </filter>
  </get>
    """
    # try:
    m = netconf()
    # 将字符串转换成XML文件对象
    content = to_ele(CONFIG)
    res = m.rpc(content)
    print(res)
    m.close()
```
