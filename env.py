#!/usr/bin/env python3

import os
import platform


def get_system_lib_dir_name():
    """
        获取依赖系统类型的库文件夹名
    """
    sys_type = platform.system()
    if sys_type == 'Darwin':
        return 'macos'
    elif sys_type == 'Windows':
        return 'win'
    elif sys_type == "Linux":
        return 'linux'


# 当前目录
current_dir_path = os.path.split(os.path.abspath(__file__))[0]

# 库目录
lib_path = os.path.join(current_dir_path, "lib")
print("lib_path: " + lib_path)

# 依赖操作系统的库目录
sys_lib_path = os.path.join(lib_path, get_system_lib_dir_name())
print("lib of system: " + sys_lib_path)