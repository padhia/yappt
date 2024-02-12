"class to store metadata for formatting a column"
import datetime as dt
from dataclasses import Field, dataclass, fields
from decimal import Decimal
from enum import Enum
from typing import Callable, Generic, Optional, TypeVar, get_type_hints

from ..util import bare_type, format_bool
from .duration import Duration
from .prettyint import PrettyInt

T = TypeVar("T")


class HAlign(str, Enum):
    """
    An Enum class to determine type of horizontal alignment

    Attributes:
        LEFT: "<" left alignment
        RIGHT: ">" right alignment
        CENTER: "^" center alignment
    """

    LEFT = "<"
    RIGHT = ">"
    CENTER = "^"

    def __init__(self, a: str):
        self.align = str.ljust if a == "<" else str.rjust if a == ">" else str.center

    @staticmethod
    def from_type(t: type) -> "HAlign":
        """
        determine prefered horizontal alignment of a Python type.
        - temporal and boolean values are center aligned
        - numerical types are right aligned
        - all other are left aligned

        Args:
            t: a Python type

        Returns:
            one of either LEFT, RIGHT or CENTER
        """
        if issubclass(t, (bool, dt.date, dt.time, dt.datetime)):
            return HAlign.CENTER
        if issubclass(t, (int, float, Decimal, Duration)):
            return HAlign.RIGHT
        return HAlign.LEFT


@dataclass(frozen=True)
class Column(Generic[T]):
    """
    A class that holds metadata to format values of a single column of a specific type

    Attributes:
        title: column title
        alignment: whether the formatted data is to be aligned left, right or center
        as_str: a callable that takes a value, format specification and returns the value as a formatted string
        format_spec: format specification to use, (default: "")
        none_str: how to render None values (default: "")
    """

    title: str
    alignment: HAlign
    to_str: Callable[[T, str], str]
    format_spec: str = ""
    none_str: str = ""

    def format(self, val: T) -> str:
        """format a value of this column type"""
        return self.none_str if val is None else self.to_str(val, self.format_spec)

    @staticmethod
    def from_type(
        title: str,
        type_hint: type[T],
        format_spec: Optional[str] = None,
        align: Optional[str] = None,
        default_fmtspec: dict[type, str] = {},
    ) -> "Column[T]":
        """
        Instantiate a Column instance for a Python type

        Args:
            title: column title
            type_hint: a Python type to determine formatting style; if the type is Optional[T], T is used instead
            format_spec: optional, defaults to ""
            align: optional, "<" for left, ">" for right and "^" for center, default: numbers right, bool/temporal values center, left for others

        Returns:
            None
        """
        KNOWN_TYPES: dict[type[T], Callable[[T, str], str]] = {
            bool: format_bool,
            int: PrettyInt.__format__,
            dt.timedelta: Duration.__format__,
        }  # type: ignore
        base_type = bare_type(type_hint)

        return Column(
            title,
            alignment=HAlign(align) if align is not None else HAlign.from_type(base_type),
            to_str=KNOWN_TYPES.get(base_type, format),
            format_spec=format_spec if format_spec is not None else default_fmtspec.get(base_type, ""),
        )

    @staticmethod
    def from_dataclass(A: type[T], default_fmtspec: dict[type, str] = {}) -> "list[Column[T]]":
        def header(f: Field[T]) -> str:
            return f.metadata.get("title") or f.name.replace("_", " ").title()

        type_hints = get_type_hints(A)
        return [
            Column.from_type(header(f), type_hints[f.name], f.metadata.get("format"), f.metadata.get("align"), default_fmtspec)
            for f in fields(A)  # type: ignore
        ]
