from setuptools import setup, find_namespace_packages

from version import VERSION

setup(
    name='arsenalqa-http',
    version=VERSION,
    url='https://github.com/wgnet/arsenalqa',
    description='Extra for ArsenalQA package',
    author='Wargaming.net QA group',
    license='Apache License 2.0',
    packages=find_namespace_packages(
        include=('arsenalqa.transports.http', 'arsenalqa.transports.http.*'),
    ),
    zip_safe=False,
    install_requires=[
        'requests>=2.0,<3.0',
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
