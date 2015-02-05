#!/usr/bin/env python
# coding=utf-8

"""采集工具集"""

import urllib,os,urlparse,urllib2
import random,string,time
import hashlib,re
import db

DATA_URLS = []

def gethtml(url):
    '''
        获取网页内容
    '''
    header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
        "Connection":"keep-alive",       
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    req = urllib2.Request(url, headers=header)
    webpage = urllib2.urlopen(req)
    html = webpage.read()
    return html

def addurl(urlf, start=0, end=0, isreset=False):
    '''
        添加采集网址
    '''
    global DATA_URLS
    if start > 0 and end>0:
        if isreset:
            DATA_URLS = []
        for i in range(start, end):
            DATA_URLS.append(urlf.replace("{p}", str(i)))        
    else:
        DATA_URLS.append(urlf)
    return DATA_URLS

def getpicname(path):
    '''
        retrive filename of url
    '''
    ext = os.path.splitext(path)[1] 
    if ext == '':
        ext = '.jpg'
    name = ''.join(random.choice(string.letters) for i in xrange(9)) 
    return "%s%s" % (name, ext)
    #pr = urlparse.urlparse(path)
    #path='http://'+pr[1]+pr[2]
    #return os.path.split(path)[1]

def saveimgto(path, urls):
    '''
    save img of url to local path
    '''
    if not os.path.isdir(path):
        print('path is invalid')
        sys.exit()
    else:
        path = "%s%s/" % (path, time.strftime('%Y-%m-%d-%H',time.localtime(time.time())))
        if not os.path.exists(path):
            os.mkdir(path)
        for url in urls:            
            tofile = os.path.join(path, getpicname(url))
            log('save %s as %s' % (url, tofile))
            of=open(tofile, 'w+b')
            q=urllib.urlopen(url)
            of.write(q.read())
            q.close()
            of.close()

def auto_save_file(html, regx=None):
    '''
        自动下载图片，附件等
    '''
    pass


def log(strs):
    print strs

def md5(sstr):
    return hashlib.md5(sstr).hexdigest() 

def hascj(url, cjcfg):
    '''
        判断网址是否已经采集过
    '''
    url = url.strip()
    sql = "select count(*) as num from cjtools.successurls where classid='%d' and urlmd5='%s'" % (cjcfg['classid'], md5(url))
    res, row = db.get_row(sql)
    print row
    return row['num']>0

def insert_success_cjdata(url, cjcfg):
    '''
        记录采集成功的数据
    '''
    url = url.strip()
    sql = "insert into cjtools.successurls (id, classid, classpy, url, urlmd5) \
    values ('0', '%d', '%s', '%s', '%s')" % (cjcfg['classid'], cjcfg['classpy'], url, md5(url))
    print db.execute(sql)

def startend(html, start, end):
    '''
        获取内容
    '''
    rex = "%s(.*)%s" % (start,end)
    rex = '<p class="clearfix">(.*)</p>(\s+)<p class="clearfix">'
    print html.encode('utf8').decode('utf8')
    html = """
            <p class="clearfix">
                <a goto="xin2">新课标全国卷</a>
                <a goto="gx">大纲全国卷</a>
                <a goto="bj">北京卷</a>
                <a goto="sh">上海卷</a>
                <a goto="tj">天津卷</a>
                <a goto="cq">重庆卷</a>
                <a goto="sd">山东卷</a>
                <a goto="js">江苏卷</a>
                <a goto="hn">湖南卷</a>
                <a goto="fj">福建卷</a>
                <a goto="sc">四川卷</a>
            </p>


    """
    return re.findall(rex, html, re.I|re.S|re.M)


def auto_get_links(html, start, end):
    pass

if __name__ == '__main__':
    print md5('123456')
    print md5('abc123')

    html = gethtml('http://www.gaokao.com/gkzw/gkmfzw/')

    start = '''<div class="tabCon">
                <div>
'''
    start = start.replace("\n", r'\\n')
    print start
    end = '''<h3'''
    print startend(html, start, end)
    exit()

    addurl("http://baidu.com/p.html")
    print addurl("http://badu.com/p{p}.html", 2, 20)

    print getpicname('http://www.sgzhang.com/uploads/2014/10/MyEnTunnel_01.png')
    print getpicname('http://www.sgzhang.com/uploads/2014/10/MyEnTunnel_01')
    print getpicname('http://www.sgzhang.com/uploads/2014/10/MyEnTunnel_01.tar')
    saveimgto('/tmp/', ['http://www.sgzhang.com/uploads/2014/10/MyEnTunnel_01.png','http://www.sgzhang.com/uploads/2014/11/t-mei.jpg'])

    print hascj('http://www.ssss.com/1.html', {'classid':99999, 'classpy':'test'})
    insert_success_cjdata('http://www.ssss.com/1.html', {'classid':99999, 'classpy':'test'})
    print hascj('http://www.ssss.com/1.html', {'classid':99999, 'classpy':'test'})


