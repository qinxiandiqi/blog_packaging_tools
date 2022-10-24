#!/usr/bin/env python

import argparse
import configparser
import os
import env
from blogs import *
from hugo.hugo import HugoPacker
from packaging import *

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

    blog = CSDNBlog(cp=cp)
    blog.scan()

    packer = HugoPacker()
    packer.pack(blog=blog)
