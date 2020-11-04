from setuptools import setup, find_namespace_packages

from version import VERSION

setup(
    name='arsenalqa-websocket',
    version=VERSION,
    url='https://github.com/wgnet/arsenalqa',
    description='Extra for ArsenalQA package',
    author='Wargaming.net QA group',
    license='Apache License 2.0',
    packages=find_namespace_packages(
        include=('arsenalqa.transports.websocket', 'arsenalqa.transports.websocket.*'),
    ),
    zip_safe=False,
    install_requires=[
        'websockets==8.1',
    ],
    python_requires='>=3.7',
    keywords=['TESTING', 'MICROSERVICES'],
    classifiers=[
        'Intended Audience :: QA',
        'Topic :: Software Testing :: Microservice testing Tools',
        'License :: OSI Approved :: Apache License 2.0',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
  ],
)
