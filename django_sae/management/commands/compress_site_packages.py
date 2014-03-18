# coding=utf-8
import os
import sys
import zipfile
import time
from distutils.sysconfig import get_python_lib
from django.core.management.base import NoArgsCommand
from django_extensions.management.commands import clean_pyc


def zip_folder(folder_path, zip_name, include_empty_folder=True, filter_root_func=None):
    root_length = len(folder_path) + 1
    empty_folders = []
    zip_file = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
    for root, folders, files in os.walk(folder_path):
        if filter_root_func(root[root_length:]):
            continue
        empty_folders.extend([folder for folder in folders if os.listdir(os.path.join(root, folder)) == []])
        for f in files:
            file_name = os.path.join(root, f)
            zip_file.write(file_name, file_name[root_length:])
        if include_empty_folder:
            for folder in empty_folders:
                zif = zipfile.ZipInfo(os.path.join(root, folder) + "/")
                zip_file.writestr(zif, "")
        empty_folders = []
    zip_file.close()


class Command(NoArgsCommand):
    help = "Compress site-packages folder to a zip file."
    usage_str = "Usage: ./manage.py compress_site_packages"
    filter_name = ("_markerlib", "pip", "setuptools", "sae")

    def handle(self, path=None, name=None, **options):
        if path is None:
            path = get_python_lib()
        if name is None:
            name = "site-packages%s.zip" % int(time.time())

        # 用户可以上传和使用 .pyc 文件，注意 .pyc 文件必须是python2.7.3生成的，否则无效。
        # http://sae.sina.com.cn/doc/python/runtime.html#id3
        if options.get("clean_pyc", sys.version_info[0:3] != (2, 7, 3)):
            clean_pyc.Command().execute(path=path)

        def filter_root(root):
            package_name = root.split(os.path.sep)[0]
            if not package_name or package_name in self.filter_name or ".egg-info" in package_name:
                return True

        zip_folder(path, name, True, filter_root)
        self.stdout.write("compressed success:%s" % name)