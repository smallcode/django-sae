# coding=utf-8
import os
import sys
import zipfile
import time
import re
from distutils.sysconfig import get_python_lib
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django_extensions.management.commands import clean_pyc, compile_pyc


def zip_folder(folder_path, zip_name, include_empty_folder=True, check_root=None, check_file=None):
    root_length = len(folder_path) + 1
    zip_file = zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED)
    for root, folders, files in os.walk(folder_path):
        short_root = root[root_length:]
        if check_root is None or check_root(short_root):
            empty_folders = [folder for folder in folders if os.listdir(os.path.join(root, folder)) == []]
            for f in files:
                if check_file is None or check_file(short_root, f):
                    file_name = os.path.join(root, f)
                    zip_file.write(file_name, file_name[root_length:])
            if include_empty_folder:
                for folder in empty_folders:
                    zif = zipfile.ZipInfo(os.path.join(root, folder) + "/")
                    zip_file.writestr(zif, "")
    zip_file.close()


class Command(NoArgsCommand):
    help = "Compress site-packages folder to a zip file."
    usage_str = "Usage: ./manage.py compress_site_packages"
    filter_modules = ("_markerlib", "pip", "setuptools", "sae", "MySQLdb", "lxml", "PIL",
                      "werkzeug", "prettytable", "yaml", "argparse", "grizzled", "sqlcmd", "enum",
                      "test", "tests", "_mysql", "_mysql_exceptions", "_mysql",
                      "easy_install", "pkg_resources")

    @classmethod
    def check_root(cls, root):
        module_name = root.split(os.path.sep)[0]
        if module_name in cls.filter_modules or "." in module_name:
            return False
        return True

    @classmethod
    def check_file(cls, root, f):
        if not root:
            file_name, extend_name = os.path.splitext(f)
            if file_name in cls.filter_modules or extend_name in ['.egg', '.txt', '.pth']:
                return False
        return True

    @staticmethod
    def get_wsgi_file():
        return os.path.join(settings.BASE_DIR, 'index.wsgi')

    @staticmethod
    def replace_site_packages(path, name):
        if os.path.exists(path):
            with open(path) as rf:
                text = rf.read()
                m = re.search("sys.path.insert\(0, os.path.join\(root, '(?P<name>.+)'\)\)", text)
                if m:
                    with open(path, 'w') as wf:
                        wf.write(text.replace(m.group('name'), name))

    def handle(self, path=None, name=None, **options):
        if path is None:
            path = get_python_lib()
        if name is None:
            name = "site-packages%s.zip" % int(time.time())

        # 用户可以上传和使用 .pyc 文件，注意 .pyc 文件必须是python2.7.3生成的，否则无效。
        # http://sae.sina.com.cn/doc/python/runtime.html#id3
        if options.get("clean_pyc", sys.version_info[0:3] != (2, 7, 3)):
            clean_pyc.Command().execute(path=path, verbosity=1)
        else:
            compile_pyc.Command().execute(path=path, verbosity=1)

        zip_folder(path, name, True, self.check_root, self.check_file)
        self.replace_site_packages(self.get_wsgi_file(), name)
        self.stdout.write("compressed success:%s" % name)