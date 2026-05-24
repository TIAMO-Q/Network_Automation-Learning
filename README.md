# Network_Automation-Learning
> 记录我学习 python语言 网络自动化方向的代码、实验笔记和实战练习
> 目标是掌握 **Python 网络自动化**，能够利用 `paramiko`、`并发编程` 等技术批量管理华为网络设备

# 项目结构（及时更改）
network-automation-learning/
├── README.md # 项目说明（本文件）
├── requirements.txt # Python 依赖库列表
├── paramiko_basics/ # paramiko 基础练习
│ ├── ssh_login.py # SSH 登录单台设备
│ ├── exec_command.py # 执行单条命令
│ └── multi_device_backup.py # 批量备份配置（基础版）
├── concurrent/ # 并发编程
│ ├── threading_demo.py # 多线程并发备份
│ └── concurrent_futures.py # ThreadPoolExecutor 示例
├── netconf_yang/ # NETCONF / YANG 入门
│ └── get_capabilities.py # 获取设备能力集（示例）
├── notes/ # 学习笔记（Markdown）
│ ├── python_basics.md # Python 基础语法总结
│ ├── paramiko_notes.md # paramiko 使用要点
│ └── concurrency_notes.md # 并发编程核心概念
└── exams/ # 课程编程题练习（HCIE 考试题）
└── datacom_programming_exam.py # 真题模拟

# 技术栈

- 语言：Python 3.11
- 主要库：
  - `paramiko` – SSH 连接网络设备
  - `netmiko`（后续补充）– 简化多厂商设备管理
  - `concurrent.futures` / `threading` – 并发执行
  - `ncclient`（后续补充）– NETCONF 客户端
- 环境：华为 eNSP 模拟器走回环网卡 与 Pycharm 的远程连接

- # 学习目标

-  Python 基础（变量、循环、函数、类、异常）
-  `paramiko` 实现 SSH 登录并执行命令
-  多线程/协程并发管理多台设备
-  学习 `netmiko` 替代 `paramiko` 简化代码
-  掌握 `TextFSM` 解析设备输出
-  使用 `Jinja2` 批量生成配置模板
-  掌握 NETCONF / YANG 与华为设备交互

# 快速开始
1. 克隆仓库
   打开电脑的 终端（Windows 下可以是 CMD 或 PowerShell，macOS/Linux 下是 Terminal），然后输入：
   git clone https://github.com/TIAMO-Q/Network_Automation_Learning.git
   cd network-automation-learning
   如果不习惯用 git clone，也可以直接在 GitHub 网页上点击“Download ZIP”下载压缩包，解压后跳过 git clone 步骤，但后续安装依赖和运行脚本仍然需要终端。
2.安装依赖
  在项目文件夹内，执行：
  pip install -r requirements.txt/python -m pip install -r requirements.txt
3.配置设备信息
示例脚本中请替换为你的 eNSP 设备 IP 和凭证，这一步不需要终端，而是用记事本、VS Code 等编辑器打开脚本文件（例如 paramiko_basics/ssh_login.py），把里面的 IP、用户名、密码改成你自己的 eNSP 设备信息。保存后回到终端
4.运行示例
在项目根目录下执行：
python paramiko_basics/ssh_login.py
























