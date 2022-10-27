#!/usr/bin/env python

from configparser import ConfigParser
from datetime import datetime
from enum import Enum, unique
from types import FunctionType
from typing import Callable, List


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


class Packer:
    def __init__(self, cp: ConfigParser):
        pass

    def pack_post(self, post: Post):
        """打包博客文章"""
        pass


class Blog:
    """博客"""

    def __init__(self, cp: ConfigParser, packer: Packer) -> None:
        self.cp = cp
        self.packer = packer
        self.posts: List[Post] = []

    def scan(self) -> None:
        """扫描博客文章"""
        self.posts = self._scan_posts()

    def pack(self) -> None:
        """打包博客文章"""
        self.posts = self._scan_posts(
            action=lambda p: self.packer.pack_post(p))

    def _scan_posts(self, action: Callable[[Post], None] = None) -> List[Post]:
        """扫描博客文章"""
        return []
