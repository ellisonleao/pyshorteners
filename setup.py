# coding: utf8

from setuptools import setup

setup(
    name='pyshorteners',
    version='0.2.2',
    license='MIT',
    description=('A simple URL shortening Python Lib, implementing '
                 'the most famous shorteners.'),
    long_description=open('README.rst').read(),
    author=u'Ellison Leão',
    author_email='ellisonleao@gmail.com',
    url='https://github.com/ellisonleao/pyshorteners/',
    platforms='any',
    zip_save=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['requests', ],
    test_suite="test_shorteners",
    packages=['pyshorteners'],
    namespace_packages=['pyshorteners'],
)
