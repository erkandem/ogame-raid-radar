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
    name='ogame_data_api',
    version='0.3.2',
    description='wrapper around public game statistics for https://ogame.org',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',
    url='https://github.com/erkandem/ogame-data-api',
    author='Erkan Demiralay',
    author_email='erkan.dem@pm.me',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='ogame',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6, <4',
    install_requires=['pandas', 'requests', 'xmltodict'],
    extras_require={  # Optional
        'test': ['coverage', 'pytest'],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/erkandem/ogame-data-api/issues',
        'Source': 'https://github.com/erkandem/ogame-data-api/sampleproject/',
    },
)
