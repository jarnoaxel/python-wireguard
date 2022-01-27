from setuptools import setup
from pathlib import Path
import os

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = os.environ.get('RELEASE_VERSION')

setup(name='python_wireguard',
      version=version,
      description='A python wrapper for controlling Wireguard',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='',
      author='jarnoaxel',
      license='MIT',
      packages=['python_wireguard'],
      include_package_data=True,
      zip_safe=False)