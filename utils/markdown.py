#!/usr/bin/env python3

import hashlib
import os
import re
from io import BytesIO
from itertools import chain
from typing import List

import requests
from PIL import Image


class MarkdownImage:
    def __init__(self, url: str, local_dir: str) -> None:
        self.url = url
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
        self.local_dir = local_dir

    def download_to_local(self):
        response = requests.get(url=self.url)
        image = Image.open(BytesIO(response.content))
        md5 = hashlib.md5()
        md5.update(self.url.encode("utf-8"))
        self.file_name = f"{md5.hexdigest()}.{image.format.lower()}"
        self.local_file = os.path.join(self.local_dir, self.file_name)
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
