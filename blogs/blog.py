#!/usr/bin/env python

from datetime import datetime
from typing import List
from enum import Enum, unique
from configparser import ConfigParser


class Blog:
    """博客"""

    def __init__(self, cp: ConfigParser) -> None:
        self.cp = cp
        self.posts = []

    def scan(self):
        """扫描博客文章"""
        self.posts = self._scan_posts()

    def _scan_posts(self) -> List:
        """扫描博客文章"""
        return []


@unique
class PostType(Enum):
    """文章类型：原创、翻译"""
    Original = 0
    Translate = 1


class Post:
    """文章"""

    def __init__(self, id: str = "", publish_time: datetime = datetime.today(),
                 read_num: int = 0, comment_num: int = 0, name: str = "",
                 tags: List[str] = [], categories: List[str] = [],
                 type: PostType = PostType.Original,
                 html: str = "", markdown: str = ""):
        self.id = id
        self.publish_time = publish_time
        self.read_num = read_num
        self.comment_num = comment_num
        self.name = name
        self.tags = tags
        self.categories = categories
        self.type = type
        self.html = html
        self.markdown = markdown
