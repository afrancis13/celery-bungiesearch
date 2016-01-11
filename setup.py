# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


VERSION = (1, 2, 4)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))


install_requires = [
    'bungiesearch>=1.2.2',
    'celery==3.1.18',
    'Django>=1.4.3',
]


with open('README.rst') as f:
    readme = f.read()


setup(
    name='celery-bungiesearch',
    packages=find_packages(
        where='.',
        exclude=('tests',)
    ),
    version=__versionstr__,
    license='MIT',
    description='Celery signal processor for Bungiesearch',
    url='https://github.com/afrancis13/celery-bungiesearch',
    long_description=readme,
    author='Alex Francis',
    author_email='afrancis@berkeley.edu',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],
    install_requires=install_requires,
)
