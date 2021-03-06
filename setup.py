# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.1.7'


setup(
    name='pywe-decrypt',
    version=version,
    keywords='Wechat Weixin Decrypt',
    description='Wechat Decrypt Module for Python.',
    long_description=open('README.rst').read(),

    url='https://github.com/sdkwe/pywe-decrypt',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['pywe_decrypt'],
    py_modules=[],
    # Python3.x
    # from Crypto.Util.py3compat import byte_string ImportError: cannot import name 'byte_string'
    # pip3 uninstall pycrypto
    # pip3 uninstall pycryptodome
    # pip3 install pycryptodome
    install_requires=['pycryptodome', 'pywe-sign>=1.0.8', 'pywe_utils', 'pywe-xml>=1.0.3'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
