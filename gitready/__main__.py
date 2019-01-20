#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
Creates a new python project from scratch

Usage: git_ready [options] NAME

Options:
  -h, --help             print this help text and exit
  -l, --license LICENSE  specify a license file to include [default: mit]

Licenses:
  apache2, bsd, gplv3, mit, mozilla
"""
import datetime
import io
import os
import shlex
import shutil
import subprocess

import jinja2

HERE = os.path.realpath(__file__)


class License(object):
    def __init__(self, name, short=None):
        self.name = name
        self.short = short
        self.trove = "License :: OSI Approved :: " + name


LICENSES = {
    "apache2": License("Apache Software License", "Apache 2.0"),
    "bsd": License("BSD License", "BSD License"),
    "gplv3": License("GNU General Public License v3 (GPLv3)", "GPLv3"),
    "mit": License("MIT License", "MIT"),
    "mozilla": License("Mozilla Public License 2.0 (MPL 2.0)", "MPL 2.0"),
}


def run_command(command):
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode("utf-8")


def render_file(context, src, dst):
    src_path = os.path.join(os.path.dirname(os.path.dirname(HERE)), src)
    src_dirname = os.path.dirname(src_path)
    src_basename = os.path.basename(src_path)

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(src_dirname))
    text = env.get_template(src_basename).render(**context)

    dst_path = os.path.join(os.getcwd(), dst)
    with io.open(dst_path, "w", encoding="utf-8") as fd:
        fd.write(text + "\n")


def parse_args():
    from docopt import docopt

    return docopt(__doc__)


def main():
    args = parse_args()

    project_name = args["NAME"]
    license = args["--license"].lower()

    # create and enter the project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    os.mkdir(project_dir)
    os.chdir(project_dir)

    # create source and tests directories
    os.mkdir(project_name)
    os.mkdir("tests")

    # run git init
    run_command("git init")

    # get git config
    output = run_command("git --no-pager config --list --global")
    config = dict(line.split("=", 1) for line in output.splitlines())

    context = {
        "year": datetime.datetime.now().year,
        "author": config["user.name"],
        "email": config["user.email"],
        "github_user": "aluttik",
        "travis_user": "aluttik",
        "pypi_project": project_name,
        "project": project_name,
        "license": LICENSES[license].short,
        "license_trove": LICENSES[license].trove,
    }

    render_file(context, "files/licenses/" + license, "LICENSE")
    render_file(context, "files/CONTRIBUTING.md", "CONTRIBUTING.md")
    render_file(context, "files/README.md", "README.md")
    render_file(context, "files/MANIFEST.in", "MANIFEST.in")
    render_file(context, "files/requirements.txt", "requirements.txt")
    render_file(context, "files/gitignore", ".gitignore")
    render_file(context, "files/Makefile", "Makefile")
    render_file(context, "files/travis.yml", ".travis.yml")
    render_file(context, "files/tox.ini", "tox.ini")
    render_file(context, "files/setup_cfg", "setup.cfg")
    render_file(context, "files/setup_py", "setup.py")
    render_file(context, "files/init_py", project_name + "/__init__.py")
    render_file(context, "files/main_py", project_name + "/__main__.py")
    render_file(context, "files/tests_init_py", "tests/__init__.py")

    if license in ("apache2",):
        render_file(context, "files/notices/" + license, "NOTICE")


if __name__ == "__main__":
    main()
