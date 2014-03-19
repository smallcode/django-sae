# coding=utf-8
import os
import sys
import pip
from django.conf import settings
from django.core.management.base import NoArgsCommand
from pip.commands import InstallCommand


class Command(NoArgsCommand):
    help = "Upgrade packages list in requirements."

    def handle_noargs(self, **options):
        if options.get('requirements', False):
            req_files = options["requirements"]
        elif os.path.exists("requirements.txt"):
            req_files = ["requirements.txt"]
        elif os.path.exists("requirements"):
            req_files = ["requirements/{0}".format(f) for f in os.listdir("requirements")
                         if os.path.isfile(os.path.join("requirements", f)) and
                         f.lower().endswith(".txt")]
        else:
            sys.exit("requirements not found")

        initial_args = ['install', '--upgrade', '--no-deps']
        [initial_args.extend(['--requirement', os.path.join(settings.BASE_DIR, req)]) for req in req_files]
        cmd_name, args = pip.parseopts(initial_args)

        InstallCommand().main(args)

