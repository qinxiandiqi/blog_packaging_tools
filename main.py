#!/usr/bin/env python

import configparser
import os

import env
from blogs import *
from packaging import *

if __name__ == '__main__':
    cp = configparser.ConfigParser()
    cp.read(os.path.join(env.current_dir_path, "config.ini"))

    blog = CSDNBlog(cp=cp)
    blog.scan()

    packer = HugoPacker()
    packer.pack_blog(blog=blog)
