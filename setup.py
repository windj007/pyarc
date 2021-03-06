import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyarc",
    version = "0.0.1",
    author = "Roman Suvorov",
    author_email = "windj007@gmail.com",
    description = ("Yet another REST client for Python that allows asynchronous and batch requests via Requests and ERequests"),
    license = "BSD",
    keywords = "rest client",
    url = "http://packages.python.org/pyarc",
    packages=['pyarc', 'pyarc.backends', 'pyarc.tests'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: WWW/HTTP",
        "License :: OSI Approved :: BSD License",
    ],
    requires = ['requests', 'erequests', 'pytz'],
    test_suite = "pyarc.tests.all_tests"
)