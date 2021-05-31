"""
class for messages(DTO) 
"""

class Msg(object):
    def __init__(self, xmlData):
        self.ToUserName = xmlData.find('ToUserName').text
        self.FromUserName = xmlData.find('FromUserName').text
        self.CreateTime = xmlData.find('CreateTime').text
        self.MsgType = xmlData.find('MsgType').text
        self.MsgId = xmlData.find('MsgId').text


class TextMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Content = xmlData.find('Content').text.encode("utf-8")    


class ImageMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.PicUrl = xmlData.find('PicUrl').text
        self.MediaId = xmlData.find('MediaId').text


class LocationMsg(Msg):
    def __init__(self, xmlData):
        Msg.__init__(self, xmlData)
        self.Location = (xmlData.find('Location_X').text, 
                         xmlData.find('Location_Y').text)  
        self.Scale = xmlData.find('Scale').text
        self.Label = xmlData.find('Label').text
        
class VoiceMsg(Msg):

    def __init__(self, xmlData):
        super().__init__(self, xmlData)
        self.MediaId = xmlData.find('MediaId').text 
        self.Format = xmlData.find('Fomrat').text
