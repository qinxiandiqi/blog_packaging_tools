#!/usr/bin/env python3

import os
import zipfile


def find_file_in_dir_with_filename(dir: str, target_name: str):
    """在指定目录下查询包含target_name字符的文件路径"""
    for fpaths, dirs, fnames in os.walk(dir):
        for name in fnames:
            if target_name in name:
                return os.path.join(fpaths, name)


def zip_dir(dir: str, zip_file_path: str):
    """将dir目录的内容压缩到zip_file_path文件"""
    print(f"start zip dir: {dir}")
    zip_file = zipfile.ZipFile(
        zip_file_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=5)
    for fpaths, dirs, fnames in os.walk(dir):
        for name in fnames:
            child_file_path = os.path.join(fpaths, name)
            zip_file.write(child_file_path)
            print(f"zip file: {child_file_path}")
    zip_file.close()
    print(f"done: zip dir SUCCESS to {zip_file_path}")
