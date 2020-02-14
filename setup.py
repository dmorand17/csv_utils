from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = [req for req in f.read().splitlines() if not req.startswith('#')]

setup(
    name='csv_utils',
    version='0.1.0-rc1',
    description='CSV Utility scripts',
    long_description=readme,
    author='Douglas Morand',
    author_email='dmorand@gmail.com',
    url='https://github.com/dmorand17/csv_utils',
    license=license,
    packages=find_packages(exclude=('tests', 'templates')),
    install_requires=requirements
)