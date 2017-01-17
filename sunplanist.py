# encoding=utf-8
import json
import base64
import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector

myWeiBo = [
    {'no': 'cp123002@126.com', 'psw': '*******'}
]
articleUrl = 'http://weibo.com/u/1927070524?is_search=0&visible=0&is_article=1&is_tag=0&profile_ftype=1&page='
remoteArtileUrl = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&profile_ftype=1&is_article=1&pagebar=0&pl_name=Pl_Official_MyProfileFeed__24&id=1005051927070524&script_uri=/u/1927070524&feed_type=0&pre_page=1&domain_op=100505&__rnd=1484618916861&page='
staticUrl = 'http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=100505&profile_ftype=1&is_article=1&pagebar=0&pl_name=Pl_Official_MyProfileFeed__24&id=1005051927070524&script_uri=/u/1927070524&feed_type=0&page=2&pre_page=1&domain_op=100505&__rnd=1484618916861'
path = 'D:/sunplanist/'
domain = 'http://weibo.com/'
articleDomain = 'http://weibo.com/ttarticle/p/show?id='
cookies = dict({'SUB': '_2A251eDr2DeRxGedH61IY9irPzj2IHXVWDCs-rDV_PUNbm9AKLW3lkW9jxBxPPHtTE2oL9Ro7x3uIQDsx4A..', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJOyNfRkxkNh0jS8bSgy.y5NHD95Qp1K571KqXe0-pWs4DqcjzMNxLMcyDdJ-t', 'ALF': '1516076582', 'SCF': 'AsyQefbOlYDylg4fCtw3H3QMPF2JV8CpO-vIxNV0cOhJwr1y9KpQLywbKICnoNJWuyQxr8Io4N75502Z5V8Z-Fo.', 'ALC': 'ac%3D0%26bt%3D1484540582%26cv%3D5.0%26et%3D1516076582%26scf%3D%26uid%3D1900964351%26vf%3D0%26vs%3D1%26vt%3D0%26es%3D76d319342811f47f070777c7a21408ad', 'sso_info': 'v02m6alo5qztZOdlrmzmoalrpmSmbWalpC9jJOksIyDpLaNg4y1jJDAwA==', 'tgc': 'TGT-MTkwMDk2NDM1MQ==-1484540582-xd-94656CFB8970062D24ADEEFB3C75B24F-1', 'LT': '1484540582'})
remoteHeaders = {'Host': 'weibo.com','Upgrade-Insecure-Requests':'1','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
remoteCookie = {'Cookie': 'SINAGLOBAL=180004545838.58127.1478226788825; TC-Ugrow-G0=02e35d9240e6933947925d24232af628; SSOLoginState=1484533995; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; wb_g_upvideo_1900964351=1; _s_tentry=login.sina.com.cn; Apache=4914359893033.586.1484533998141; ULV=1484533998155:8:2:1:4914359893033.586.1484533998141:1484014332879; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; UOR=www.csdn.net,widget.weibo.com,login.sina.com.cn; SCF=AunKxN5b-9Qj_8fHyis92yCtDUqeqE1j2tPOKNHhkkWvaaHsOYZP-QxFTjFndvhGUmQX-Xb7vsiPInnoKUwWkAA.; SUB=_2A251efdeDeRxGedH61IY9irPzj2IHXVWD2-WrDV8PUNbmtAKLU7QkW9OTxN_MGwdKyPi10rGDGtDF_OgzQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJOyNfRkxkNh0jS8bSgy.y5JpX5KMhUgL.Fo24eh54SoB0SK22dJLoI7y0UsH0IsLV9Btt; SUHB=010HR9Eb3Yh3k3; ALF=1516157581'}
aricleSet = set()
def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
        postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
        session = requests.Session()
        r = session.post(loginURL, data=postData)
        jsonStr = r.content.decode('gbk')
        info = json.loads(jsonStr)
        if info["retcode"] == "0":
            print "Get Cookie Success!( Account:%s )" % account
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            print "Failed!( Reason:%s )" % info['reason']
    return cookie

def getArticleList(page,cookie):
    try:
        headers = {'encoding': 'UTF-8'}
        realArticleUrl = articleUrl+page
        print realArticleUrl
        r = requests.get(realArticleUrl,cookies = cookie,headers =headers)
        selector = Selector(text=r.text.encode('utf-8'))
        text0 = selector.xpath('//script/text()').extract() # 获取标签里的所有text()
        for i in text0:
            try:
                #print i
                tag = i[8:len(i)-1]
                data = json.loads(tag)
                html =  data['html']
                setArticleSet(html)
            except:
                print ''
    except:
        print  '->  ' + str(aricleSet)

    realRemoteArtileUrl = remoteArtileUrl+page
    print realRemoteArtileUrl
    remote = requests.get(realRemoteArtileUrl, cookies=remoteCookie,headers = remoteHeaders)
    #print remote.text
    data = json.loads(remote.text)
    remoteHtml = data['data']
    setArticleSet(remoteHtml)

    return aricleSet

def setArticleSet(html):
    try:
        soup = BeautifulSoup(html)
        # print soup
        linkhtml = soup.select('div[action-data*="ttarticle"]')
        # linkhtml = soup.select('div[action-data]')
        # if(linkhtml != '' ):
        for i in linkhtml:
            aricleSet.add(domain + i.get('action-data'))
    except:
        print ''

def getTitle(content):
    soup = BeautifulSoup(content)
    title =  soup.select('div[node-type="articleTitle"]')[0].get_text()
    return title

def getArticleContent(id,cookie):
    r = requests.get(articleDomain + id, cookies=cookie)
    return r.text

def outputFile(title,content):
    file = open(path+title+'.html', "wb")
    file.write(content.encode('utf-8'))
    file.close()

def getArticleId(urlSet):
    idSet = set()
    for url in urlSet:
        id = url[url.index('%3D')+3:url.index('&')]
        idSet.add(id)
    return idSet

def process(articleList):
    list = '<meta>'
    for i in articleList:
        content = getArticleContent(i, cookies)
        print content
        title = getTitle(content)
        list = list + '<a href="'+i+'.html">'+title+'</a><br/>'
        outputFile(i, content)
    outputFile('list',list)
#cookies = getCookies(myWeiBo)

print "Get Cookies Finish!( Num:%d)" % len(cookies)
allArtile = set()
for i in range(1,10):
    urlSet = getArticleList(str(i), cookies)
    allArtile = allArtile | getArticleId(urlSet)
process(allArtile)
#print allArtile   123