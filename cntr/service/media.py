from .basic import Basic
import urllib3
import poster3

class Media(object):
    def __init__(self):
        poster3.streaminghttp.register_openers()
    
    # 上传图片
    def upload(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        param = {'media': openFile}
        postData, postHeaders = poster3.encode.multipart_encode(param)

        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (
            accessToken, mediaType)
        request = urllib3.Request(postUrl, postData, postHeaders)
        urlResp = urllib3.urlopen(request)
        print(urlResp.read())   # TODO: solve returned json to get MediaId 

if __name__ == '__main__':
    myMedia = Media()
    accessToken = Basic().get_access_token()
    filePath = "D:/code/mpGuide/media/test.jpg"  # 请按实际填写
    mediaType = "image"
    myMedia.upload(accessToken, filePath, mediaType)