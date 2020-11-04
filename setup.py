from setuptools import setup, find_namespace_packages

from version import VERSION

setup(
    name='arsenalqa',
    version=VERSION,
    url='https://github.com/wgnet/arsenalqa',
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
