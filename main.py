#!/usr/bin/env python
# -*-coding:utf-8 -*-

import argparse
import configparser
import os
import time
import env
import blog

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--startPage", dest="start_page",
                        type=int, required=False, default=1)
    parser.add_argument("--endPage", dest="end_page",
                        type=int, required=False, default=100)
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page

    cp = configparser.ConfigParser()
    cp.read(os.path.join(env.current_dir_path, "config.ini"))
    author_id = cp.get("csdn", "author")
    cookie = cp.get("csdn", "cookie").encode("utf-8").decode("latin1")

    blogs = []
    for page in range(start_page, end_page + 1):
        page_blogs = blog.scan_blog_list_page(author_id=author_id, page=page)
        if len(page_blogs) == 0:
            break
        else:
            blogs.extend(page_blogs)
    for blog in blogs:
        blog.request_detail(cookie)
        print(blog.__dict__)
        time.sleep(1)

