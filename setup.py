import codecs
import os
import re
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)

        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        sys.exit(pytest.main(self.test_args))


# Set run-time dependencies
dependencies = [
    'requests',
    'pytz',
]

# Set test dependencies
test_dependencies = [
    'pytest-cov',
    'pytest',
]

# Set extra dependencies
extra_dependencies = {
    'security': [
        'pyOpenSSL>=0.14',
        'cryptography>=1.3.4',
        'idna>=2.0.0',
    ],
}

if sys.version_info < (2, 7):
    # Workaround for atexit._run_exitfuncs error when invoking `test` with
    # older versions of Python
    try:
        import multiprocessing
    except ImportError:
        pass


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # Intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

long_description = read('README.rst')

setup(name='unityapiclient',
      version=find_version('unityapiclient', '__init__.py'),
      description=('Client library for the Unity IDM APIs'),
      long_description=long_description,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'License :: OSI Approved :: Apache Software License',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      keywords='unity identity management rest api client library',
      author='Nicolas Liampotis',
      author_email='nliam@grnet.gr',
      url='http://eudat-b2access.github.io/unity-api-python-client',
      download_url='https://github.com/EUDAT-B2ACCESS/unity-api-python-client',
      license='Apache License 2.0',
      packages=['unityapiclient'],
      zip_safe=False,
      install_requires=dependencies,
      tests_require=test_dependencies,
      extras_require=extra_dependencies,
      python_requires='>=2.6,<2.8',
      cmdclass={'test': PyTest},
)
