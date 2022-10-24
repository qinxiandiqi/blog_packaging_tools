#!/usr/bin/env python

from datetime import datetime
from typing import List
import requests
from bs4 import BeautifulSoup
import json
import html2text
import time
from blogs.blog import *


class CSDNBlog(Blog):
    """CSDN博客"""

    def __init__(self, cp: ConfigParser) -> None:
        super().__init__(cp)
        self.author_id = cp.get("csdn", "author")
        self.cookie = cp.get("csdn", "cookie").encode(
            "utf-8").decode("latin1")
        self.start_page = cp.getint("csdn", "start_page")
        self.end_page = cp.getint("csdn", "end_page")

    def _scan_posts(self) -> List:
        posts = []
        for page in range(self.start_page, self.end_page + 1):
            page_posts = self.__scan_posts_by_page(page=page)
            if len(page_posts) == 0:
                break
            else:
                posts.extend(page_posts)
        for post in posts:
            post.sync(self.cookie)
            print(post.__dict__)
            time.sleep(1)

    def __scan_posts_by_page(self, page: int) -> List:
        """扫描博客文章，从博客分页获取文章列表基本信息"""
        url = f'https://blog.csdn.net/{self.author_id}/article/list/{page}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'}
        response = requests.get(url, headers=headers)
        parser = BeautifulSoup(response.content, "html.parser")
        divs = parser.find_all(
            'div', attrs={'class': 'article-item-box csdn-tracking-statistics'})
        posts = []
        for div in divs:
            try:
                post = CSDNPost()
                post.id = div.attrs["data-articleid"]
                date = div.find('span', attrs={'class': 'date'}).get_text()
                post.publish_time = datetime.strptime(
                    date, "%Y-%m-%d %H:%M:%S")
                nums = div.find_all('span', attrs={'class': 'read-num'})
                if len(nums) >= 1:
                    post.read_num = int(nums[0].get_text())
                if len(nums) >= 2:
                    post.comment_num = int(nums[1].get_text())
                posts.append(post)
            except:
                print('Wrong, ' + div)
        return posts


class CSDNPost(Post):
    """CSDN博客文章内容"""

    def __init__(self, id: str = "", publish_time: datetime = ...,
                 read_num: int = 0, comment_num: int = 0, name: str = "",
                 tags: List[str] = ..., categories: List[str] = ..., type:
                 PostType = PostType.Original, html: str = "", markdown: str = ""):
        super().__init__(id, publish_time, read_num, comment_num,
                         name, tags, categories, type, html, markdown)

    def sync(self, cookie):
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
                self.type = PostType.Original
            elif type == 'translated':
                self.type = PostType.Translate
            self.html = blog_json['data']['content']
            self.markdown = blog_json['data']['markdowncontent']
            if len(self.markdown) <= 0:
                self.markdown = html2text.html2text(self.html)
        except Exception as e:
            print(e)
            print(url)
