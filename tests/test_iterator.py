"test tabulate with an iterator as an input"

from textwrap import dedent
from typing import Optional

from yappt import tabulate_iter


def test_dataclass() -> None:
    rows = [(1, "one"), [2, "two"], [3, None]]
    lines = tabulate_iter(rows, headers=["C1", "C2"], types=[Optional[int], Optional[str]], default_fmtspc={int: "03d"})
    actual = "\n".join(lines)

    assert actual == dedent(
        """\
        ┌─────┬─────┐
        │  C1 │ C2  │
        ├─────┼─────┤
        │ 001 │ one │
        │ 002 │ two │
        │ 003 │     │
        └─────┴─────┘"""
    )
