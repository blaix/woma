from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='woma',
    version='0.0.0',
    description='A python web development framework',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/blaix/woma',
    author='Justin Blake',
    author_email='justin@blaix.com',
    packages=['woma'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=['property-caching>=1.0,<2.0', 'WebOb>=1.5,<2.0'],
    # TODO: move test requirements to tox
    extras_require={
        'dev': [
            'flake8',
            'flake8-quotes',
            'isort',
            'nose>=1.3,<2',
            'tdubs>=0.1,<0.2',
            'testtube>=1.0,<2',
            'spec>=1.3,<2',
        ]
    },
)
