#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

from distutils.extension import Extension

setup(
    name='gpiodev',
    version='0.0.1',
    description='Library to operate GPIO pins via character device',
    long_description=''.join(open('README.md').readlines()),
    long_description_content_type="text/markdown",
    keywords='gpio, raspberry-pi',
    author='Aleksandra Fedorova',
    author_email='alpha@bookwar.info',
    url="https://github.com/bookwar/python-gpiodev",
    license='Apache 2.0',
    packages=find_packages(),
    package_data={
        'gpiodev': ['libgpioctl.so'],
    },
    ext_modules=[
        Extension('gpiodev.libgpioctl', ['gpiodev/src/gpioctl.c']),
    ],
    headers=['gpiodev/src/gpioctl.h'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        ]
)
