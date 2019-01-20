<h1 align="center">{{ project }}</h1>
<h3 align="center">summary</h3>

<p align="center">
<a href="https://travis-ci.org/{{ github_user }}/{{ project }}"><img alt="Build status" src="https://img.shields.io/travis/{{ github_user }}/{{ project }}/master.svg"></a>
<a href="https://pypi.org/project/{{ pypi_project }}/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/{{ pypi_project }}.svg"></a>
<a href="https://pypi.org/project/{{ pypi_project }}"><img alt="Supported Python versions" src="https://img.shields.io/pypi/pyversions/{{ pypi_project }}.svg"></a>
<a href="https://pypi.org/project/{{ pypi_project }}"><img alt="License: {{ license }}" src="https://img.shields.io/pypi/l/{{ pypi_project }}.svg"></a>
<a href="https://github.com/{{ github_user }}/{{ project }}"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

## Installation

    pip install {{ pypi_project }}
