#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README.md file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='membersuite_api_client',
      version="1.1.5",
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
          'Programming Language :: Python :: 3.4',
      ],
      include_package_data=True,
      install_requires=["future==0.16.0",
                        "retrying>=1.3.3",
                        "zeep>=0.26"]
      )
