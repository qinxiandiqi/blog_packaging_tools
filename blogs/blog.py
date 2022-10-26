#!/usr/bin/env python

from configparser import ConfigParser
from datetime import datetime
from enum import Enum, unique
from typing import List


@unique
class PostType(Enum):
    """文章类型：原创、翻译"""
    Original = 0
    Translate = 1


class Post:
    """文章"""

    def __init__(self, id: str = "", author: str = "",
                 publish_time: datetime = datetime.today(),
                 read_num: int = 0, comment_num: int = 0, name: str = "",
                 tags: List[str] = [], categories: List[str] = [],
                 type: PostType = PostType.Original, summary: str = "",
                 html: str = "", markdown: str = ""):
        self.id = id
        self.author = author
        self.publish_time = publish_time
        self.read_num = read_num
        self.comment_num = comment_num
        self.name = name
        self.tags = tags
        self.categories = categories
        self.type = type
        self.summary = summary
        self.html = html
        self.markdown = markdown


class Blog:
    """博客"""

    def __init__(self, cp: ConfigParser) -> None:
        self.cp = cp
        self.posts: List[Post] = []

    def scan(self) -> None:
        """扫描博客文章"""
        self.posts = self._scan_posts()

    def _scan_posts(self) -> List[Post]:
        """扫描博客文章"""
        return []
