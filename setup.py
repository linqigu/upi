# -*- coding:utf-8 -*-
"""
@author: LQG
@mail: linqigu@163.com
@file: config.py
@time: 2021/11/10 22:59
@desc: 
"""
from setuptools import setup, find_packages

from upi import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='upi',
    version=__version__,
    license='MIT',
    author="linqigu",
    author_email="linqigu@163.com",
    description="pay sdk",
    url='https://github.com/linqigu/upi',
    download_url='https://github.com/linqigu/upi',
    # 关键词
    keywords=['upi', 'pay', 'wxPay'],
    python_requires='>=3.6',
    install_requires=[
        'requests', 'bs4', 'lxml'
    ],
    platforms='any',
    packages=find_packages(),
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
