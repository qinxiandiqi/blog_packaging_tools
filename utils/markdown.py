#!/usr/bin/env python3

import hashlib
import os
import re
from itertools import chain
from typing import List

import requests


class MarkdownImage:
    def __init__(self, url: str, local_dir: str) -> None:
        self.url = url
        self.local_dir = local_dir
        if not os.path.exists(dir):
            os.makedirs(dir)

    def download_to_local(self):
        md5 = hashlib.md5()
        md5.update(self.url)
        file_name = f"{md5.hexdigest}.{self.url.split('.')[-1]}"
        self.local_file = os.path.join(self.local_dir, file_name)
        response = requests.request(url=self.url)
        with open(self.local_file, "wb") as file:
            file.write(response.content)


def download_markdown_images(markdown: str, dir: str) -> List[MarkdownImage]:
    """打包markdown文件中的图片资源

    Args:
        markdown: markdown文本
        dir: markdown文本中图片下载本地保存路径
    """
    if not os.path.exists(dir):
        os.makedirs(dir)

    images = []
    matches = re.compile(
        r"!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>").findall(markdown)
    if matches and len(matches) > 0:
        for url in list(chain(*matches)):
            if url and len(url) > 0:
                if re.match('((http(s?))|(ftp))://.*', url):
                    image = MarkdownImage(url=url, local_dir=dir)
                    image.download_to_local()
                    images.append(image)
    return images
