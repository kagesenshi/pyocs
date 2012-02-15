from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='pyocs',
      version=version,
      description="Python library for Open Collaboration Services",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Izhar Firdaus',
      author_email='izhar@inigo-tech.com',
      url='http://github.com/kagesenshi/pyocs/',
      license='BSD/MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'xmldict>=0.4',
          'zope.interface',
          'zope.schema'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
