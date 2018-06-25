# -*- coding: utf-8 -*-
from os.path import isdir

import pytest

pytestmark = [pytest.mark.slow, pytest.mark.system]


def run_common_tasks(venv, tests=True, flake8=True):
    if tests:
        venv.run('python setup.py test')

    venv.install('sphinx')  # required for doctest
    venv.run('python setup.py doctest')
    venv.run('python setup.py docs')
    venv.run('python setup.py --version')
    venv.run('python setup.py sdist')
    venv.run('python setup.py bdist')

    if flake8:
        venv.install('flake8')
        venv.run('flake8 --count')


def test_putup(venv, tmpdir):
    # Given a venv with pyscaffold installed,
    # when we run putup
    with tmpdir.as_cwd():
        venv.run('putup myproj')
    # then no error should be raised when running the common tasks
    with tmpdir.join('myproj').as_cwd():
        run_common_tasks(venv)


def test_putup_with_update(venv, tmpdir):
    # Given a venv with pyscaffold installed,
    with tmpdir.as_cwd():
        # and a project was already created
        venv.run('putup myproj')
        # when we run putup with the update flag
        venv.run('putup --update myproj')
    # then no difference should be found
    with tmpdir.join('myproj').as_cwd():
        git_diff = venv.run('git diff')
        assert git_diff.strip() == ''


def test_differing_package_name(venv, tmpdir):
    # Given a venv with pyscaffold installed,
    # when we run putup
    with tmpdir.as_cwd():
        venv.run('putup my-cool-proj -p myproj')
        # then the folder structure should respect the names
        assert isdir('my-cool-proj')
        assert isdir('my-cool-proj/src/myproj')
    # then no error should be raised when running the common tasks
    with tmpdir.join('my-cool-proj').as_cwd():
        run_common_tasks(venv)
