import os
from pathlib import Path

from setuptools import find_packages, setup

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def get_long_description():
    return open(os.path.join(ROOT_DIR, "README.md"), encoding="utf-8").read()


setup(
    name="netznoe-smartmeter-portal-api",
    version="1.1.0",
    license="MIT",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    include_package_data=True,
    package_dir={"": "src"},
    description="An unofficial python implementation of the NetzNÖ Smartmeter Portal API",
    author="Mathias Schuepany",
    url="https://github.com/schue30/NetzNoe-SmartmeterPortal-Api",
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
)
