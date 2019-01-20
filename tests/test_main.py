# -*- coding: utf-8 -*-
import pytest

from gitready.__main__ import get_author_email, parse_args, run_command, initialize_repo


def test_parse_args_splits_user_and_repo():
    parsed = parse_args(args=["foo/bar"])
    assert not hasattr(parsed, "user_repo")
    assert parsed.user == "foo"
    assert parsed.repo == "bar"


def test_parse_args_default_pypi_is_repo():
    parsed = parse_args(args=["foo/bar", "--pypi", "baz"])
    assert parsed.pypi == "baz"
    parsed = parse_args(args=["foo/bar"])
    assert parsed.pypi == "bar"


def test_parse_args_cant_split_user_repo():
    with pytest.raises(SystemExit):
        parse_args(args=["foo"])


def test_parse_args_license_is_uppercase():
    with pytest.raises(SystemExit):
        parse_args(args=["foo/bar", "--license", "BSD"])


@pytest.yield_fixture
def git_config():
    has_name = bool(run_command("git --no-pager config --list | grep user.name"))
    has_email = bool(run_command("git --no-pager config --list | grep user.email"))

    saved_name = run_command("git --no-pager config user.name").rstrip()
    saved_email = run_command("git --no-pager config user.email").rstrip()

    try:
        yield
    finally:
        if has_name:
            run_command("git --no-pager config user.name '%s'" % saved_name)
        else:
            run_command("git --no-pager config --system --unset-all user.name")
            run_command("git --no-pager config --global --unset-all user.name")
            run_command("git --no-pager config --local --unset-all user.name")

        if has_email:
            run_command("git --no-pager config user.email '%s'" % saved_email)
        else:
            run_command("git --no-pager config --system --unset-all user.email")
            run_command("git --no-pager config --global --unset-all user.email")
            run_command("git --no-pager config --local --unset-all user.email")


def test_get_author_email_both_were_found(git_config):
    run_command("git --no-pager config user.name foo")
    run_command("git --no-pager config user.email bar")
    got_name, got_email = get_author_email()
    assert got_name == "foo"
    assert got_email == "bar"


def test_get_author_email_author_not_found(git_config):
    run_command("git --no-pager config user.name ''")
    with pytest.raises(Exception):
        get_author_email()


def test_get_author_email_email_not_found(git_config):
    run_command("git --no-pager config user.email ''")
    with pytest.raises(Exception):
        get_author_email()


def test_initialize_repo_adds_remote_user(tmpdir):
    initialize_repo(user="foo", repo="bar", cwd=tmpdir.strpath)
    assert tmpdir.join("bar").check(dir=1)
    assert tmpdir.join("bar", "bar").check(dir=1)
    assert tmpdir.join("bar", "tests").check(dir=1)
    assert tmpdir.join("bar", ".git").check(dir=1)
    assert tmpdir.join("bar", ".git", "config").check(file=1)
    text = tmpdir.join("bar", ".git", "config").read_text("utf-8")
    assert "url = git@github.com:foo/bar.git" in text
