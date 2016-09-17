# -*- coding: UTF-8 -*-
import httplib
import urllib2
import gzip
import StringIO
import os
import time
from bs4 import BeautifulSoup


class book_parser(object):
    """docstring for book_parser"""

    def __init__(self, novel_name, host):
        super(book_parser, self).__init__()
        self.host = host
        self.novel_name = novel_name
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    def gUnziper(self, content):
        compressedfile = StringIO.StringIO(content)
        gUnziper = gzip.GzipFile(fileobj=compressedfile)
        uncompressedData = gUnziper.read()
        return uncompressedData

    def getDirectory(self, direct_link):
        target_file_name = self.novel_name + '/' + 'directory.txt'
        (base, filename) = os.path.split(target_file_name)
        if not os.path.exists(base):
            os.makedirs(base)
        file = open(target_file_name, 'w')
        conn = httplib.HTTPConnection(self.host)
        request = conn.request('GET', direct_link, '', self.header)
        response = conn.getresponse()
        webContent = self.gUnziper(response.read())
        conn.close()
        soup = BeautifulSoup(webContent, 'html5lib')
        titleList = soup.select("#list > dl > dd > a")
        for title in titleList:
            record = unicode(title.string) + '\t' + title['href'] + '\n'
            file.write(record.encode('utf-8'))

    def getChapters(self,start):
        directoryFile = open(self.novel_name + '/' + 'directory.txt', 'r')
        title = directoryFile.readline()
        iterate = 0
        while(title):
            if(iterate < start):
                iterate += 1
                title = directoryFile.readline()
                continue
            title_name = title.split('\t')[0].split()[0]
            title_link = title.split('\t')[1]
            print "parsing chapter " + title_name
            self.getChapter(title_link, title_name)
            title = directoryFile.readline()
            iterate += 1
            # time.sleep(5)
        directoryFile.close()

    def getChapter(self, url, name):
        file = open(self.novel_name + '/' + name.decode('utf-8') + '.txt', 'w')
        target_url = "http://" + self.host + url
        request = urllib2.Request(url=target_url, headers=self.header)
        request.add_header('Connection', 'keep-alive')
        request.add_header('Host', 'www.biquge.com.tw')
        response = urllib2.urlopen(request)
        webContent = self.gUnziper(response.read())
        soup = BeautifulSoup(webContent, 'html5lib')
        for item in soup.select("#content"):
            content = unicode(item)
            file.write(content.encode('utf-8'))
        file.close()



novel_name = '异常生物见闻录'
BP = book_parser(novel_name.decode('utf-8'), 'www.biquge.com.tw')
#BP.getDirectory('/4_4029/')
BP.getChapters(1038)
