#!/usr/bin/env python

import os
import string

from blogs.blog import *
from utils import markdown


class HugoPacker(Packer):
    """hugo打包器"""

    def __init__(self, cp: ConfigParser, output_dir: str):
        super().__init__(cp)
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        hugo_dir = os.path.split(os.path.abspath(__file__))[0]
        self.default_tempalte_path = os.path.join(hugo_dir, "template.md")
        with open(self.default_tempalte_path) as template_file:
            self.default_template = string.Template(template_file.read())

    def pack_post(self, post: Post):
        md = post.markdown
        post_dir = os.path.join(self.output_dir, post.name.replace(' ', ''))
        if not os.path.exists(post_dir):
            os.makedirs(post_dir)
        images = markdown.download_markdown_images(md, post_dir)
        for image in images:
            md = md.replace(image.url, image.file_name)
        summary = post.summary.replace("\\", "\\\\").replace("\"", "\\\"")
        series = [f'"{x}"' for x in post.categories]
        categories = series[:]
        if post.type is PostType.Translate:
            categories.insert(0, '"翻译"')
        tags = [f'"{x}"' for x in post.tags]
        post_txt = self.default_template.safe_substitute(
            title=f'"{post.name}"',
            date=post.publish_time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            authors=f'"{post.author}"',
            summary=f'"{summary}"',
            series=f'{", ".join(series)}',
            categories=f'{", ".join(categories)}',
            tags=f'{", ".join(tags)}',
            images="",
            read_num=post.read_num,
            comment_num=post.comment_num,
            content=md
        )
        with open(os.path.join(post_dir, "index.md"), "w") as post_file:
            post_file.write(post_txt)
