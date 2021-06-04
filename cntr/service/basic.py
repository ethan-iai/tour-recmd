import os
import time
import json
import requests

APP_CONFIG_PATH = '~/.app_config'

class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):
        with open(os.path.expanduser(APP_CONFIG_PATH)) as f:
            kwargs = json.load(f)
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid={app_id}&secret={app_secret}".format(**kwargs))
        urlResp = requests.get(postUrl)
        urlResp = json.loads(urlResp.content)
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while(True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()


if __name__ == '__main__':
    print(Basic().get_access_token())
