import math
import jieba
EARTH_RADIUS = 6378.137

def rad(d):
    return d * math.pi / 180.0

def getDistance(lat1, lng1, lat2, lng2):
    """
    :param lat1: 第一个点的纬度(str)
    :param lng1: 第一个点的经度
    :param lat2: 第儿个点的纬度
    :param lng2: 第二个点的经度
    :return: 两个景点间的距离(float)
    """
    lat1=float(lat1)
    lng1=float(lng1)
    lat2=float(lat2)
    lng2=float(lng2)

    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b/2), 2)))
    s = s * EARTH_RADIUS
    return round(s,2)

class SynonymHandler(object):

    def __init__(self, synonym_path):
        self._replacements = dict()
        with open(synonym_path, "r", encoding='utf-8') as lines:
            for line in lines:
                words = line.strip().split(" ")
                replacement = words[0]
                for word in words[1:]:
                    self._replacements[word] = replacement

    def __call__(self, string):
        words = list(jieba.cut(string, cut_all=False))
        for i, word in enumerate(words):
            if word in self._replacements:
                words[i] = self._replacements[word]
        return ''.join(words)


if __name__ == '__main__':
    from cntr.utils import get_data_path
   
    handler = SynonymHandler(get_data_path('data/synonym.txt'))

    while True:
        line = input()
        print(handler(line))







# def recommand_by_province(mc):
#     """
#     #TODO:触发词:"省份"；关键词："景点"
#     :param province:
#     :return:
#     """
#     N_des = N_selector.match("名称",name = mc).first()
#     R_des_pro = R_selector.match((N_des,), "省份").first()
#     province = R_des_pro.end_node['name']
#     N_province = N_selector.match("省份", name=province).first()
#     R_des = R_selector.match((N_province,), "省份2名称")
#     des = []
#     for r in R_des:
#         des.append(r.end_node['name'])
#     return des
