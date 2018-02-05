# -*- coding: utf-8 -*-
__author__ = 'liubo'
from setuptools import setup

setup(
    name='automation',
    version='1.0.0',
    author='liubo',
    author_email='602318557@qq.com',
    install_requires = ['jinja2','json_to_model'],
    description='iOS Code auto Generator',
    packages=['automation'],
    package_data={'automation': ['tpl/*.html']},
    license='MIT'
)
