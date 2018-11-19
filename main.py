import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3534.4 Safari/537.36"}
proxies = {'http': 'socks5://127.0.0.1:1080', 'https': 'socks5://127.0.0.1:1080'}#代理自己设定



#Sougou
#https://www.sogou.com/web?query=%E5%85%AC%E5%8F%B8&page=1
#page=1表示第一页
#搜狗有请求频率限制，这个就不加入模块了
sougouPatt=re.compile("<cite.*?>.*?(www.*?/).*?<a style=\"display:none;\"")
pattSouGou2=re.compile("(http.*?//.*/)")
def GetSougouData(keyWords):
    i=1
    while 1<100:
        url="https://www.sogou.com/web?query="+keyWords+"page="+str(i)
        i+=1
        rep=requests.get(url,headers=headers)
        texts=rep.text
        print(texts)
        quit()
        ress=sougouPatt.findall(texts)
        print(ress)
#GetSougouData("公司")

#baidu
#https://www.baidu.com/s?wd=公司&pn=30
#pn=0表示第一页
#百度有点变态，要使用beautifulSoup解析
pattBaidu=re.compile("(.*/)")
pattBaidu2=re.compile("(http.*?//.*/)")
def GetBaiduData(keyWords):
    i=0
    results=[]
    while i<1000:
        print(i)
        BaiduUrl="https://www.baidu.com/s?wd="+keyWords+"+&pn="+str(i)
        i+=10
        res=requests.get(BaiduUrl,headers=headers)
        texts=res.text
        soup=BeautifulSoup(texts,'lxml')
        aContents=soup.find_all("a", class_="c-showurl")
        for aContent in aContents:
            vv=aContent.string
            if "so.com" in vv or "baidu" in vv or "360" in vv or "bing" in vv or "google" in vv:
                continue
            url=vv
            if "https" in url or "http" in url:
                try:
                    url=pattBaidu2.findall(url)
                    url=url[0]
                except:
                    continue
            if "http" not in url and "https" not in url:
                try:
                    url=pattBaidu.findall(url)
                    url = "http://" + url[0]
                except:
                    continue
            if url!=[]:
                print("baidu: "+url)
                results.append(url)
    return results
#GetBaiduData("公司")

#GetGoogleData("公司")
#取95页的数据最好
#google
#https://www.google.com/search?q=公司&start=30
#start=0表示第一页
#strs="""<cite class="iUh30">https://baike.baidu.com/item/公司</cite><cite class="iUh30">https://baike.baidu.com/item/公司</cite>"""
googlePatt=re.compile("<cite.*?>(.*?)</cite>")
#print(googlePatt.findall(strs))
def GetGoogleData(keyWords):
    i=0
    results=[]
    while i<1000:
        GoogleUrl="https://www.google.com/search?q=+"+keyWords+"+&start="+str(i)
        i+=10
        res=requests.get(GoogleUrl,headers=headers,proxies=proxies,verify=False)
        texts=res.text
        print(texts)
        onePageList=googlePatt.findall(texts)
        if onePageList!=[]:
            for ii,vv in enumerate(onePageList):
                if "so.com" in vv or "baidu" in vv or "360" in vv or "bing" in vv or "google" in vv:
                    continue
                if "http" and "https" not in vv:
                    vv="http://"+vv
                print("Google: "+vv)
                results.append(vv)
    return results

#360
#https://www.so.com/s?q=%E5%85%AC%E5%8F%B8&pn=1
#pn=1表示第一页
Patt360=re.compile("<cite.*?>(.*?)</cite>")
patt3602=re.compile(".*?\.com|.*?\.cn|.*?\.net|.*?\.org|.*?\.cc")

def Get360Data(keyWords):
    i=0
    results=[]
    while i<100:
        Url360="https://www.so.com/s?q="+keyWords+"&pn="+str(i)
        i+=1
        res=requests.get(Url360,headers=headers)
        texts=res.text
        onePageList = Patt360.findall(texts)
        if onePageList != []:
            for ii, vv in enumerate(onePageList):
                if "com" or "cn" or "net" or "org" or "cc" in vv:
                    try:
                        res=patt3602.findall(vv)[0]
                    except:
                        continue
                    if "so.com" in vv or "baidu" in vv or "360" in vv or "bing" in vv or "google" in vv:
                        continue
                    if "http" and "https" not in res:
                        res="http//"+res
                    results.append(res)
                    print("360: "+res)
    return results
#Get360Data("公司")

#bing)
#https://cn.bing.com/search?q=%E5%85%AC%E5%8F%B8&first=0
#first=0表示第一页，10表示第二页，20表示第三页
BingPatt=re.compile("<cite>(.*?)</cite>")
def getBingData(keyWords):
    i = 0
    results = []
    while i < 1000:
        BingUrl = "https://cn.bing.com/search?q="+keyWords+"&first="+str(i)+"&FORM=PERE"
        i += 10
        print(BingUrl)
        res = requests.get(BingUrl, headers=headers)
        texts = res.text
        res=BingPatt.findall(texts)
        for v in res:
            #print(v)
            results.append(v)
    return results
#getBingData("公司")
#Bing找不到规律接口，此项不用

#目前可用的搜索引擎为360百度
Get360Data("公司")
#GetGoogleData("公司")google的机器人检测绕不过去
GetBaiduData("公司")