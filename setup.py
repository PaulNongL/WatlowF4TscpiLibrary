'''setup script for this module'''

from setuptools import setup

def readme():
    '''pull iin the readme file for the long description'''
    with open('README.md') as rfile:
        return rfile.read()

setup(
    name='f4tscpi',
    version='0.1.0',
    description='A library for interfacing with Watlow F4T using SCPI method',
    long_description=readme(),
    url='https://github.com/PaulNongL/WatlowF4TscpiLibrary/tree/f4tscpi',
    author='Paul Nong-Laolam<Espec North America>',
    author_email='pnong-laolam@espec.com',
    license='MIT',
    packages=['f4tscpi'],
    zip_safe=False,
    keywords='F4T',
    include_package_data=True,
    scripts=['bin/f4t_run.py'],

    classifiers=[
        'Programming Language :: Python :: 3.6.8',
        'Programming Language :: Python :: 3.7.3',
        'Programming Language :: Python :: 3.9.3',
    ]
)
