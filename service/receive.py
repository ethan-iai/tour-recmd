import xml.etree.ElementTree as ET
from base import TextMsg, ImageMsg, LocationMsg, VoiceMsg

class ReceiveHandler(object):
    
    def __init__(self):
        self._type_class_map = {
            'text' : TextMsg,
            'image' : ImageMsg,
            'location': LocationMsg,
            'voice' : VoiceMsg,
        }
    
    def parse_xml(self, web_data):
        if len(web_data) == 0:
            return None
        xmlData = ET.fromstring(web_data)
        msg_type = xmlData.find('MsgType').text
        try:
            return msg_type, self._type_class_map[msg_type](xmlData)
        except KeyError as e:
            return None, None

