"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='ogame_stats',
    version='0.3.2',
    description='wrapper around public game statistics for https://ogame.org',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',
    url='https://github.com/erkandem/ogame_stats',
    author='Erkan Demiralay',
    author_email='erkan.dem@pm.me',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Simulation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='ogame',
    package_dir={'': 'ogame_stats'},
    packages=find_packages(where='ogame_stats', exclude=('docs', 'tests')),
    python_requires='>=3.6, <4',
    install_requires=['pandas', 'requests', 'xmltodict'],
    extras_require={  # Optional
        'test': ['coverage', 'pytest'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/erkandem/ogame_stats/issues',
        'Source': 'https://github.com/erkandem/ogame_stats/',
    },
)
