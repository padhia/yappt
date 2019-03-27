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

def test_neg_num():
	"test negative HumanInt values"
	assert format(HumanInt(-340000), "h")    == "-332K"
	assert format(HumanInt(-340000), "s")    == "-340K"
	assert format(HumanInt(-340000), "e")    == "-340e3"
	assert format(HumanInt(-340000), "9.2h") == " -332.03K"

def test_explicit_types():
	"test case: explicit types specified"
	assert tabulate(data, cols, none_value='?') == """\
Human Str Int       Date    Float      Dec
----- --- --- ---------- -------- --------
12.1K ABC  12 2017-12-20 5,555.67 1,222.44
    0 B     1          ?     1.35        ?"""

def test_infer_types():
	"test case: infer types from data"
	assert tabulate([[1234567, None]], ['C1', 'C2']) == """\
       C1 C2
--------- --
1,234,567   """

def test_no_titles():
	"test case: no column titles specified"
	assert tabulate([[123456, HumanInt(1234567890), 'abcd']]) == """\
123,456 1.1G abcd"""


class Node:
	"Node of a tree; has zero or more children"
	def __init__(self, name):
		self.name, self.children = name, []
	def __str__(self):
		return str(self.name)

root = Node(0)
root.children = [Node(1), Node(2), Node(3)]
root.children[0].children = [Node(11)]
root.children[1].children = [Node(21), Node(22)]
root.children[1].children[0].children = [Node(211), Node(212)]

def test_tree_walk():
	"Test tree walker with default style"
	assert '\n'.join(t+str(n) for t, n in treeiter(root)) == """\
0
├─ 1
│  └─ 11
├─ 2
│  ├─ 21
│  │  ├─ 211
│  │  └─ 212
│  └─ 22
└─ 3"""

def test_tree_walk_ascii():
	"Test tree walker with ascii style"
	assert '\n'.join(t+str(n) for t, n in treeiter(root, style='ascii')) == """\
0
|- 1
|  L_ 11
|- 2
|  |- 21
|  |  |- 211
|  |  L_ 212
|  L_ 22
L_ 3"""

def test_tree_walk_raw():
	"Test tree walker with no style"
	assert '\n'.join(t+str(n) for t, n in treeiter(root, style=None)) == """\
0
T1
IL11
T2
IT21
IIT211
IIL212
IL22
L3"""

print('\n'.join(t+str(n) for t, n in treeiter(root)))
pprint(data, cols, none_value='?')
