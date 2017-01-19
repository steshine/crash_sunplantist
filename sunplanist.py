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
areadyFile = 'db.bin'
articleDomain = 'http://weibo.com/ttarticle/p/show?id='
#cookies = {'Cookie':'Cookie: SINAGLOBAL=180004545838.58127.1478226788825; TC-Ugrow-G0=02e35d9240e6933947925d24232af628; SSOLoginState=1484533995; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; wb_g_upvideo_1900964351=1; _s_tentry=login.sina.com.cn; Apache=4914359893033.586.1484533998141; ULV=1484533998155:8:2:1:4914359893033.586.1484533998141:1484014332879; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; wvr=6; SCF=AunKxN5b-9Qj_8fHyis92yCtDUqeqE1j2tPOKNHhkkWv555kOBOlNaRmZ_nUd39D-IYcaY1u6d1JU0Pg6ancxnU.; SUB=_2A251eqisDeRxGedH61IY9irPzj2IHXVW8Z1krDV8PUNbmtAKLVbZkW8TH27jhksSU6Br_ltr8hKlpKCyPQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJOyNfRkxkNh0jS8bSgy.y5JpX5KMhUgL.Fo24eh54SoB0SK22dJLoI7y0UsH0IsLV9Btt; SUHB=0h1IgCQAKwffqE; ALF=1516244092; UOR=www.csdn.net,widget.weibo.com,login.sina.com.cn'}
#contentCookie = {'Cookie':'SINAGLOBAL=180004545838.58127.1478226788825; TC-Ugrow-G0=02e35d9240e6933947925d24232af628; SSOLoginState=1484533995; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; wb_g_upvideo_1900964351=1; _s_tentry=login.sina.com.cn; Apache=4914359893033.586.1484533998141; ULV=1484533998155:8:2:1:4914359893033.586.1484533998141:1484014332879; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; UOR=www.csdn.net,widget.weibo.com,login.sina.com.cn; SCF=AunKxN5b-9Qj_8fHyis92yCtDUqeqE1j2tPOKNHhkkWvaaHsOYZP-QxFTjFndvhGUmQX-Xb7vsiPInnoKUwWkAA.; SUB=_2A251efdeDeRxGedH61IY9irPzj2IHXVWD2-WrDV8PUNbmtAKLU7QkW9OTxN_MGwdKyPi10rGDGtDF_OgzQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJOyNfRkxkNh0jS8bSgy.y5JpX5KMhUgL.Fo24eh54SoB0SK22dJLoI7y0UsH0IsLV9Btt; SUHB=010HR9Eb3Yh3k3; ALF=1516157581; wvr=6; WBStorage=ffbf906cea1ff551|undefined'}
#remoteCookie = {'Cookie': 'SINAGLOBAL=180004545838.58127.1478226788825; TC-Ugrow-G0=02e35d9240e6933947925d24232af628; SSOLoginState=1484533995; TC-V5-G0=458f595f33516d1bf8aecf60d4acf0bf; wb_g_upvideo_1900964351=1; _s_tentry=login.sina.com.cn; Apache=4914359893033.586.1484533998141; ULV=1484533998155:8:2:1:4914359893033.586.1484533998141:1484014332879; TC-Page-G0=e2379342ceb6c9c8726a496a5565689e; wvr=6; SCF=AunKxN5b-9Qj_8fHyis92yCtDUqeqE1j2tPOKNHhkkWv555kOBOlNaRmZ_nUd39D-IYcaY1u6d1JU0Pg6ancxnU.; SUB=_2A251eqisDeRxGedH61IY9irPzj2IHXVW8Z1krDV8PUNbmtAKLVbZkW8TH27jhksSU6Br_ltr8hKlpKCyPQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJOyNfRkxkNh0jS8bSgy.y5JpX5KMhUgL.Fo24eh54SoB0SK22dJLoI7y0UsH0IsLV9Btt; SUHB=0h1IgCQAKwffqE; ALF=1516244092; UOR=www.csdn.net,widget.weibo.com,login.sina.com.cn'}
aricleSet = set()
class config():

    def __init__(self):
        self.initlizate()
        if(self.cookieTimeout()):
            self.update()
            self.initlizate()
    def initlizate(self):
        file = open('user.conf', 'r')
        content = file.read()
        file.close()
        self.cookiesMap = json.loads(content)
    def update(self):
        cookie = getCookies(myWeiBo)
        config = {"cookies":cookie,"contentCookie":cookie,"remoteCookie":cookie}
        file = open('user.conf', 'wb')
        file.write(config)
        file.close()
    def cookieTimeout(self):
        content = getArticleList('1',self.cookiesMap['contentCookie'],self.cookiesMap['remoteCookie'])
        return content == ''
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

