# ReOTC

场外期权报价

## API列表

| API名称 | 认证方式 | 描述 |
| --- | --- | --- |
| GetQuotes | APP | 获取A股场外期权报价 |

## API调用

接口遵循aliyun开放接口规范，代码示例为`Python 2.7`, 其他语言可参考:

- [查看PHP版调用示例](https://github.com/aliyun/api-gateway-demo-sign-php)
- [查看.NET版调用示例](https://github.com/aliyun/api-gateway-demo-sign-net)
- [查看Node.js版调用示例](https://github.com/aliyun/api-gateway-nodejs-sdk)

### 公共入参

公共请求参数是指每个接口都需要使用到的请求参数。

参数名称 | 位置 |必须 | 描述
-------|------|--------|----
X-Ca-Key |Header| 是  | Appkey，调用API的身份标识
X-Ca-Signature | Header| 是  | 通过签名计算规则计算的请求签名串，参照：<a href="#Signature">签名计算规则</a>
X-Ca-Timestamp | Header| 否  | API 调用者传递时间戳，值为当前时间的毫秒数，也就是从1970年1月1日起至今的时间转换为毫秒，时间戳有效时间为15分钟
X-Ca-Nonce|Header| 否  |API请求的唯一标识符，15分钟内同一X-Ca-Nonce不能重复使用，建议使用 UUID，结合时间戳防重放
Content-MD5|Header| 否  |当请求 Body 非 Form 表单时，需要计算 Body 的 MD5 值传递给云网关进行 Body MD5 校验
X-Ca-Signature-Headers|Header|否|指定哪些Header参与签名，支持多值以","分割，默认只有X-Ca-Key参与签名，为安全需要也请将X-Ca-Timestamp、X-Ca-Nonce进行签名，例如：X-X-Ca-Signature-Headers:Ca-Timestamp,X-Ca-Nonce

### <span id="Signature">签名计算规则</span>
请求签名，是基于请求内容计算的数字签名，用于API识别用户身份。客户端调用API时，需要在请求中添加计算的签名（X-Ca-Signature）。

#### 签名计算流程
_________________________________________________________
准备APPkey → 构造待签名字符串stringToSign → 使用Secret计算签名
_________________________________________________________

##### 1.准备APPKey, Secret
Appkey，调用API的身份标识

##### 2.构造待签名字符串stringToSign

````
String stringToSign=
HTTPMethod + "\n" +
Accept + "\n" +                //建议显示设置 Accept Header。当 Accept 为空时，部分 Http 客户端会给 Accept 设置默认值为 */*，导致签名校验失败。
Content-MD5 + "\n"
Content-Type + "\n" +
Date + "\n" +
Headers +
Url
````

###### HTTPMethod
为全大写，如 POST。

````
Accept、Content-MD5、Content-Type、Date 如果为空也需要添加换行符”\n”，Headers如果为空不需要添加”\n”。
````

###### Content-MD5

Content-MD5 是指 Body 的 MD5 值，只有当 Body 非 Form 表单时才计算 MD5，计算方式为：

String content-MD5 = Base64.encodeBase64(MD5(bodyStream.getbytes("UTF-8")));
bodyStream 为字节数组。

###### Headers

Headers 是指参与 Headers 签名计算的 Header 的 Key、Value 拼接的字符串，建议对 X-Ca 开头以及自定义 Header 计算签名，注意如下参数不参与 Headers 签名计算：X-Ca-Signature、X-Ca-Signature-Headers、Accept、Content-MD5、Content-Type、Date。

###### Headers 组织方法：
先对参与 Headers 签名计算的 Header的Key 按照字典排序后使用如下方式拼接，如果某个 Header 的 Value 为空，则使用 HeaderKey + “:” + “\n”参与签名，需要保留 Key 和英文冒号。

````
String headers =
HeaderKey1 + ":" + HeaderValue1 + "\n"\+
HeaderKey2 + ":" + HeaderValue2 + "\n"\+
...
HeaderKeyN + ":" + HeaderValueN + "\n"
````

将 Headers 签名中 Header 的 Key 使用英文逗号分割放到 Request 的 Header 中，Key为：X-Ca-Signature-Headers。

###### Url

Url 指 Path + Query + Body 中 Form 参数，组织方法：对 Query+Form 参数按照字典对 Key 进行排序后按照如下方法拼接，如果 Query 或 Form 参数为空，则 Url = Path，不需要添加 ？，如果某个参数的 Value 为空只保留 Key 参与签名，等号不需要再加入签名。

````
String url =
Path +
"?" +
Key1 + "=" + Value1 +
"&" + Key2 + "=" + Value2 +
...
"&" + KeyN + "=" + ValueN
````

注意这里 Query 或 Form 参数的 Value 可能有多个，多个的时候只取第一个 Value 参与签名计算。

##### 3.使用Secret计算签名

````
Mac hmacSha256 = Mac.getInstance("HmacSHA256");
byte[] keyBytes = secret.getBytes("UTF-8");
hmacSha256.init(new SecretKeySpec(keyBytes, 0, keyBytes.length, "HmacSHA256"));
String sign = new String(Base64.encodeBase64(Sha256.doFinal(stringToSign.getBytes("UTF-8")),"UTF-8"));
````

Secret 为 APP 的密钥。



## API名称：GetQuotes

### *描述*

获取A股场外期权报价

### *请求信息*

HTTP协议：HTTPS

调用地址：otc.bjsdfx.com/api/options/quotes/[collection]

方法：Get

### *请求参数*

| 名称 | 位置 | 类型 | 必填 | 描述 |
| --- | --- | --- | --- | --- |
| collection | PATH | STRING | 是 | 报价集合，目前只开放30分钟报价集合，固定为 30min.csv |
| headOnly | QUERY | BOOLEAN | 否 | 仅返回报价集合的最后更新时间 |

### *返回信息*

#### 返回参数类型

PASSTHROUGH

#### 返回结果示例

````
symbol,name,option_type,strike_type,quote_date,begin_date,end_date,strike,quote,market_type,expiration
000001,平安银行,C,A,2018-02-28 14:30,2018-03-01,2018-03-11,1.0,4.92,1,10
000001,平安银行,C,A,2018-02-28 14:30,2018-03-01,2018-03-11,1.05,3.02,1,10
000001,平安银行,C,A,2018-02-28 14:30,2018-03-01,2018-03-31,1.0,6.92,1,30
000001,平安银行,C,A,2018-02-28 14:30,2018-03-01,2018-03-31,1.1,3.54,1,30
000001,平安银行,C,A,2018-02-28 14:30,2018-03-01,2018-05-30,1.0,10.55,1,90
000001,平安银行,C,A,2018-02-28 14:30,2018-03-01,2018-08-28,1.0,12.65,1,180
000002,万科A,C,A,2018-02-28 14:30,2018-03-01,2018-03-11,1.0,4.78,1,10
000002,万科A,C,A,2018-02-28 14:30,2018-03-01,2018-03-11,1.05,2.88,1,10
000002,万科A,C,A,2018-02-28 14:30,2018-03-01,2018-03-31,1.0,7.99,1,30
000002,万科A,C,A,2018-02-28 14:30,2018-03-01,2018-03-31,1.1,4.59,1,30
000002,万科A,C,A,2018-02-28 14:30,2018-03-01,2018-05-30,1.0,12.32,1,90
000002,万科A,C,A,2018-02-28 14:30,2018-03-01,2018-08-28,1.0,15.32,1,180
000004,国农科技,C,A,2018-02-28 14:30,2018-03-01,2018-05-30,1.0,14.78,1,90
000004,国农科技,C,A,2018-02-28 14:30,2018-03-01,2018-08-28,1.0,17.35,1,180
000008,神州高铁,C,A,2018-02-28 14:30,2018-03-01,2018-03-11,1.0,4.02,1,10
000008,神州高铁,C,A,2018-02-28 14:30,2018-03-01,2018-03-11,1.05,2.16,1,10
000008,神州高铁,C,A,2018-02-28 14:30,2018-03-01,2018-03-31,1.0,5.58,1,30
000008,神州高铁,C,A,2018-02-28 14:30,2018-03-01,2018-03-31,1.1,2.29,1,30
000008,神州高铁,C,A,2018-02-28 14:30,2018-03-01,2018-05-30,1.0,8.54,1,90
000008,神州高铁,C,A,2018-02-28 14:30,2018-03-01,2018-08-28,1.0,11.97,1,180
````

### *错误码*

| 错误码 | 错误信息 | 描述 |
| --- | --- | --- |
| 公共错误码 | -- | 所有API公用的错误码，请参照 <a href="#pubError">《 公共错误码 》</a> |

## <span id='pubError'>公共错误</span>
### 如何获取公共错误
所有的 API 请求只要到达了网关，网关就会返回请求结果信息。

用户需要查看返回结果的头部，即 Header 部分。返回参数如示例：

    //请求唯一ID，请求一旦进入API网关应用后，API网关就会生成请求ID并通过响应头返回给客户端，建议客户端与后端服务都记录此请求ID，可用于问题排查与跟踪
    X-Ca-Request-Id: 7AD052CB-EE8B-4DFD-BBAF-EFB340E0A5AF

    //API网关返回的错误消息，当请求出现错误时API网关会通过响应头将错误消息返回给客户端
    X-Ca-Error-Message: Invalid Url

    //当打开Debug模式后会返回Debug信息，此信息后期可能会有变更，仅用做联调阶段参考
    X-Ca-Debug-Info: {"ServiceLatency":0,"TotalLatency":2}

在 Header 中获得 X-Ca-Error-Message 可以基本明确报错原因，而 X-Ca-Request-Id 可以用于提供给这边的支持人员，供支持人员搜索日志。
### 公共错误码
#### 客户端错误

错误代码|Http 状态码|语义|解决方案
------|-----------|---|------
Throttled by USER Flow Control|403|因用户流控被限制|调用频率过高导致被流控，可以联系 API 服务商协商放宽限制。
Throttled by APP Flow Control|403|因APP流控被限制|调用频率过高导致被流控，可以联系 API 服务商协商放宽限制。
Throttled by API Flow Control|403   |因 API 流控被限制|调用频率过高导致被流控，可以联系 API 服务商协商放宽限制。
Throttled by DOMAIN Flow Control    |403|   因二级域名流控被限制|直接访问二级域名调用 API，每天被访问次数上限1000次。
TThrottled by GROUP Flow Control|403|因分组流控被限制|调用频率过高导致被流控，可以联系 API 服务商协商放宽限制。
Quota Exhausted |403|   调用次数已用完 |购买的次数已用完。
Quota Expired   |403|   购买次数已过期 |购买的次数已经过期。
User Arrears    |403|   用户已欠费   |请尽快充值续费。
Empty Request Body  |400|   body 为空|    请检查请求 Body 内容。
Invalid Request Body    |400    |body 无效    |请检查请求 Body。
Invalid Param Location  |400|   参数位置错误|请求参数位置错误。
Unsupported Multipart   |400|   不支持上传|不支持上传文件。
Invalid Url |400    |Url 无效 |请求的 Method、Path 或者环境不对。请参照错误说明 Invalid Url。
Invalid Domain  |400|   域名无效    |请求域名无效，根据域名找不到 API。请联系 API 服务商。
Invalid HttpMethod  |400    |HttpMethod 无效|输入的 Method 不合法。
Invalid AppKey|400|AppKey 无效或不存在    |请检查传入的 AppKey。注意左右空格的影响。
Invalid AppSecret   |400    |APP 的Secret 错误|    检查传入的 AppSecret。注意左右空格的影响。
Timestamp Expired|400|时间戳过时|请核对请求系统时间是否为标准时间。
Invalid Timestamp   |400|   时间戳不合法|请参照 请求签名说明文档。
Empty Signature |404|签名为空|请传入签名字符串，请参照 请求签名说明文档。
Invalid Signature, Server StringToSign:%s|400|签名无效|签名无效，参照 Invalid Signature 错误说明
Invalid Content-MD5|400|    Content-MD5 值不合法|请求 Body 为空，但传入了 MD5 值，或 MD5 值计算错误。请参照 请求签名说明文档。
Unauthorized    |403|   未被授权|   APP 未获得要调用的 API 的授权。请参照错误说明 Unauthorized。
Nonce Used|400| SignatureNonce| 已被使用SignatureNonce 不能被重复使用。
API Not Found|  400 |找不到 API|传入的APIdi地址或者HttpMethod不正确，或已下线。

#### 服务器端错误（调用 API）
以下为API服务端错误，如果频繁错误，可联系服务商。

错误代码|Http状态码|语义|解决方案
------|----------|---|----
Internal Error  |500    |内部错误|建议重试,或者联系服务商
Failed To Invoke Backend Service    |500|   底层服务错误|API 提供者底层服务错误，建议重试，如果重试多次仍然不可用，可联系 API 服务商解决
Service Unavailable|503|    服务不可用   |建议重试,或者联系服务商
Async Service   |504    |后端服务超时|建议重试,或者联系服务商

