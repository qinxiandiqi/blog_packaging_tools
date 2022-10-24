#!/usr/bin/env python

from packaging.packer import *
from utils import markdown


class HugoPacker(Packer):
    """hugo打包器"""

    def __init__(self, cp: ConfigParser, output_dir: str):
        super().__init__(cp)
        self.output_dir = output_dir

    def pack_post(self, post: Post):
        md = post.markdown
        markdown.download_markdown_images(md, self.output_dir)
        return super().pack_post(post)

    def pack_blog(self, blog: Blog):
        """打包博客"""
        for post in blog.posts:
            self.pack_post(post)
