#!/usr/bin/env python
# -*-coding:utf-8 -*-

from datetime import datetime
from fnmatch import translate
import imp
import requests
from bs4 import BeautifulSoup
import json
import html2text
from enum import Enum, unique

@unique
class BlogType(Enum):
    Original = 0
    Translate = 1

class Blog:
    """文章"""

    def __init__(self):
        self.id = ""
        self.publish_time = datetime.today()
        self.read_num = 0
        self.comment_num = 0
        self.name = ""
        self.tags = []
        self.categories = []
        self.type = BlogType.Original
        self.html = ""
        self.markdown = ""

    def request_detail(self, cookie):
        """获取文章详情数据"""
        url = f"https://blog-console-api.csdn.net/v1/editor/getArticle?id={self.id}"

        headers = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        }
        data = {"id": self.id}
        reply = requests.get(url, headers=headers, data=data)
        try:
            blog_json = reply.json()
            self.name = blog_json['data']['title']
            self.tags = blog_json['data']['tags'].split(',')
            self.categories = blog_json['data']['categories'].split(',')
            type = blog_json['data']['type']
            if type == 'original':
                self.type = BlogType.Original
            elif type == 'translated':
                self.type = BlogType.Translate
            self.html = blog_json['data']['content']
            self.markdown = blog_json['data']['markdowncontent']
            if len(self.markdown) <= 0:
                self.markdown =  html2text.html2text(self.html)
        except Exception as e:
            print("***********************************")
            print(e)
            print(url)


def scan_blog_list_page(author_id, page):
    """从博客分页获取文章列表基本信息
    """
    url = f'https://blog.csdn.net/{author_id}/article/list/{page}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
    response = requests.get(url, headers=headers)
    parser = BeautifulSoup(response.content, "html.parser")
    divs = parser.find_all(
        'div', attrs={'class': 'article-item-box csdn-tracking-statistics'})
    blogs = []
    for div in divs:
        try:
            blog = Blog()
            blog.id = div.attrs["data-articleid"]
            date = div.find('span', attrs={'class': 'date'}).get_text()
            blog.publish_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            nums = div.find_all('span', attrs={'class': 'read-num'})
            if len(nums) >= 1:
                blog.read_num = int(nums[0].get_text())
            if len(nums) >= 2:
                blog.comment_num = int(nums[1].get_text())
            blogs.append(blog)
        except:
            print('Wrong, ' + div)
    return blogs


if __name__ == '__main__':
    blogs = scan_blog_list_page("qinxiandiqi", 0)
    for blog in blogs:
        print(blog.__dict__)