def getArticleList(page,cookie,remoteCookie):
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
    remote = requests.get(realRemoteArtileUrl, cookies=remoteCookie)
    print remote.text
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
    titles = soup.select('div[node-type="articleTitle"]')
    if len(titles) > 0:
        title = titles[0].get_text()
        return title
    return ''

def getArticleContent(id,cookie):
    contentUrl = articleDomain + id
    print contentUrl
    r = requests.get(contentUrl, cookies=cookie)
    return r.text

def outputArticleContent(title, content):
        file = open(path + title + '.html', "a")
        file.write(content)
        file.close()

def outputFile(title,content):
        file = open(path+title+'.html', "a")
        file.write(content.encode('utf-8'))
        file.close()

def getArticleId(urlSet):
    idSet = set()
    for url in urlSet:
        id = url[url.index('%3D')+3:url.index('&')]
        idSet.add(id)
    return idSet
#获取已经加载的文章id
def getArticleDB():
    areadyArticle = set()
    try:
        file = open(path+areadyFile,'r')
        lines = file.readlines()
        file.close()
    except:
        return set()
    for line in lines:
        areadyArticle.add(line.strip())
    return areadyArticle

def insertArticeDB(idsets):
    file = open(path + areadyFile, 'a')
    for i in idsets:
        if(i != ''):
            file.write(i+'\n')
    file.close()

def download(articleList):
    head = '<!DOCTYPE html> <html> <head>     <meta charset="UTF-8"/>     <meta name="viewport" content="width=device-width, initial-scale=1"/>     <link rel="shortcut icon" href="favorite.ico">     <link rel="apple-touch-icon-precomposed" sizes="144x144"           href="favorite.jpg">     <link rel="apple-touch-icon-precomposed" sizes="114x114"           href="favorite.jpg">     <link rel="apple-touch-icon-precomposed" sizes="72x72"           href="favorite.jpg">     <link rel="apple-touch-icon-precomposed"           href="favorite.jpg">     <style>         body {             color: #505050;             font-family: "SimHei", "Verdana";             font-size: 14px;             line-height: 1.42857;         }          .article {             width: 100%;         }          .article ul {             width: 90%;             /*text-align: center;*/             /*margin-left: auto;             margin-right: auto;*/             display: block;             margin-left: -40px;         }          .article > ul > li {             width: 100%;             color: inherit;             text-decoration: none;             float: left;             list-style: none;             position: relative;             display: block;             padding: 10px 15px;             margin-bottom: -1px;             border: 1px solid #ddd;         }          .article > ul > li > a {             color: inherit;             text-decoration: none;             float: left;             font-size: 1.2rem;         }     </style> </head> <body> <header>      </header> <div class="article">     <ul> '
    footer = '</ul> </div> <footer></footer> </body> </html>'
    if(len(articleList) == 0):
        print 'no fresh article'
        return
    url = ''
    for i in articleList:
        content = getArticleContent(i, config['cookies'])
        print content
        title = getTitle(content)
        if title != '':
            headC = '<!DOCTYPE html> <html> <head>     <meta charset="UTF-8"/>     <meta name="viewport" content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no"/>     <link rel="shortcut icon" href="favorite.ico">     <link rel="apple-touch-icon-precomposed" sizes="144x144"           href="favorite.jpg">     <link rel="apple-touch-icon-precomposed" sizes="114x114"           href="favorite.jpg">     <link rel="apple-touch-icon-precomposed" sizes="72x72"           href="favorite.jpg">     <link rel="apple-touch-icon-precomposed"           href="favorite.jpg">     <style>         body {  color: #505050;  font-family: "SimHei", "Verdana";  font-size: 14px;  line-height: 1.42857;  overflow-x: hidden;  }  .article {  width: auto;  max-width: 680px;  padding: 0 15px;  margin-right: auto;  margin-left: auto;  }  .title {  font-size: 1.2rem;  }  .WB_editor_iframe {  display: block !important;  visibility: inherit !important;  } img{  max-width:100%;} </style> </head> <body> <header>      </header> <div class="article">  '
            footerC = '</div><footer></footer> </body> </html>'
            soup = BeautifulSoup(content)
            contents = soup.select('div[node-type="articleContent"]')
            if len(contents) > 0:
                miniContent = str(contents[0].encode('utf-8'))
                outputArticleContent(i, headC +  miniContent + footerC)
            url = url + ' <li><a href="'+i+'.html">'+title+'</a></li>'

    outputFile('index',head+'\n'+url + footer)
#cookies = getCookies(myWeiBo)
config = config().cookiesMap
''''''

print "Get Cookies Finish!( Num:%d)" % len(config['cookies'])
allArtileIds = getArticleDB()
currentIds = set()
for i in range(1,12):
    urlSet = getArticleList(str(i), config['cookies'],config['remoteCookie'])
    currentIds = currentIds | getArticleId(urlSet)
needProcess = currentIds - allArtileIds
insertArticeDB(needProcess)
download(needProcess)
#print allArtile   123
