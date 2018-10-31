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
	version='0.1.1',
	license='MIT',
	python_requires='>=3.6',

	py_modules=['yappt'],

	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Intended Audience :: Developers',
		'Topic :: Utilities',
		'Programming Language :: Python :: 3 :: Only',
	],
)
