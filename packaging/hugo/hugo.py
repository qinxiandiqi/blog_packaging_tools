#!/usr/bin/env python

from packaging.packer import *


class HugoPacker(Packer):
    """hugo打包器"""

    def __init__(self, cp: ConfigParser):
        super().__init__(cp)

    def pack(self, blog: Blog):
        """打包博客"""
        return super().pack(blog)
