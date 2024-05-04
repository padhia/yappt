"test tabulate"

from dataclasses import dataclass, field
from datetime import date
from textwrap import dedent
from typing import Optional

from yappt import tabulate_iter


def test_dataclass() -> None:
    @dataclass
    class Row:
        int_col: int
        text_col: Optional[str]
        bool_col: bool = field(metadata=dict(format="y"))
        date_col: date

    rows = [
        Row(1, "one", False, date(2000, 1, 1)),
        Row(2, "two", True, date(2000, 1, 2)),
        Row(99, None, True, date(2000, 12, 31)),
    ]
    actual = "\n".join(tabulate_iter(rows))

    expected = dedent(
        """\
        ┌─────────┬──────────┬──────────┬────────────┐
        │ Int Col │ Text Col │ Bool Col │  Date Col  │
        ├─────────┼──────────┼──────────┼────────────┤
        │       1 │ one      │          │ 2000-01-01 │
        │       2 │ two      │    ✓     │ 2000-01-02 │
        │      99 │          │    ✓     │ 2000-12-31 │
        └─────────┴──────────┴──────────┴────────────┘"""
    )

    assert actual == expected


def test_list() -> None:
    rows = [[1, "one"], [2, "two"], [999, None]]
    lines = tabulate_iter(rows, headers=["C1", "C2"], types=[int, Optional[str]])
    actual = "\n".join(lines)

    assert actual == dedent(
        """\
        ┌─────┬─────┐
        │  C1 │ C2  │
        ├─────┼─────┤
        │   1 │ one │
        │   2 │ two │
        │ 999 │     │
        └─────┴─────┘"""
    )


def test_embedded_nl() -> None:
    rows = [[1, "one"], [2, "two\nthree"], [999, None]]
    lines = tabulate_iter(rows, headers=["C1", "C2"], types=[int, Optional[str]])
    actual = "\n".join(lines)

    assert actual == dedent(
        """\
        ┌─────┬───────┐
        │  C1 │ C2    │
        ├─────┼───────┤
        │   1 │ one   │
        │   2 │ two   │
        │     │ three │
        │ 999 │       │
        └─────┴───────┘"""
    )


def test_default_fmtspec() -> None:
    rows = [[1, "one"], [2, "two"], [3, None]]
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


def test_peek() -> None:
    rows = [[1, "one"], [2, "two"], [999, None]]
    lines = tabulate_iter(rows, headers=["C1", "C2"], types=[int, Optional[str]], peek=2)
    actual = "\n".join(lines)

    assert actual == dedent(
        """\
        ┌────┬─────┐
        │ C1 │ C2  │
        ├────┼─────┤
        │  1 │ one │
        │  2 │ two │
        │ 999 │     │
        └────┴─────┘"""
    )
