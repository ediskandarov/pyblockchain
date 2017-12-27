from setuptools import find_packages, setup


setup(
    name='pyblockchain',
    version='0.2.2',
    description='pyblockchain is a Python library for parsing blockchain data',
    url='https://github.com/toidi/pyblockchain',
    author='Eduard Iskandarov',
    author_email='eduard.iskandarov@yandex.ru',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='blockchain bitcoin altcoin',
    packages=find_packages(),
    install_requires=[
        'base58',
    ],
)
