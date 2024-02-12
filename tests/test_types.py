"test types"
import pytest

from yappt import Duration, PrettyInt, format_bool


def test_duration() -> None:
    assert format(Duration(seconds=300)) == "5m"
    assert format(Duration(seconds=310)) == "5m 10s"
    assert format(Duration(seconds=172800)) == "48h"
    assert format(Duration(seconds=7210)) == "2h 10s"

    assert format(Duration(seconds=1507.329), ".3") == "00:25:07.329"
    assert format(Duration(seconds=1507.329), ".2") == "00:25:07.33"
    assert format(Duration(seconds=1507.329), ".0") == "00:25:07"

    with pytest.raises(ValueError):
        format(Duration(seconds=1507.329), "x")


def test_prettyint() -> None:
    assert format(PrettyInt(10_240)) == format(10_240, ",d")
    assert format(PrettyInt(10_000), "s") == "10K"
    assert format(PrettyInt(1_048_576), ".1h") == "1M"
    assert format(PrettyInt(1_000_000), "s") == "1M"


def test_prettyint_exp() -> None:
    assert PrettyInt.with_exp(1_000) == "1e3"
    assert PrettyInt.with_exp(999_000) == "999e3"
    assert PrettyInt.with_exp(1_000_000) == "1e6"
    assert PrettyInt.with_exp(1_100_000) == "1.1e6"


def test_prettyint_unit() -> None:
    assert PrettyInt.with_unit(10_000, "", True) == "10K"
    assert PrettyInt.with_unit(1_048_576, ".1", False) == "1M"
    assert PrettyInt.with_unit(1_000_000, "", True) == "1M"
    assert PrettyInt.with_unit(1_000_000_000, "", True) == "1G"
    assert PrettyInt.with_unit(1_000_000_000_000, "", True) == "1T"


def test_bool() -> None:
    assert format_bool(False) == "✗"
    assert format_bool(True) == "✓"
    assert format_bool(False, "y") == ""
    assert format_bool(True, "y") == "✓"
    assert format_bool(False, "n") == "✗"
    assert format_bool(True, "n") == ""
