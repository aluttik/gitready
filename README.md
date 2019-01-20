<h1 align="center">GitReady</h1>
<h3 align="center">Initializes a git repo for a python project</h3>

<p align="center">
<a href="https://travis-ci.org/aluttik/gitready"><img alt="Build status" src="https://img.shields.io/travis/aluttik/gitready/master.svg"></a>
<a href="https://pypi.org/project/gitready/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/gitready.svg"></a>
<a href="https://pypi.org/project/gitready"><img alt="Supported Python versions" src="https://img.shields.io/pypi/pyversions/gitready.svg"></a>
<a href="https://pypi.org/project/gitready"><img alt="License: Apache 2.0" src="https://img.shields.io/pypi/l/gitready.svg"></a>
<a href="https://github.com/aluttik/gitready"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Installation

    pip install gitready

## Command Line Interface

```
usage: gitready [--license <license>] [--pypi <project>] [-h] [-V] user/repo

Creates a new python project from scratch.

positional arguments:
  user/repo            GitHub user and repository names.

optional arguments:
  --license <license>  Which open source license to use. [default: mit]
                       [possible values: apache2, bsd, gplv3, mit, mozilla]
  --pypi <project>     PyPI name if different than the repo name.
  -h, --help           Print this help message and exit.
  -V, --version        Show version information and exit.
```
