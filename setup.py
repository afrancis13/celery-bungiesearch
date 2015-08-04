# -*- coding: utf-8 -*-
from setuptools import setup


VERSION = (1, 0, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))


install_requires = [
    'Django>=1.4.3',
    'celery==3.1.18'
]

commit_id = '9b19e80da491e4f83bb4ce84691d803316602c6f'
dependency_links = [
    'git+ssh://git@github.com:afrancis13/bungiesearch.git@%s#egg=bungiesearch' % commit_id
]


with open('README.rst') as f:
    readme = f.read()


setup(
    name='celery-bungiesearch',
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
    dependency_links=dependency_links
)
