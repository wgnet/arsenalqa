from setuptools import setup, find_namespace_packages

from version import VERSION

setup(
    name='arsenalqa-db',
    version=VERSION,
    url='https://github.com/wgnet/arsenalqa',
    description='Extra for ArsenalQA package',
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
        'Intended Audience :: QA',
        'Topic :: Software Testing :: Microservice testing Tools',
        'License :: OSI Approved :: Apache License 2.0',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
  ],
)
