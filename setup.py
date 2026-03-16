import os
from setuptools import setup, find_packages

# Read version from OPENAPI_VERSION file
with open('OPENAPI_VERSION', 'r') as f:
    version = f.read().strip()

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='linkbreakers',
    version=version,
    description='Official Python SDK for the Linkbreakers API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Linkbreakers',
    author_email='support@linkbreakers.com',
    url='https://linkbreakers.com',
    project_urls={
        'Documentation': 'https://docs.linkbreakers.com',
        'Source': 'https://github.com/linkbreakers-com/linkbreakers-python',
        'Tracker': 'https://github.com/linkbreakers-com/linkbreakers-python/issues',
    },
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'urllib3>=1.25.3',
        'python-dateutil',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    keywords='linkbreakers url-shortener qr-code link-management api',
    license='MIT',
)
