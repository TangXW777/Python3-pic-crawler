#! /usr/bin/env python3
# -*- encoding: utf-8 -*-

#============= 获取某网站以及子网站所有的图片 =================

import re
import urllib.request
import requests
import http.cookiejar
import os.path
from collections import deque

urlList = set();  # 保存所有url
imgList = set();  # 保存所有图片url

# 获取opener
def makeMyOpener(head = {
	'Connection': 'Keep-Alive',
  'Accept': 'text/html, application/xhtml+xml, */*',
  'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
	cj = http.cookiejar.CookieJar();
	opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj));
	header =  [];
	for key, value in head.items():
		elem = (key, value);
		header.append(elem);
	opener.addheaders = header;
	return opener;

# 保存url到文件
def saveFileUrl():
	with open('urlFile.out', 'w') as f:
		for x in urlList:
			f.write(x + '\n');
		
# 保存图片url到文件
def saveFileImgUrl():
	with open('imgFile.out', 'w') as f:
		for x in imgList:
			f.write(x + '\n');
		

# 获取父网页url和及其对应的子网页的url,嵌套一层
def getAllUrl(url, opener):
	uop = opener.open(url, timeout = 1000);
	data = uop.read();
	linkre = re.compile('href="(.+?)"');
	for x in linkre.findall(data.decode('utf-8')):
		if 'http' in x:
			urlList.add(x);

# 获取所有的图片url
def getPicUrl(opener):
	for x in urlList:
		try:
			uop = opener.open(x, timeout=1000);
			data = uop.read();
			linkre = re.compile('<img src="(.*?)"');
			for img in linkre.findall(data.decode('utf-8')):
				path = x + '/' + img;
				imgList.add(path);
		except:
			print('URL ERROR:%s...' % x);


# 保存图片		
def saveImg():
	i = 1;
	if not os.path.exists('img_T'):
		os.mkdir('img_T');
	
	for x in imgList:
		try:
			pic = requests.get(x, timeout=1000);
		except:
			print('IMG URL ERROR:%s...' % x);
		path = 'img_T\\' + str(i) + os.path.splitext(x)[1];
		with open(path, 'wb') as f:
			f.write(pic.content);
			print('图片%s正在下载...' %str(i));
		i = i + 1;
		
		
if __name__ == '__main__':
	# 输入父网址url
	pURL = input('please enter a url:');
	
	# 创建opener
	opener = makeMyOpener();
	
	# 获取url和imgurl
	getAllUrl(pURL, opener);
	# 把首页也加入
	urlList.add(pURL);
	getPicUrl(opener);
	
	# 保存img
	saveImg();
	
	# 保存url和imgurl,这里不需要
	#saveFileUrl();
	#saveFileImgUrl();
	
