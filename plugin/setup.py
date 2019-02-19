# @Author  : lgb
# @Email   : liguobin@wanshare.com
# @Time    : 2018/11/19 15:29

from setuptools import setup

setup(name='pytest-simple',
      use_scm_version=True,
      description='pytest plugin for simple development',
      long_description=open('README.rst').read(),
      author='robin',
      author_email='liguobin@wanshare.com',
      packages=['pytest_simple'],
      package_data={'pytest_simple': ['resources/*']},
      entry_points={'pytest11': ['html = pytest_simple.plugin']},
      setup_requires=['setuptools_scm'],
      install_requires=[
        'pytest>=3.0',
        'pytest-metadata'],
      license='Mozilla Public License 2.0 (MPL 2.0)',
      keywords='py.test pytest simple',
      classifiers=[
          'Development Status :: v1.0',
          'Framework :: Pytest',
          'Intended Audience :: Developers',
          'Operating System :: POSIX',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: MacOS :: MacOS X',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
          'Topic :: Utilities',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ])
