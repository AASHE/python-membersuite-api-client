#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README.md file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='membersuite_api_client',
      version='0.1.7',
      description='MemberSuite API Client',
      author='AASHE',
      author_email='webdev@aashe.org',
      url='https://github.com/AASHE/python-membersuite-api-client',
      long_description=read("README.md"),
      packages=[
          'membersuite_api_client',
      ],
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3.4.3',
      ],
      include_package_data=True,
      install_requires=[
          "zeep>=0.26",
          "future==0.16.0",
          "lxml==3.7.0"
      ],
      )
