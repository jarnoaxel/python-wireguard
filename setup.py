'''
Used for building the python_wireguard package.
'''
from pathlib import Path
import os
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = os.environ.get('RELEASE_VERSION')

setup(name='python_wireguard',
      version=version,
      description='A python wrapper for controlling Wireguard',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jarnoaxel/python-wireguard',
      author='jarnoaxel',
      license='GPL-3.0-or-later',
      packages=['python_wireguard'],
      include_package_data=True,
      keywords=['vpn', 'wireguard'],
      zip_safe=False)
