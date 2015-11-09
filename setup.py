#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools.command.test import test as TestCommand
import materials
import sys

with open('README.md') as readme_file:
    readme = readme_file.read()


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='materials',
    version=materials.__version__,
    description="Scraper for chemical compounds",
    long_description=readme,
    author="Boston University",
    author_email='fjansen@bu.edu',
    url='https://github.com/Hariri-Institute-SAIL/materials',
    packages=[
        'materials',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    cmdclass={'test': PyTest},
    license="MIT",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Natural Language :: English',
        "Programming Language :: Python :: 3"
    ],
    test_suite='tests',
    tests_require=['pytest'],
    extras_require={
        'testing': ['pytest'],
    }
)
