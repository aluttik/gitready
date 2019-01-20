#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import datetime
import io
import os
import shlex
import subprocess

from . import __version__

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


def parse_args(args=None):
    p = argparse.ArgumentParser(
        prog="gitready",
        description="Creates a new python project from scratch.",
        add_help=False,
    )
    p.add_argument(
        "user_repo", metavar="user/repo", help="GitHub user and repository names."
    )
    p.add_argument(
        "--license",
        default="mit",
        metavar="<license>",
        choices=["apache2", "bsd", "gplv3", "mit", "mozilla"],
        help="""Which open source license to use. [default: mit]
            [possible values: apache2, bsd, gplv3, mit, mozilla]""",
    )
    p.add_argument(
        "--pypi",
        default=None,
        metavar="<project>",
        help="PyPI name if different than the repo name.",
    )
    p.add_argument(
        "-h", "--help", action="help", help="Print this help message and exit."
    )
    p.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help="Show version information and exit.",
    )
    parsed = p.parse_args(args=args)

    if parsed.user_repo.count("/") != 1:
        p.error("invalid USER/REPO")
    else:
        parsed.user, parsed.repo = parsed.user_repo.split("/")
        del parsed.user_repo

    if parsed.pypi is None:
        parsed.pypi = parsed.repo

    return parsed


def run_command(command):
    args = shlex.split(command)
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out.decode("utf-8")


def render_file(context, src, dst):
    src_path = os.path.join(os.path.dirname(os.path.dirname(HERE)), src)
    with io.open(src_path, "r", encoding="utf-8") as fd:
        template = fd.read()
    dst_path = os.path.join(os.getcwd(), context["project"], dst)
    with io.open(dst_path, "w", encoding="utf-8") as fd:
        fd.write(template % context + "\n")


def check_pypi_not_taken(project):
    r = requests.get("https://pypi.org/project/" + project)
    if r.status_code != 404:
        raise Exception("PyPI project already taken: " + project)


def check_github_not_taken(user, repo):
    r = requests.get("https://github.com/{}/{}/".format(user, repo))
    if r.status_code != 404:
        raise Exception("GitHub project already taken: {}/{}".format(user, repo))


def get_author_email():
    output = run_command("git --no-pager config --list")
    config = dict(line.split("=", 1) for line in output.splitlines())
    author, email = config.get("user.name"), config.get("user.email")
    if not author or not email:
        raise Exception("Could not find user.name and user.email in global git config")
    #     r = requests.get("https://api.github.com/users/" + user)
    #     data = r.json()
    #     if author is None:
    #         author = data['name']
    #     if email is None:
    #         email = data['email']
    return author, email


def initialize_repo(user, repo, cwd=None):
    before = os.getcwd()
    if cwd is None:
        cwd = before

    try:
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
        os.chdir(before)


def main():
    args = parse_args()

    license = args.license.lower()
    author, email = get_author_email()

    # check_pypi_not_taken(args.pypi)
    # check_github_not_taken(args.user, args.repo)
    initialize_repo(args.user, args.repo)

    context = {
        "year": datetime.datetime.now().year,
        "author": author,
        "email": email,
        "github_user": args.user,
        "project": args.repo,
        "pypi_project": args.pypi,
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
    render_file(context, "files/init_py", args.repo + "/__init__.py")
    render_file(context, "files/main_py", args.repo + "/__main__.py")
    render_file(context, "files/tests_init_py", "tests/__init__.py")

    if license in ("apache2",):
        render_file(context, "files/notices/" + license, "NOTICE")


if __name__ == "__main__":
    main()
