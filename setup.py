from setuptools import setup
import re
import os
import sys


# https://packaging.python.org/guides/distributing-packages-using-setuptools/
# https://github.com/pypa/sampleproject
# Get the version from init
def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    version_match = re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                              init_py, re.MULTILINE).group(1)
    if version_match:
        return version_match
    raise RuntimeError('Unable to find version string.')


version = get_version('rest_framework')


# Publish args
if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print(" git tag -a {0} -m 'version {0}'".format(version))
    print(" git push --tags")
    sys.exit()


setup(
    version=version,
    # Rest of settings are in setup.cfg
)
