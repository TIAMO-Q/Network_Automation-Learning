# SSH原理与实践
### 1 SSH简介
+ SSH（Secure Shell，安全外壳协议）是一种用于在不安全网络上进行安全远程登录和实现其他安全网络服务的协议。
+ SSH协议由三个组件构成：SSH传输层协议，SSH用户认证协议，SSH连接协议。
    - SSH传输层协议：版本协商、算法协商、密钥交换
    - SSH用户认证协议：用户认证（口令、密钥）
    - SSH连接协议：建立会话连接

### 2 密码学补充
#### 2.1 对称加密和非对称加密
+ 对称加密 ：加密和解密使用的是同一把密钥
    - 优点：加密速度快
    - 缺点：不安全，密钥在传输过程当中存在安全风险

<img src="SSH原理与实践.assets/image-20220617145822207.png" title="null" crop="0,0,1,1" id="Gm5BL" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267614341-b6aeae3d-87eb-4d13-a298-881776cae2e6.png" width="966" title="" crop="0,0,1,1" id="u1570ceec" class="ne-image">

+ 非对称加密：每一方拥有两把钥匙，一把叫做公钥，一把叫私钥：公钥加密，私钥解密；私钥加密，公钥解密
    - 优点：安全，私钥是保存在本地的，也就意味着，即便密文被获取到，也无法进行解密
    - 缺点：加密速度慢。虽然攻击者无法通过密文得到明文信息，但是可以篡改信息

<img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267636476-c647c4de-e24c-47bf-b8af-bc643d732cd1.png" width="1015.3333333333334" title="" crop="0,0,1,1" id="u1b59f40e" class="ne-image">

```python
如何获取对方的公钥：
1.发起请求来获取
2.可以将自己的公钥放在一台公共的服务器上
```

#### 2.2 数字信封
+ 核心概念：对于明文还是采用对称加密的方式，而对于对称加密的密钥，采用非对称加密的方式
+ 优点：在保证安全性的前提下，又提升了加密的速度
+ 缺点：虽然攻击者无法通过密文得到明文信息，但是可以篡改信息

<img src="SSH原理与实践.assets/image-20220617145937979.png" title="null" crop="0,0,1,1" id="lONP5" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267695021-2e24b4d7-c669-42a1-9c23-5c09a5bf3dd2.png" width="1026" title="" crop="0,0,1,1" id="u6d7fc0a0" class="ne-image">

```python
此时假设甲向乙发送信息：
1.甲采用对称密钥对明文信息进行加密
2.甲使用乙的公钥对对称密钥进行加密，得到就是数字信封
3.甲将密文以及数字信封发送给乙
4.乙收到密文以及数字信封之后，先用自己的私钥对数字信封进行解密，得到对称密钥
5.乙使用解密得到的对称密钥再对密文信息进行解密，得到最原始的明文信息
```

#### 2.3 数字签名
<img src="SSH原理与实践.assets/image-20220617150000236.png" title="null" crop="0,0,1,1" id="XEn26" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267363987-ff85596a-412d-4e70-a9ad-5dd242bc2b41.png" width="1053.3333333333333" title="" crop="0,0,1,1" id="jSxMj" class="ne-image">

```python
假设甲要向乙发送信息
1.甲采用对称密钥对明文信息进行加密
2.甲使用乙的公钥对对称密钥进行加密，得到就是数字信封
3.甲将最原始的明文信息通过hash计算得到一段hash-1值，并将该hash值使用甲的私钥进行加密，得到一个数字签名
4.甲将密文、数字信封以及数字签名发送给乙
5.乙通过自己的私钥对数字信封进行解密，得到对称密钥
6.乙使用对称密钥对密文信息进行解密，得到明文信息
7.乙使用该明文信息通过hash计算得到一段hash-2值
8.乙使用甲的公钥对数字签名进行解密，得到hash-1值
9.乙将hash-1 和hash-2进行比对，如果相同，则可以判定信息没有被篡改，或者说一定是甲发送的信息
```

### 3 SSH传输层协议
<img src="SSH原理与实践.assets/image-20220617152725857.png" title="null" crop="0,0,1,1" id="aMpqh" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267713209-16ad451b-0116-48bb-8e82-fb66ade9d1e2.png" width="1031.3333333333333" title="" crop="0,0,1,1" id="ub6103572" class="ne-image">

```python
密钥交换算法：双方根据该算法生成一个对称加密的密钥，用于后续报文的加密
公钥算法：用于用户认证时选择哪种算法进行非对称加密
对称加密算法：用于报文在进行对称加密时采用哪种对称加密的算法
消息认证算法：用于数据完整性的认证
```



### 4 用户认证原理
+ 口令认证（账号密码认证）

<img src="SSH原理与实践.assets/image-20220617151729483.png" title="null" crop="0,0,1,1" id="khi93" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267729735-227bdd2e-d85b-4b1c-8d5e-983964823082.png" width="760" title="" crop="0,0,1,1" id="u77ecadba" class="ne-image">

+ 公钥认证（免密登录）

<img src="SSH原理与实践.assets/image-20220617151805850.png" title="null" crop="0,0,1,1" id="yCABv" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267732985-b0dd4c66-a774-48be-a089-5c570fb90ee5.png" width="738.6666666666666" title="" crop="0,0,1,1" id="u94ac4270" class="ne-image">

+ 免密登录虽然不用输入账号密码，但是需要事先将客户端的公钥保存在服务器中

### 5 SSH连接协议
<img src="SSH原理与实践.assets/image-20220617152621092.png" title="null" crop="0,0,1,1" id="NkOPg" class="ne-image"><img src="https://cdn.nlark.com/yuque/0/2026/png/50508853/1779267724952-abe184a4-3b4d-4060-b8ca-b7974f397347.png" width="618" title="" crop="0,0,1,1" id="u63f8222f" class="ne-image">
