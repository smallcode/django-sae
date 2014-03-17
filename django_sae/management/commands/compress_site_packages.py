# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import zipfile
import time


def zip_folder(folder_dir, zip_name, include_empty_folder=True):
    root_length = len(folder_dir) + 1
    empty_folders = []
    zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for root, folders, files in os.walk(folder_dir):
        empty_folders.extend([folder for folder in folders if os.listdir(os.path.join(root, folder)) == []])
        for name in files:
            file_name = os.path.join(root, name)
            zip_file.write(file_name, file_name[root_length:])
        if include_empty_folder:
            for folder in empty_folders:
                zif = zipfile.ZipInfo(os.path.join(root, folder) + "/")
                zip_file.writestr(zif, "")
        empty_folders = []
    zip_file.close()


class Command(BaseCommand):
    def handle(self, *args, **options):
        folder_dir = getattr(settings, 'PACKAGES_DIR', None)
        if folder_dir is None:
            raise CommandError('PACKAGES_DIR is None, it should be set in settings')
        zip_name = options.get('zip_name', 'site-packages%s.zip' % int(time.time()))
        zip_folder(folder_dir, zip_name)
        self.stdout.write("update and compress to file: %s success" % zip_name)