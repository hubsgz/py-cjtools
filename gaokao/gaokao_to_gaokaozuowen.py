#!/usr/bin/env python
# coding=utf-8

#高考作文采集

import sys

CFG = {}
CFG['classpy'] = 'gaokao';
CFG['classid'] = 88;

sys.path.append('../lib/')
import cjtools

#采信内容页网址
def get_detail_urls(html):

	relist = []

	start = 'fsefes'
	end = 'sefs'
	#links = cjtools.auto_get_links(html, start, end)

	relist.add({'url':'....', 'data':{}})

	return relist

def get_title(html):
	
	start = '<h1>';
	end = '</h1>'
	cjtools.startend(html, start, end)

def get_newstext(html):
	pass

def get_newstime(html):
	pass

def start():
	#要采集的网址
	urls = cjtools.addurl('http://a.com/index_%', 1, 10)
	for url in urls:
		html = cjtools.gethtml(url)
		detail_urls = get_detail_urls(html)
		for detailurl in detail_urls:

			if not cjtools.hascj(detailurl, CFG):

				detailhtml = cjtools.gethtml(detailurl)

				data = {'classid':CFG.classid, 'cjmark' : detailurl}
				data.title = get_title(detailhtml)
				data.newstext = get_newstext(detailhtml)

				isok = model.gkziliao.insert(data)
				if isok:
					cjtools.insert_success_cjdata(detailurl, CFG)
					cjtools.log('%s is ok' % data)
				else:
					cjtools.log('insert error %s' % detailurl)
			else:
				cjtools.log('skip %s' % detailurl)

def test():
	print cjtools.addurl('http://a.com/index_%', 1, 10)


if __name__ == '__main__':
	test()
	#start()
