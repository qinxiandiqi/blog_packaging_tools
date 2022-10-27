#!/usr/bin/env python

import configparser
import os

import env
from blogs import *

if __name__ == '__main__':
    cp = configparser.ConfigParser()
    cp.read(os.path.join(env.current_dir_path, "config.ini"))

    packer = HugoPacker(cp=cp, output_dir=os.path.join(env.output_dir, "hugo"))

    blog = CSDNBlog(cp=cp, packer=packer)
    blog.pack()