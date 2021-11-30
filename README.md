# 支付SDK(微信、支付宝、银联)
### 编写不易，望勿抄袭，随便使用，请勿将代码发送其它平台，可引用
https://github.com/linqigu/upi
## 一、为什么要写这个SDK：
    (文字功底不好，口水话)为什么要写这个SDK，因为对接微信、支付宝、银联太难了，自己过来人，只想解决后续技术小伙伴少走点弯路
## 二、怎么使用好这个SDK
    1.pip install upi。
    2.在https://github.com/linqigu/upi 有使用tests。
    3.也可以发送邮箱给本人咨询怎么使用,个人邮箱 linqigu@163.com。
## 三、这个SDK以后的发展方向
    1.目前只集成了微信支付v2版本。
    2.后续新增加微信支付V3版本、查询订单、退款、下载账单待微信支付功能。
    3.支付宝支付目前已经申请下来商户号，开发中。
    4.银行支付目前只有特约商户的，好像不适用每个产品商务(正研究公共银联支付)。
## 四、版本更新
####  v0.0.8 更新内容
        1.修改wxPay支付中定义的变量为私有变量，不允许外面访问。
####  v0.0.2 更新内容
        1.生成微信支付wxPay，新增加微信支付包括 JS支付(公众号)、小程序支付、二维支付、APP支付、H5支付
        2.使用方式：
        from upi import wxPay
        app_id = ''
        mch_id = ''
        mch_key = ''
        notify_url = ''
        pay = wxPay(
            app_id=app_id,
            mch_id=mch_id,
            mch_key=mch_key,
            notify_url=notify_url
        )
        
        order_no = ''  # 订单号 可使用 from upi.util.tool import get_order_no 生成
        fee = 1 # 支付金额（整数）
        open_id = 'oHQtp5NEePp-HaSVEgrvCjw9eKcw'  # 用户openid
        body = '支付详情说明'
        res = self.pay.js_pay(
            order_no=order_no,
            fee=fee,
            openid=open_id,
            body=body
        )
        print(res)
        3.详情查询tests文件中demo.
#### v0.0.1 更新内容(已删除)
        1.第一版本提交，无代码，支付生成upi、test 目录
