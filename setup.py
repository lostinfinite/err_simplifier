from setuptools import setup, find_packages

setup(
    name='err_simplifier',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'colorama',
        'subprocess',
        'os'
    ],
    description='A package for simplifying error messages and CLI outputs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='ContentLTD',
    author_email='suppott@contentltd.net',
    url='https://github.com/lostinfinite/err_simplifier',
    license='MIT',
)
