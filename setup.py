from setuptools import setup, find_packages

setup(
    name='spacewalk',
    version=open('VERSION').read().strip(),
    author='MotiveMetrics',
    install_requires=[
        '-e git+https://github.com/tiptapinc/zerog.git@SV2-2416-couchbase3#egg=zerog',
        'marshmallow-jsonschema',
        'pytest',
        'pytest-cov',
        'pytest-tornado'
    ],
    packages=find_packages(exclude=["tests"])
)
