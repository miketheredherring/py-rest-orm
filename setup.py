import codecs
import os
import re

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

here = os.path.abspath(os.path.dirname(__file__))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='py-rest-orm',
    version=find_version('pyrestorm', '__init__.py'),
    packages=['pyrestorm', ],
    include_package_data=True,
    license='MIT License',
    description='Generic Python REST ORM. Inspired by Django. Powered by Requests.',
    long_description=README,
    install_requires=[
        'requests>=2.9.1',
        'six==1.10.0',
    ],
    url='',
    author='Mike Hearing',
    author_email='mhearing@genepeeks.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
