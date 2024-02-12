"print rows as a grid"
import logging
import os
from itertools import chain, islice
from typing import Iterable, Iterator, Optional, Sequence

from .types import BasicGridStyle, BoxedGridStyle, GridConnectors, GridStyle

logger = logging.getLogger(__name__)


MinimalStyle = BasicGridStyle("-", "  ", "  ")
SimpleStyle = BasicGridStyle("─", " │ ", "─┼─")
AsciiStyle = BasicGridStyle("-", " | ", "-+-")
BoxStyle = BoxedGridStyle(
    "─",
    GridConnectors("┌─", "─┬─", "─┐"),
    GridConnectors("├─", "─┼─", "─┤"),
    GridConnectors("│ ", " │ ", " │"),
    GridConnectors("└─", "─┴─", "─┘"),
)
AsciiBoxStyle = BoxedGridStyle(
    "-",
    GridConnectors("+-", "-+-", "-+"),
    GridConnectors("+-", "-+-", "-+"),
    GridConnectors("| ", " | ", " |"),
    GridConnectors("+-", "-+-", "-+"),
)


_available_styles: dict[str, GridStyle] = {
    "BOX": BoxStyle,
    "MINIMAL": MinimalStyle,
    "SIMPLE": SimpleStyle,
    "ASCII": AsciiStyle,
    "ASCIIBOX": AsciiBoxStyle,
}


def _get_grid_style() -> Optional[GridStyle]:
    style_name = os.environ.get("GRID_STYLE")
    if style_name is not None:
        if style_name.upper() in _available_styles:
            return _available_styles[style_name.upper()]
        logger.warning(
            "yappt: $GRID_STYLE has an invalid style '%s', valid style names: [%s]",
            style_name,
            ",".join(_available_styles.keys()),
        )

    return None


override_grid_style = _get_grid_style()


def iter_with_grid(
    data: Iterator[Sequence[str]],
    *,
    num_headers: int = 1,
    grid_style: Optional[GridStyle] = None,
    default_grid_style: Optional[GridStyle] = None,
) -> Iterable[str]:
    "accepts an Iterable of sequences of strings, and returns an Iterable of tabulated strings"
    first_row = next(data, None)
    if first_row is None:
        return

    data = chain([first_row], data)
    widths = [len(x) for x in first_row]

    style = grid_style or override_grid_style or default_grid_style or BoxStyle

    yield from style.format_top(widths)
    if num_headers:
        yield from (style.format_row(h) for h in islice(data, num_headers))
        yield from style.format_sep(widths)
    yield from (style.format_row(d) for d in data)
    yield from style.format_bot(widths)
