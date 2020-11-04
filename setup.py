from os import path

from setuptools import setup, find_namespace_packages

from version import VERSION

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='arsenalqa',
    version=VERSION,
    url='https://github.com/wgnet/arsenalqa',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Wargaming.net QA group',
    license='Apache License 2.0',
    packages=find_namespace_packages(
        include=('arsenalqa', 'arsenalqa.*'),
        exclude=(
            'arsenalqa.transports.http',
            'arsenalqa.transports.amqp',
            'arsenalqa.transports.db',
            'arsenalqa.transports.websocket',
        )
    ),
    extras_require={
        'http': f'arsenalqa-http>={VERSION}',
        'amqp': f'arsenalqa-amqp>={VERSION}',
        'db': f'arsenalqa-db>={VERSION}',
        'websocket': f'arsenalqa-websocket>={VERSION}',
    },
    zip_safe=False,
    install_requires=[
        'python-dateutil==2.8.1',
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
