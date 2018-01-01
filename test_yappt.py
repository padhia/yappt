#! /usr/bin/env python
"""pytest test cases to unit test yappt module"""

import datetime as dt
from decimal import Decimal
from yappt import *

data = [
	[12345, 'ABC', 12, dt.date(2017, 12, 20), 5555.67, Decimal(1222.445)],
	[0, 'B', 1, None, 1.3456, None],
]

cols = [('Human', HumanInt), ('Str', str), ('Int', int), ('Date', dt.date), ('Float', float), ('Dec', Decimal)]

def tabulate_str(*args, **kwargs):
	"convert formatted tabulate results to a string for comparison"
	return '\n'.join('  '.join(row) for row in tabulate(*args, **kwargs))

def test_explicit_types():
	"test case: explicit types specified"
	assert tabulate_str(data, cols, none_value='?') == """\
Human  Str  Int        Date     Float       Dec
-----  ---  ---  ----------  --------  --------
12.1K  ABC   12  2017-12-20  5,555.67  1,222.44
    0  B      1           ?      1.35         ?"""

def test_infer_types():
	"test case: infer types from data"
	assert tabulate_str([[1234567, None]], ['C1', 'C2']) == """\
       C1  C2
---------  --
1,234,567    """

def test_no_titles():
	"test case: no column titles specified"
	assert tabulate_str([[123456, HumanInt(1234567890), 'abcd']]) == "123,456  1.1G  abcd"
