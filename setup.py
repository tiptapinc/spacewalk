from setuptools import setup, find_packages

setup(
    name='spacewalk',
    version=open('VERSION').read().strip(),
    author='MotiveMetrics',
    install_requires=[
        '-e git+https://github.com/tiptapinc/zerog.git@0.0.36#egg=zerog',
        'marshmallow-jsonschema',
        'pytest',
        'pytest-cov',
        'pytest-tornado'
    ],
    packages=find_packages(exclude=["tests"])
)
