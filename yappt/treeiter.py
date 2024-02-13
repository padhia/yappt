from typing import Callable, Iterable, TypeVar

from .util import iter_more

T = TypeVar("T")


def treeiter(root: T, leaves: Callable[[T], Iterable[T]], width: int = 2, gap: int = 1) -> Iterable[tuple[str, T]]:
    """
    accepts an iterable that iterates over a tree depth first, and returns a new iterable that iterates over
    the original tree, but also returns a visual tree trunk representation

    Args:
        root: root element of type T
        leaves: callable that returns an iterable of child nodes
        width: how wide/skinny the visual representation should be. default 1, range 0+

    Returns:
        an Iterable of tuple that contains visual trunk and original element
    """

    def shift(trunk: str, by: str) -> str:
        "add a new branch to the trunk"
        return trunk.replace("└", " ").replace("├", "│") + by

    def walk(node: T, trunk: str) -> Iterable[tuple[str, T]]:
        "Visits node and its children in order"
        yield (trunk, node)
        for more, child in iter_more(leaves(node)):
            yield from walk(child, shift(trunk, "├" if more else "└"))

    def stylize(xs: str) -> str:
        def stretch(x: str) -> str:
            return x + (" " if x == " " or x == "│" else "─") * width + " " * gap

        return "".join(map(stretch, xs))

    for trunk, node in walk(root, ""):
        yield (stylize(trunk), node)
