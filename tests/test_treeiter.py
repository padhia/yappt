"test treeiter"

from textwrap import dedent
from typing import Iterable

from yappt import treeiter


def test_treeiter() -> None:
    roles = {"sysadmin": ["elt", "bi"], "elt": ["dev", "qa"], "dev": ["qa", "rw"]}

    def leaves(x: str) -> Iterable[str]:
        return iter(roles.get(x, []))

    result = "\n".join(f"{s}{r}" for s, r in treeiter("sysadmin", leaves, width=1, gap=0))
    expect = dedent(
        """\
        sysadmin
        ├─elt
        │ ├─dev
        │ │ ├─qa
        │ │ └─rw
        │ └─qa
        └─bi"""
    )

    assert result == expect
