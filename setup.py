from setuptools import setup, find_packages

setup(
    name='spacewalk',
    version=open('VERSION').read().strip(),
    author='MotiveMetrics',
    install_requires=[
        'zerog',
        'marshmallow-jsonschema',
        'pytest',
        'pytest-cov',
        'pytest-tornado'
    ],
    packages=find_packages(exclude=["tests"])
)
