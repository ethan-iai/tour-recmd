import web
import time

from cntr.graph import KnowledgeGraphHandler
from cntr.utils import get_data_path
from cntr.service.utils import str_cut

MAX_WORD = 1024

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
            'voice' : \
                    """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[voice]]></MsgType>
                        <Voice>
                            <MediaId><![CDATA[{MediaId}]]></MediaId>
                        </Voice>
                    </xml>
                    """,
            'music' : \
                    """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[music]]></MsgType>
                        <Music>
                            <Title><![CDATA[{Title}]]></Title>
                            <Description><![CDATA[{Description}]]></Description>
                            <MusicUrl><![CDATA[{MusicURL}]]></MusicUrl>
                            <HQMusicUrl><![CDATA[{HQMusicURL}]]></HQMusicUrl>
                            <ThumbMediaId><![CDATA[{MediaId}]]></ThumbMediaId>
                        </Music>
                    </xml>
                    """,
            'news' : \
                    """
                    <xml>
                        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                        <CreateTime>{CreateTime}</CreateTime>
                        <MsgType><![CDATA[news]]></MsgType>
                        <ArticleCount>1</ArticleCount>
                        <Articles>
                            <item>
                            <Title><![CDATA[{Title}]]></Title>
                            <Description><![CDATA[{Description}]]></Description>
                            <PicUrl><![CDATA[{PicUrl}]]></PicUrl>
                            <Url><![CDATA[{Url}]]></Url>
                            </item>
                        </Articles>
                    </xml>
                    """,
        }
        self._type_handler_map = {
            'text' : self._text_msg_handler,
        }
        
        self._graph_handler = KnowledgeGraphHandler(
            province_path=get_data_path('data/province.txt'),
            type_path=get_data_path('data/type.txt'),
            name_path=get_data_path('data/name.txt')
        )

    def _init_kwargs(self, msg):
        kwargs = dict()
        kwargs['ToUserName'] = msg.FromUserName
        kwargs['FromUserName'] = msg.ToUserName
        kwargs['CreateTime'] = int(time.time())
        return kwargs
        
    def _text_msg_handler(self, msg):
        kwargs = self._init_kwargs(msg)
        # TODO: interface attached here
        kwargs['Content'] = str_cut(self._graph_handler(msg.Content.decode('utf-8')), MAX_WORD)     
        return self._type_xmlform_map['text'].format(**kwargs)

    def _voice_msg_handler(self, msg):
        pass

    def _loaction_msg_handler(self, msg):
        pass

    def _image_msg_handler(self, msg):
        pass

    def _default_handler(self):
        return "success"

    def __call__(self, msgType, msg):
        if msg.MsgId in web.ctx.globals.reply_msg_cache:
            print('[DBG] entry found')
            return web.ctx.globals.reply_msg_cache[msg.MsgId]    
        else:
            try:
                web.ctx.globals.reply_msg_cache[msg.MsgId] =\
                    self._type_handler_map[msgType](msg)
                print('[DBG] entry inserted')
            except KeyError:
                web.ctx.globals.reply_msg_cache[msg.MsgId] =\
                    self._default_handler()
            except Exception as e:
                print(e.args)
                web.ctx.globals.reply_msg_cache[msg.MsgId] =\
                    self._default_handler()
            # print(web.ctx.globals.reply_msg_cache)
            print('[DBG] entry not found')
            # return self._reply_msg_cache.pop(msg.MsgId)

