import requests

"""
pid=项目ID
uid=登录用户名
token=登录时返回的令牌
mobile=指定号码获取(可以不填写该参数，如填入格式不正确则获取新号码)
size=获取号码数(可以不填，默认为1，1<=size<=10)
operator=运营商；可以不填，指定运营商只支持填单个，取值:CMCC(移动)|UNICOM(联通)|TELECOM(电信)
province=指定省份获取号码，只能填单个地区，不填为任意地区
notProvince=排除指定省份号码，只能填单个地区，不填为不排除任何地区
vno=指定或排除虚拟运营商； 可以不填 ， vno=0 表示排除过滤虚拟运营商 vno=1 表示指定只取虚拟运营商。
city=指定城市；可以不填，只能填单个市，筛选市时需先选择省，才能选省下的市 如选广州市 那么 province=广东 ，否则无效，city取值范围请参考下面城市列表取值；
province/notProvince/city 参数为中文，传参时要经过URL转码, 例如 广东 编码后为 %E5%B9%BF%E4%B8%9C（java转码方式编码 java.net.URLEncoder.encode("广东","UTF-8")）。
使用 地区、运营商、虚拟运营商 筛选功能时需注意一个账号筛选时只选一个地区、运营商，不要一下筛选某地区，一下又筛选另一地区，否则返回的号码可能会混淆不一致。
省份(province/notProvince) 取值范围：辽宁|湖南|内蒙古|浙江|黑龙江|陕西|广西|安徽|湖北|贵州|福建|山西|西藏|河南|江西|海南|山东|江苏|云南|北京| 天津|广东|上海|新疆|青海|吉林|河北|四川|重庆|甘肃|宁夏
城市(city)取值范围 ；筛选市时需先选择省 ，否则无效。
author_uid=开发者账号
"""


class Dz(object):
    def __init__(self,username,password,pid,next_pid="",mobile="",operator="",province="",notProvince="",vno="",city="",author_uid=""):
        self.username = username
        self.password = password
        self.pid = pid
        self.next_pid = next_pid
        self.mobile = mobile
        self.operator = operator
        self.province = province
        self.notProvince = notProvince
        self.vno = vno
        self.city = city
        self.author_uid=author_uid
        self.error_msg = {
            "login_error": "用户名密码错误",
            "message": "访问过快，限制1秒一次。",
            "to_fast_try_again": "访问过快，限制1秒一次。",
            "account_is_closed": "账号被关闭（登录官网进入安全中心开启）",
            "account_is_stoped": "账号被停用",
            "account_is_locked": "账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）",
            "no_data": "系统暂时没有可用号码了",
            "parameter_error": "传入参数错误",
            "not_login": "没有登录,在没有登录下去访问需要登录的资源，忘记传入uid,token,或者传入token值错误，请登录获得最新token值",
            "you_cannot_get": "使用了项目绑定（登录官网进入安全中心解除绑定或添加该项目绑定）",
            "not_found_project": "没有找到项目,项目ID不正确",
            "Lack_of_balance": "可使用余额不足",
            "max_count_disable": "已经达到了当前等级可以获取手机号的最大数量，请先处理完您手上的号码再获取新的号码（处理方式：能用的号码就获取验证码，不能用的号码就加黑）",
            "unknow_error": "未知错误,再次请求就会正确返回",
            "not_found_moblie":"没有找到手机号",
            "not_receive":"还没有接收到验证码,请让程序等待几秒后再次尝试",


        }


    def loginln(self):
        """
        登录
        login_error                 用户名密码错误
        message|to_fast_try_again   访问过快，限制1秒一次。
        account_is_closed           账号被关闭（登录官网进入安全中心开启）
        account_is_stoped           账号被停用
        account_is_locked           账号被锁定（无法取号，充值任意金额解锁，请登录官网查看详情！）
        :return:
        """

        url = "http://api.jmyzm.com/http.do?action=loginIn&uid=%s&pwd=%s" %(self.username,self.password)
        response = requests.get(url=url).text
        if self.username in response:
            return response.split("|")[1]
        else:
            return self.error_msg[response]
        # print(error[response])

    def getMobilenum(self,token):
        """
        获取手机号
        :return:
        http://api.jmyzm.com/http.do?action=getMobilenum&pid=项目ID&uid=用户名&token=登录时返回的令牌&mobile=&size=1&province=%E5%B9%BF%E4%B8%9C&operator=CMCC&vno=&city=

        """
        # token = ""
        url = "http://api.jmyzm.com/http.do?action=getMobilenum&pid=%s&uid=%s&token=%s&mobile=%s&size=1&province=%s&operator=%s&vno=%s&city=%s" %(self.pid,self.username,token,self.mobile,self.province,self.operator,self.vno,self.city)
        response=requests.get(url=url).text
        if token in response:
            return response.split("|")[0]
        else:
            return self.error_msg[response]

    def getVcodeAndReleaseMobile(self,token,mobile):
        """
        获取验证码并不再使用本号
        :return:
        """
        url = "http://api.jmyzm.com/http.do?action=getVcodeAndReleaseMobile&uid=%s&token=%s&mobile=%s&author_uid=%s" %(self.username,token,mobile,self.author_uid)
        response = requests.get(url=url).text
        if mobile in response:
            return response.split("|")[1]
        else:
            return self.error_msg[response]

    def getVcodeAndHoldMobilenum(self,token,mobile):
        """
        获取验证码并继续使用本号
        :param token:
        :param mobile:
        :return:
        """
        url = "http://api.jmyzm.com/http.do?action=getVcodeAndHoldMobilenum&uid=%s&token=%s&mobile=%s&next_pid=%s&author_uid=%s" %(self.username,token,mobile,self.next_pid,self.author_uid)
        response = requests.get(url=url).text
        if token in response:
            return response.split("|")[1]
        else:
            return self.error_msg[response]

    def addlgnoreList(self,token,mobile):
        """
        加黑无用号码
        :param token:
        :param mobile:
        :return:
        """
        url = "http://api.jmyzm.com/http.do?action=addIgnoreList&uid=%s&token=%s&mobiles=%s&pid=%s" %(self.username,token,mobile,self.pid)
        response = requests.get(url=url).text
        if response in self.error_msg:
            return self.error_msg[response]
        else:
            return response

    def getUserInfos(self,token):
        """
        获取用户个人信息
        :return:
        """

        url = "http://api.jmyzm.com/http.do?action=getUserInfos&uid=%s&token=%s" %(self.username,token)
        response = requests.get(url=url).text

        if self.username in response:
            userinfo_list = response.split(";")
            user = userinfo_list[0]
            jifen = userinfo_list[1]
            yue = userinfo_list[2]
            num = userinfo_list[3]
            return {"用户名": user,"积分": jifen,"用户余额":yue,"可同时获取号码数": num,}
        else:
            return self.error_msg[response]

    def getRecvingInfo(self,token,pid=""):
        """
        已获取号码列表
        :param token:
        :param pid:
        :return:
        """
        url = "http://api.jmyzm.com/http.do?action=getRecvingInfo&uid=%s&pid=%s&token=%s" %(self.username,pid,token)
        response = requests.get(url=url).text
        print(response)
        if response in self.error_msg:
            return self.error_msg[response]
        else:
            return response



if __name__ == '__main__':



    regi=Dz("username","password","项目ID","开发者账号")
    #
    token = regi.loginln()
    # print(token)
    # mobile = regi.getMobilenum(token)
    # print(mobile)
    print(regi.getUserInfos(token))
    regi.getRecvingInfo(token)