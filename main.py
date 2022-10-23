#!/usr/bin/env python
# -*-coding:utf-8 -*-

import argparse
import configparser
import os
import env
from blogs import *

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

    blog = CSDNBlog(
        author_id=author_id, cookie=cookie, start_page=start_page, end_page=end_page)
    blog.scan()
