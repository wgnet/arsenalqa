from os import path

from setuptools import setup, find_namespace_packages

from version import VERSION

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='arsenalqa-db',
    version=VERSION,
    url='https://github.com/wgnet/arsenalqa',
    description='Extra for ArsenalQA package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Wargaming.net QA group',
    license='Apache License 2.0',
    packages=find_namespace_packages(
        include=('arsenalqa.transports.db', 'arsenalqa.transports.db.*'),
    ),
    zip_safe=False,
    install_requires=[
        'sqlalchemy==1.3.17',
        'pypika==0.37.15',
    ],
    python_requires='>=3.7',
    keywords=['TESTING', 'MICROSERVICES'],
    classifiers=[
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
