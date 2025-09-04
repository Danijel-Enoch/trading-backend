#  Drakkar-Software trading-backend
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
# from distutils.extension import Extension
from setuptools import find_packages
from setuptools import setup

VERSION = "1.2.41"
PROJECT_NAME = "trading-backend"

PACKAGES = find_packages(exclude=["tests"])


# long description from README file
with open('README.md', encoding='utf-8') as f:
    DESCRIPTION = f.read()

# Process requirements.txt to handle Git URLs
def get_install_requires():
    """Parse requirements.txt and handle Git URLs properly"""
    with open('requirements.txt') as f:
        requirements = []
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            # Handle Git URLs - these need to be installed via pip, not setup.py
            if line.startswith('git+'):
                # For setup.py, we'll use the package name that the Git repo provides
                # Users will need to install via pip with requirements.txt
                if 'ccxt' in line:
                    requirements.append('ccxt>=4.4.85')
            else:
                requirements.append(line)
        return requirements

REQUIRED = get_install_requires()
REQUIRES_PYTHON = '>=3.8'

setup(
    name=PROJECT_NAME,
    version=VERSION,
    url='https://github.com/Danijel-Enoch/trading-backend',
    license='LGPL-3.0',
    author='Drakkar-Software',
    author_email='contact@drakkar.software',
    description='Trading tools with weex exchange support',
    packages=PACKAGES,
    include_package_data=True,
    long_description=DESCRIPTION,
    tests_require=["pytest"],
    test_suite="tests",
    zip_safe=False,
    data_files=[],
    install_requires=REQUIRED,
    python_requires=REQUIRES_PYTHON,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
