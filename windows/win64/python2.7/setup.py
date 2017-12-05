#!/usr/bin/env python

from setuptools import setup, find_packages
setup(
    name="pyacrcloud",
    version="1.0.0",
    packages=find_packages(),

    package_data={
        '': ['*.txt', '*.rst'],
        'acrcloud': ['*.so', '*.pyd'],
    },

    author="ACRCloud",
    author_email="support@acrcloud.com",
    description='Python wrapper for acrcloud libraries',
    license='MIT',
    keywords="ACRCLoud Python SDK",
    url='https://github.com/acrcloud/acrcloud_sdk_python',
    zip_safe=False,
    # could also include long_description, download_url, classifiers, etc.
)
