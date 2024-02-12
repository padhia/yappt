"datetime.timedelta subclass that produces formatted human-readable output"
import datetime as dt
import re


class Duration(dt.timedelta):
    """Python datetime.timedelta subclass that can be formatted.

    The default formatting (format spec is omitted or is "") is to be human-readable (e.g. "20h 30m 10s").

    Format spec can be ".N" where N is unsigned number, in which case formatting is done as "HH:MM:SS(.ms)".
    where ".ms" is fractional seconds displayed with N digits precision. When N is zero, no fractional seconds
    are displayed.
    """

    def __format__(self, spec: str = "") -> str:
        hh, mm, ss = self.days * 24 + self.seconds // 3600, (self.seconds % 3600) // 60, self.seconds % 60

        if spec == "":
            return " ".join(f"{v}{s}" for v, s in [(hh, "h"), (mm, "m"), (ss, "s")] if v > 0) or "0"

        if (m := re.fullmatch("\\.(\\d+)", spec)) is not None:
            frac = int(m.group(1))
            return f"{hh:02d}:{mm:02d}:{ss:02d}" + (f"{self.microseconds / 1000_000:.{frac}f}"[1:] if frac > 0 else "")

        raise ValueError(f"Unknown format code {spec} for Duration")

    @staticmethod
    def from_timedelta(t: dt.timedelta) -> "Duration":
        "convert a datetime.timedelta value to Duration"
        return Duration(days=t.days, seconds=t.seconds, microseconds=t.microseconds)
