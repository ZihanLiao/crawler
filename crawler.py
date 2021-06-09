import requests
import time
import hashlib
import random
import json
import os
from tqdm import tqdm




# 爬取喜马拉雅的音乐的类
class crawler(object):

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36"
        }

    def getServerTime(self):
        """
        获取喜马拉雅服务器的时间戳
        :return:
        """
        # 这个地址就是返回服务器时间戳的接口
        serverTimeUrl = "https://www.ximalaya.com/revision/time"
        response = requests.get(serverTimeUrl,headers = self.headers)
        return response.text

    def getSign(self,serverTime):
        """
        生成 xm-sign
        规则是 md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :param serverTime:
        :return:
        """
        nowTime = str(round(time.time()*1000))

        sign = str(hashlib.md5("himalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + serverTime + "({})".format(str(round(random.random()*100))) + nowTime
        # 将xm-sign添加到请求头中
        self.headers["xm-sign"] = sign
        # return sign

    def getInfos(self,albumId,pageNum,sort,pageSize):
        all_list = []
        # 先调用该方法获取xm-sign
        self.getSign(self.getServerTime())
        # 将访问数据接口的参数写好
        params = {
            'albumId': albumId, # 页面id
            'pageNum': pageNum,
            'sort': sort,
            'pageSize':pageSize,# 一页有多少数据
        }
        # 喜马拉雅数据接口
        url = "https://www.ximalaya.com/revision/play/album"
        response = requests.get(url,params=params, headers=self.headers)
        infos = json.loads(response.text)
        book_list = infos['data']['tracksAudioPlay']
        for book in book_list:
            # 获取每段音频的名称和地址
            list = {}
            list['name'] = book['trackName']
            list['bookName'] = book['albumName']
            list['src'] = book['src']
            # 打印list
            # print(list)
            all_list.append(list)
            # 返回字典
        return all_list


def spider_songs(list, category):
    '''保存音频（字典）'''
    for i in list:
        dir = "wav_file"
        if not os.path.exists(dir):
            print("建立目录:.%s" % dir)
            os.makedirs(dir)
        i['name'] = i['name'].replace("?", "").replace('"', "")

        with open(r'{}/{}.m4a'.format(dir, category + '-' +  hashlib.md5(i['name'].encode('utf-8')).hexdigest()), 'ab') as f:
            if os.path.getsize(f.name) == 0:
                try:
                    r = requests.get(i['src'])
                except json.JSONDecodeError:
                    print('Source is invalid')
                except requests.exceptions.MissingSchema:
                    print('Source is invalid')
                else:
                    data_size = int(r.headers['Content-Length'])/1024/1024
                    print("正在下载:{}...".format(i['name']), end="")
                    for data in tqdm(iterable=r.iter_content(1024*1024), total=data_size,desc='正在下载',unit='MB'):
                        f.write(data)
                    print("\t下载完成！")
            f.close()



if __name__ == '__main__':
    crawler = crawler()
    mapping = {
        '28911073':([i for i in range(1,3)],'yujie'),
        '194617': ([i for i in range(1,3)],'luoli'),
        '34039862': ([i for i in range(1,3)],'yujie'),
        '20171530': ([i for i in range(1,3)],'yujie'),
        '46384358':([i for i in range(1,3)],'yujie'),
        '47502235':([1],'yujie'),
        '9706710':([1],'luoli'),
        '29196477':([i for i in range(1,5)],'luoli'),
        '32382630':([i for i in range(1,16)],'yujie'),
        '42271961':([1],'shaonv'),
        '40198999':([i for i in range(1,4)],'shaonv'),
        '44285246': ([1],'shaonv'),
        '18599186':([1],'dashu'),
        '29774267':([1],'shaonian'),
        '29851329':([1],'shaonian'),
        '49117314':([1],'dashu'),
        '34390396':([i for i in range(1,69)],'dashu'),
        '40434765':([i for i in range(1,7)], 'shaonian'),
        '49332483':([i for i in range(1,6)], 'luoli'),
        '42645799':([i for i in range(1,17)],' luoli'),
        '47000765':([i for i in range(1,4)], 'shaonv'),
        '41079794':([i for i in range(1,40)], 'shaonv'),
        '28380103':([i for i in range(1,3)], 'shaonian'),
        '25461468':([1], 'shaonian'),
        '14880332':([i for i in range(1,3)], 'shaonian')
    }
    for key in mapping.keys():
        print(key)
        for page in mapping[key][0]:
            category = mapping[key][-1]
            all_list = crawler.getInfos(key,page,'1','30')
            spider_songs(all_list,category)

