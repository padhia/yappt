"utility types and functions"
import re
from types import UnionType
from typing import Iterable, TypeVar, Union, get_origin

T = TypeVar("T")


def iter_more(xs: Iterable[T]) -> Iterable[tuple[bool, T]]:
    """retrun a new iterable based on the given iterable, that peeks past the current value for existence and returns
    tuple (more, item), where more is True if current is not the last item

    Args:
        xs: An Iterable of type T

    Returns:
        An Iterable of tuple[bool, T]; where T is from the original Iterable, and bool will be True if there is
        at least one more item that be returned by next()
    """
    _xs = iter(xs)
    try:
        x = next(_xs)
    except StopIteration:
        return

    for _x in _xs:
        yield (True, x)
        x = _x

    yield (False, x)


def strip_pfx(s: str, pfx: str = r"\s*\|") -> str:
    """strip prefix (any regex patten, default \\s*\\|) from all \\n separated lines of the input string

    Args:
        s: input string containing embedded new lines with a profix
        pfx: a regex pattern that preceeds all embedded lines (default "\\s*\\|")

    Returns:
        string with embedded lines having their prefix, if any, removed
    """

    def strip(s: str) -> str:
        m = re.match(pfx, s)
        return (s[m.end() :] if m else s).rstrip()

    return "\n".join(map(strip, s.splitlines()))


def indent(s: str, times: int = 1, first_line: bool = False, *, dlm: str = "    ") -> str:
    """indent embedded lines with delimiter (default tab)

    Args:
        s: input string containing embedded new-lines
        times: number of indents (default 1)
        first_line: indent the first_line (default False)
        dlm: delimiter (default 4 spaces)

    Returns:
        string with embedded lines indented
    """
    ind = dlm * times
    return (ind if first_line else "") + f"\n{ind}".join(s.splitlines())


def format_bool(v: bool, spec: str = "") -> str:
    """format a boolean value to string
    True/False are converted to check-mark and cross-mark respectively

    Args:
        v: a boolean value
        spec: if 'y' then return value only for True value, 'n' then return value only for False value

    Returns:
        Unicode check-mark for True value and a cross-mark for False value
    """
    if spec == "y":
        return "✓" if v else ""
    if spec == "n":
        return "" if v else "✗"
    if spec == "":
        return "✓" if v else "✗"

    raise ValueError(f"'{spec}' is invalid format spec for boolean values")


def bare_type(X: type[T]) -> type[T]:
    "returns Y if X is either Optional[Y] or Y | None, otherwise returns X"
    orig_type = get_origin(X)
    if orig_type is not None and (orig_type is Union or issubclass(orig_type, UnionType)) and X.__args__[1] == type(None):  # type: ignore
        return X.__args__[0]  # type: ignore
    return X
