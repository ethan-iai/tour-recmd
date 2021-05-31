import time

class ReplyHandler(object):

    def __init__(self):
        self._type_xmlform_map = {
            'text' :  \
                    """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[text]]></MsgType>
                        <Content><![CDATA[{Content}]]></Content>
                    </xml>
                    """, 
            'image' : \
                    """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[image]]></MsgType>
                        <Image>
                        <MediaId><![CDATA[{MediaId}]]></MediaId>
                        </Image>
                    </xml>
                    """,
            'location' : \
                    """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[location]]></MsgType>
                        <Location_X>{Location_X}</Location_X>
                        <Location_Y>{Location_Y}}</Location_Y>
                        <Scale>{Scale}</Scale>
                        <Label><![CDATA[{Label}]]></Label>
                    </xml>
                    """,
            'voice' : \
                    """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[voice]]></MsgType>
                        <MediaId><![CDATA[{MediaId}]]></MediaId>
                        <Format><![CDATA[{Format}]]></Format>
                    </xml>
                    """,
        }
        self._type_handler_map = {
            'text' : self._text_msg_handler,
        }

    def _init_kwargs(self, msg):
        kwargs = dict()
        kwargs['ToUserName'] = msg.FromUserName
        kwargs['FromUserName'] = msg.ToUserName
        kwargs['CreateTime'] = int(time.time())
        return kwargs
        
    def _text_msg_handler(self, msg):
        kwargs = self._init_kwargs(msg)
        kwargs['Content'] = "test"  # interface attached here
        print(kwargs)
        return self._dbg(kwargs)

    def _dbg(self, kwargs):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                <CreateTime>{CreateTime}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{Content}]]></Content>
            </xml>
            """
        return XmlForm.format(**kwargs)

    def _voice_msg_handler(self, msg):
        pass

    def _loaction_msg_handler(self, msg):
        pass

    def _image_msg_handler(self, msg):
        pass

    def _default_handler(self):
        return "success"

    def __call__(self, msgType, msg):
        try:
            return self._type_handler_map[msgType](msg)
        except KeyError:
            return self._default_handler()
        except Exception as e:
            print(e.args)
            return self._default_handler()
