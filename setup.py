#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README.md file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='membersuite-api-client',
      version='0.1.12',
      description='MemberSuite API Client',
      author='AASHE',
      author_email='webdev@aashe.org',
      url='https://github.com/AASHE/python-membersuite-api-client',
      long_description=read("README.md"),
      packages=[
          'membersuite-api-client',
      ],
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Framework :: Django',
      ],
      include_package_data=True,
      )
