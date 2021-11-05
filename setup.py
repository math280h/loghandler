from distutils.core import setup

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="loghandler",

    version="0.1.0",

    author="math280h",

    packages=setuptools.find_packages(include=['loghandler', 'loghandler.*']),

    include_package_data=True,

    url="https://github.com/math280h/loghandler",

    description="Python logging library with support for multiple destinations",

    long_description=long_description,
    long_description_content_type="text/markdown",

    install_requires=[
        'rich==10.12.0',
        'requests==2.26.0',
    ],
)
