#! /usr/bin/env python

from setuptools import setup

with open("README.rst", encoding="utf-8") as f:
	readme = f.read()

setup(
	name='yappt',
	description='Yet Another Pretty Print Table',
	long_description=readme,
	url='https://bitbucket.org/padhia/yappt',

	author='Paresh Adhia',
	version='0.1.0',
	license='GPL',

	py_modules=['yappt'],

	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU General Public License (GPL)',

		'Intended Audience :: Developers',
		'Topic :: Utilities',

		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],
)
