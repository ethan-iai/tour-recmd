import hashlib
import reply
import receive
import web


class Handle(object):
    def __init__(self):
        self._receive_hadler = receive.ReceiveHandler()
        self._reply_handler = reply.ReplyHandler()

    def GET(self):
        try:
            data = web.input()
            if not data or len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "nil" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            temp_str = ""
            for str in list:
                temp_str = temp_str + str
            _sha1 = hashlib.sha1()
            _sha1.update(temp_str.encode('utf8'))
            hashcode = _sha1.hexdigest()
            print("handle/GET func: hashcode, signature: ", hashcode, signature)
            
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception as e:
            return e.args

    def POST(self):
        try:
            webData = web.data()
            print("Handle Post webdata is ", webData)
            #后台打日志
            recType, recMsg = self._receive_hadler.parse_xml(webData)
            return self._reply_handler(recType, recMsg)
        except Exception as e:
            return e.args
