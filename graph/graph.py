import py2neo
import jieba
import eventlet
import utils

TIME_OUT = 10


class KnowledgeGraphHandler(object):

    def __init__(self, province_path, type_path, name_path):
        jieba.load_userdict(name_path)
        jieba.load_userdict(type_path)

        file_1 = open('type.txt', 'r', encoding='UTF-8')
        self._type_list = file_1.read().splitlines()

        file_2 = open('province.txt', 'r', encoding='UTF-8')
        self._province_list = file_2.read().splitlines()

        graph = py2neo.Graph(
            "http://localhost:7474",
            password="200171"
        )

        self._N_selector = py2neo.NodeMatcher(graph)
        self._R_selector = py2neo.RelationshipMatcher(graph)

        self._all_des = self._N_selector.match("名称")




    def inquire_min_distance(self, mc):
        """

        :param mingcheng: 用户输入的景区名称
        :return: 返回(同省)景区间距离从近到远排序的字典(dict)
        """
        #先得到用户输入景点的经纬度
        NODE_des = self._N_selector.match("名称", name=mc).first()
        R_lng1 = self._R_selector.match((NODE_des,), "经度").first()
        R_lat1 = self._R_selector.match((NODE_des,), "纬度").first()
        lng1 = R_lng1.end_node['name']
        lat1 = R_lat1.end_node['name']
        R_province = self._R_selector.match((NODE_des,), "省份").first()
        province = R_province.end_node
        R_same_province_des=self._R_selector.match((province,), "省份2名称")

        des={ }
        for i in R_same_province_des: #i是省份和景点的关系
            #print(i)
            d=i.end_node
            if (d['name'] != mc):
                R_lng2 = self._R_selector.match((d,), "经度").first()
                R_lat2 = self._R_selector.match((d,), "纬度").first()
                lng2 = R_lng2.end_node['name']
                lat2 = R_lat2.end_node['name']
                dis=utils.getDistance(lat1, lng1, lat2, lng2)
                if(dis<100):
                    des[d['name']]=dis

        des=sorted(des.items(), key=lambda kv: (kv[1], kv[0]))
        des_re= ' '
        for src in des:
            des_re= des_re + str(src) + ' \n '
        return des_re

    def inquire_by_province_return_Rselector(self, province):
        #根据用户输入省份查询景区
        """
        #TODO:触发词：景区，关键词：省份。
        :param mc: 省份
        :return: 景区列表(list)
        """
        N_province=self._N_selector.match("省份", name=province).first()
        R_des= self._R_selector.match((N_province,), "省份2名称")
        return R_des

    def inquire_by_province_return_list(self, province):
        #根据用户输入省份查询景区
        """
        #TODO:触发词：景区，关键词：省份。
        :param mc: 省份
        :return: 景区列表(str)
        """
        N_province=self._N_selector.match("省份", name=province).first()
        R_des= self._R_selector.match((N_province,), "省份2名称")
        #des=''
        des=set()
        for r in R_des:
            #es=des+r.end_node['name']+'\n'
            des.add(r.end_node['name']+'\n')
        return des

    def inquire_by_type(self, type,rse):
        """
        #TODO:触发词和关键词都设置为类型字符串
        :param type:
        :return:返回某省或全国的(rse==None)的同类景区名称(list)
        """

        N_type = self._N_selector.match("类型", name=type).first()
        R_des = self._R_selector.match((N_type,), "include")
        t_des =set()

        for r in R_des:
            t_des.add(r.end_node['name']+'\n')
        
        if rse ==None:
            return t_des
        else:
            for r in rse:
                N_province = r.start_node['name']
                p_des=self.inquire_by_province_return_list(N_province)
                des = t_des & p_des
                return des



    def recommand_by_ticket(self, ticket,rse):
        """
        #TODO:触发词:票价 关键词:数字
        :param ticket:
        :return:   返回景区名称和票价字典(dict)
        """
        des=set()
        if rse!=None:
            for r in rse:
                d= r.end_node
                R_ticket = self._R_selector.match((d,),"票价").first()
                char_ticket =R_ticket.end_node['name']
                d_ticket=float(char_ticket)
                if d_ticket<=ticket:
                    des.add(d['name']+' 票价:'+char_ticket+'\n')
        else:
            for d in self._all_des:
                R_ticket = self._R_selector.match((d,),"票价").first()
                char_ticket =R_ticket.end_node['name']
                d_ticket=float(char_ticket)
                if d_ticket<=ticket:
                    des.add(d['name']+' 票价:'+char_ticket+'\n')
        return des

    def recommand_by_sales(self, sales,rse):
        des=set()
        if rse !=None:
            for r in rse:
                d =r.end_node
                R_sales = self._R_selector.match((d,),"月销量").first()
                char_sales =R_sales.end_node['name']
                d_sales=int(char_sales)
                if d_sales>=sales:
                    des.add(d['name'] + ' 月销量:' + char_sales + '\n')
        else:
            for d in self._all_des_all_des:
                R_sales = self._R_selector.match((d,), "月销量").first()
                char_sales = R_sales.end_node['name']
                d_sales = int(char_sales)
                if d_sales >= sales:
                    des.add(d['name'] + ' 月销量:' + char_sales + '\n')
        return des

    def print_detailed_info(self, mc):
        """
        打印景区详细信息
        :param mc:景区名称
        :return:返回详细信息(string)
        """
        node_des = self._N_selector.match("名称", name=mc).first()
        location = (self._R_selector.match((node_des,), "地址").first()).end_node['name']

        R_type = self._R_selector.match((node_des,), "名称2类型")
        type=" "
        for r in R_type:
            type= type +"#"+ r.end_node['name']
        level= (self._R_selector.match((node_des,), "级别").first()).end_node['name']
        ticket= (self._R_selector.match((node_des,), "票价").first()).end_node['name']
        characteristic= (self._R_selector.match((node_des,), "介绍").first()).end_node['name']
        monthly_sales= (self._R_selector.match((node_des,), "月销量").first()).end_node['name']
        picture = (self._R_selector.match((node_des,), "图片").first()).end_node['name']
        des="名称:"+ mc+"\n类型:"+type+"\n地址:"+location+"\n级别:"+level+"\n票价:"+ticket+"\n月销量:"+monthly_sales+"\n介绍:"+characteristic+"\n图片:"+picture
        return des


    def _classify(self, input):
        words = list(jieba.cut(input, cut_all=False))# paddle模式
        print("jieba分词结果:")
        print(words)
        province_rselector = None #p_r是省份到景区名称的关系类型
        guess_flag = 0
        for word in words:
            if word in self._province_list:  # 查询某省份的景区
                province_rselector = self.inquire_by_province_return_Rselector(word)
                guess_flag = 1
                break

        if "旁边" in words or "附近" in words:
            r=self.inquire_min_distance(words[0])
            return r
        elif "详细信息" in words:
            r=self.print_detailed_info(words[0])
            return r
        elif "票价" in words:
            input_ticket=""
            for i in input:  # 将字符串进行遍历
                if str.isdigit(i):  # 判断i是否为数字，如果“是”返回True，“不是”返回False
                    input_ticket += i
            r=self.recommand_by_ticket(float(input_ticket),province_rselector)
            return r
        elif "月销量" in words or "销量" in words:
            sales = ""
            for i in input:  # 将字符串进行遍历
                if str.isdigit(i):  # 判断i是否为数字，如果“是”返回True，“不是”返回False
                    sales += i
            r=self.recommand_by_sales(float(sales),province_rselector)
            return r
        for word in words:
            if word in self._type_list:
                r=self.inquire_by_type(word,province_rselector)
                return r


        #if guess_flag ==0 : print("打扰了,是我太菜了,未能识别您的问题,请您按照使用说明输入[让我看看]")
        if guess_flag == 1:
            for word in words:
                if word in self._province_list:# 查询某省份的景区
                    des = self.inquire_by_province_return_list(word)
                    return des
        return None

    def __call__(self, input):
        # eventlet.monkey_patch()  # FIXME: place in right postion
        # with eventlet.Timeout(TIME_OUT, False):
        des_list = self._classify(input)
        if isinstance(des_list, str):
            return des_list
        elif isinstance(des_list, set):
            return ''.join(des_list)
        else:
            return "能力一般,水平有限,请您重新输入问题"



if __name__ == '__main__':
	from graph import KnowledgeGraphHandler

if __name__ == '__main__':
    graph_handler = KnowledgeGraphHandler(
        province_path = r'../data/province.txt',
        type_path = r'../data/type.txt',
        name_path = r'../name.txt'
    )

    line = input()
    if line and len(line) > 0:
        print(graph_handler(line))
