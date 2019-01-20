#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
Creates a new python project from scratch

Usage: gitready [options] USER/REPO

Options:
  -h, --help         print this help text and exit
  --license LICENSE  specify a license file to include [default: mit]
  --pypi PROJECT     name to use for PyPI if different than repo name

Licenses:
  apache2, bsd, gplv3, mit, mozilla
"""
import datetime
import io
import os
import shlex
import subprocess
import sys

if sys.version_info[0] < 3:
    input = raw_input

import docopt
import jinja2

# import requests

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


def parse_args():
    args = docopt.docopt(__doc__)
    if args["USER/REPO"].count("/") != 1:
        raise docopt.DocoptExit()
    args["USER"], args["REPO"] = args.pop("USER/REPO").split("/")
    return args


def run_command(command):
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode("utf-8")


def render_file(context, src, dst):
    src_path = os.path.join(os.path.dirname(os.path.dirname(HERE)), src)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(src_path)))
    text = env.get_template(os.path.basename(src_path)).render(**context)
    dst_path = os.path.join(os.getcwd(), context["project"], dst)
    with io.open(dst_path, "w", encoding="utf-8") as fd:
        fd.write(text + "\n")


def check_pypi_not_taken(project):
    r = requests.get("https://pypi.org/project/" + project)
    if r.status_code != 404:
        raise Exception("PyPI project already taken: " + project)


def check_github_not_taken(user, repo):
    r = requests.get("https://github.com/{}/{}/".format(user, repo))
    if r.status_code != 404:
        raise Exception("GitHub project already taken: {}/{}".format(user, repo))


def get_author_email():
    output = run_command("git --no-pager config --list --global")
    config = dict(line.split("=", 1) for line in output.splitlines())
    author, email = config.get("user.name"), config.get("user.email")
    if author is None or email is None:
        raise Exception("Could not find user.name and user.email in global git config")
    #     r = requests.get("https://api.github.com/users/" + user)
    #     data = r.json()
    #     if author is None:
    #         author = data['name']
    #     if email is None:
    #         email = data['email']
    return author, email


def initialize_repo(user, repo):
    try:
        cwd = os.getcwd()

        # create and enter the project directory
        project_dir = os.path.join(cwd, repo)
        os.mkdir(project_dir)
        os.chdir(project_dir)

        # create source and tests directories
        os.mkdir(repo)
        os.mkdir("tests")

        # run git init
        run_command("git init")

        # add remote origin
        remote_url = "git@github.com:{}/{}.git".format(user, repo)
        run_command("git remote add origin " + remote_url)
    finally:
        os.chdir(cwd)


def main():
    args = parse_args()

    github_user = args["USER"]
    project_name = args["REPO"]
    pypi_project = args["REPO"] if args["--pypi"] is None else args["--pypi"]
    license = args["--license"].lower()
    author, email = get_author_email()

    # check_pypi_not_taken(pypi_project)
    # check_github_not_taken(github_user, project_name)
    initialize_repo(github_user, project_name)

    context = {
        "year": datetime.datetime.now().year,
        "author": author,
        "email": email,
        "github_user": github_user,
        "project": project_name,
        "pypi_project": pypi_project,
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
