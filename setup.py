from setuptools import setup, find_packages
from os import path

setup(
    name="record_location",
    version="0.0.1",
    description="A tool for stashing information from Life360 into Influx.",
    author="Kodey Converse",
    author_email="kodey@krconv.com",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": ["record-location=record_location.__main__:main"]},
    install_requires=["attrs", "influxdb", "loguru", "requests", "schedule"],
)
