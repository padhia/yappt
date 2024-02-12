"classes that represent grid drawing styles"
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class GridConnectors:
    """
    strings to connect individual column values to form a single line of text

    Attributes:
        left: A prefix to attach to the finalized string
        mid: individual columns are joined using this string to make up the finalized string
        right: A suffix that is added to the finalized string after all individual columns values have been concatenated
    """

    left: str
    mid: str
    right: str

    def __call__(self, row: Sequence[str]) -> str:
        return self.left + self.mid.join(row) + self.right


class GridStyle(ABC):
    """A grid styling interface"""

    def format_top(self, widths: Sequence[int]) -> Iterable[str]:
        "returns an Iterable of string to draw the Top line before the header is rendered"
        yield from []

    def format_sep(self, widths: Sequence[int]) -> Iterable[str]:
        "returns an Iterable of string to draw separaton line(s) after the header, but before the data is rendered"
        yield from []

    def format_bot(self, widths: Sequence[int]) -> Iterable[str]:
        "returns an Iterable of string to draw as the last line(s) after all the data lines has been rendered"
        yield from []

    @abstractmethod
    def format_row(self, row: Sequence[str]) -> str:
        "returns a string that is used for rendering a row of data; note also used to render header (column titles)"
        return ""


@dataclass(frozen=True)
class BoxedGridStyle(GridStyle):
    """
    A GridStyle that draws decorations on all sides of a table using a set of GridConnectors

    Attributes:
        fill: a character used to fill column width for non-data lines
        header: decoration used for drawing header (column titles)
        separator: decoration drawn to mark end of header and begining of data
        data: decoration used for drawing data and column title lines
        footer: decoration drawn at the end after all data lines have been drawn
    """

    fill: str
    header: GridConnectors
    separator: GridConnectors
    data: GridConnectors
    footer: GridConnectors

    def format_top(self, widths: Sequence[int]) -> Iterable[str]:
        yield self.header([self.fill * w for w in widths])

    def format_sep(self, widths: Sequence[int]) -> Iterable[str]:
        yield self.separator([self.fill * w for w in widths])

    def format_bot(self, widths: Sequence[int]) -> Iterable[str]:
        yield self.footer([self.fill * w for w in widths])

    def format_row(self, row: Sequence[str]) -> str:
        return self.data(row)


@dataclass(frozen=True)
class BasicGridStyle(GridStyle):
    """
    A GridStyle that draws decorations between columns and between header and data lines

    Attributes:
        fill: a character used to fill column width for non-data lines
        data_dlm: separator to join data and header values with
        title_dlm: separator to join separator line between header and data
    """

    fill: str
    data_dlm: str
    title_dlm: str

    def format_sep(self, widths: Sequence[int]) -> Iterable[str]:
        yield self.title_dlm.join(self.fill * w for w in widths)

    def format_row(self, row: Sequence[str]) -> str:
        return self.data_dlm.join(row)
