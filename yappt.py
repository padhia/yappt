"Yet another pretty print table"

import re
from decimal import Decimal
import datetime as dt

class HumanInt(int):
	"An int subclass that formats values for human readability (similar to --human-readable option of the ls command)"
	def __format__(self, spec):
		m = re.match(r'(\d*)(.\d+)?(h|s|e)$', spec)
		if not m:
			return int.__format__(self, spec)

		width, prec, typ = m.groups()

		if typ == 'e':
			if prec:
				raise ValueError('Precision not allowed in integer format specifier')

			if self == 0:
				s = '0'
			else:
				for e in [12, 9, 6, 3, 0]:
					if self % 10**e == 0:
						break
				s = (str(self // 10**e) + 'e' + str(e)) if e else str(self)

		else:
			num = float(self)
			base = 1000.0 if spec[-1] == 's' else 1024.0

			for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']:
				if num < base:
					break
				num /= base

			fmt = ',' + (prec or '.0') + 'f'
			s = format(num, fmt)
			if '.' in s:
				s = s.rstrip('0').rstrip('.')
			s += unit

		return s.rjust(int(width)) if width else s

class PPCol:
	"Pretty printer for a column within a table"
	@staticmethod
	def make_fmtval(ctype):
		"make format function based on type"
		if ctype is None:
			return str
		if issubclass(ctype, HumanInt):
			return lambda v: HumanInt.__format__(v, '.1h')
		if issubclass(ctype, int):
			return lambda v: format(v, ',d')
		if issubclass(ctype, (float, Decimal)):
			return lambda v: format(v, ',.2f')
		return str

	@staticmethod
	def make_justify(ctype):
		"make justify function based on type"
		if ctype is None:
			return str.ljust
		if issubclass(ctype, (int, float, Decimal, dt.date, dt.datetime, dt.time, dt.timedelta)):
			return str.rjust
		return str.ljust

	@staticmethod
	def creeate(col, infer_from=None):
		"create a new instance depedning on parameter type"
		if isinstance(col, PPCol): return col
		if isinstance(col, tuple): return PPCol(col[0], col[1] or next((type(v) for v in (infer_from or []) if v != None), None))
		return PPCol(None if col is None else str(col))

	def __init__(self, title, ctype=None, fmtval=None, justify=None, width=1):
		self.title = title or ''
		self.width = max(width, len(self.title))
		self.fmtval = fmtval or self.make_fmtval(ctype)
		self._justify = justify or self.make_justify(ctype)

	def justify(self, val):
		"justify value"
		return self._justify(val, self.width)

	def __str__(self):
		return f"{self.title}:{self.width}"

def tabulate(rows, columns=None, none_value='', dash='-'):
	"Pretty print table data. Inspired by https://bitbucket.org/astanin/python-tabulate"

	table = [list(r) for r in zip(*rows)]  # transpose
	if not table and not columns:
		return
	if columns:
		if table:
			if len(columns) != len(table):
				raise ValueError('Number of columns in data must match column definitions')
			columns = [PPCol.creeate(c, v) for c, v in zip(columns, table)]
		else:
			columns = [PPCol.creeate(c) for c in columns]
	else:
		columns = [PPCol.creeate('', v) for v in table]

	# stage 1: transform table values to formatted string
	table = [[c.fmtval(v) if v != None else none_value for v in vals] for c, vals in zip(columns, table)]

	# adjust max width, if needed, before the second stage
	for col, w in zip(columns, [max(len(v) for v in vals) for vals in table]):
		if w > col.width:
			col.width = w

	# stage 2: justify table values
	table = [[c.justify(v) for v in vals] for c, vals in zip(columns, table)]

	if [c.title for c in columns if c.title]: # print column titles if at least one is non-blank
		yield [c.justify(c.title) for c in columns]
		if dash:
			yield [''.ljust(c.width, dash) for c in columns]

	yield from zip(*table) # transform table to rows

def pprint(rows, columns, sep='  ', none_value='', dash='-'):
	"tabulate and print rows of data"
	print('\n'.join(sep.join(row) for row in tabulate(rows, columns, none_value=none_value, dash=dash)))
