# yappt

Yet another pretty print for tables and trees.

**Note:** Versions `0.3.0` and later aren't compatible with earlier versions

A collection of classes and functions to format textual data for printing. The main functions (`tabulate` and `treeiter`) do not require reading entire dataset into memory, allowing printing large amount of data in streaming fashion.

Class       | Capabilities
------------|------------------------------------------------------------------------------------------------------
`PrettyInt` | When formatted, returns human-readable value. It can either show K,M,G suffix or exponential notation
`Duration`  | When formatted, returns a value that shows duration in hours, minutes and seconds.

Function        | Capabilities
----------------|-------------------------------------------------------------------------------------------------------
`tabulate`      | Pretty prints an iterable of either `dataclass` objects or iterable of sequences of strings as a table
`tabulate_iter` | Like `tabulate` but returns an iterable over formatted lines of text instead of printing it
`treeiter`      | Returns an iterable over tuples of formatted representation of tree node and the original node
`strip_pfx`     | strips a common prefix from all substrings that are separated by new-lines
`indent`        | indents all substrings that are separated by new-lines
`iter_more`     | accepts an iterable and returns a new iterable that returns original item and a *more items* indicator
`format_bool`   | format boolean values as unicode "✓" and "✗" code points

Refer to `tests/` folder for examples and usage
