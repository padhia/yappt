"int subclass that formats in pretty human-readable format"
import re


class PrettyInt(int):
    "An int subclass that formats values for human readability (similar to --human-readable option of the ls command)"

    @staticmethod
    def with_exp(val: int) -> str:
        """
        (static method) format an integer value with 'e' (exponent) notation for multiple of thousands

        Examples:
            1_000     => 1e3
            999_000   => 999e3
            1_000_000 => 1e6
            1_100_000 => 1.1e6
        """
        if val == 0:
            return "0"
        e = next(e for e in [12, 9, 6, 3, 0] if val / 10**e >= 1)
        n = format(val / 10**e, ".2f").rstrip("0").rstrip(".")

        return f"{n}e{e}"

    @staticmethod
    def with_unit(val: int, prec: str, use_si: bool) -> str:
        """
        (static method) format an integer value in prettier, human readable format

        Examples:
            1_048_576, 0, False => 1M
            1_000_000, 0, True  => 1M

        Args:
            val: number to format
            prec: max precision to use
            use_si: use 1000 as the base if True, 1024 otherwise

        Returns:
            value formated as human-readable string
        """
        num = float(val)
        base = 1000.0 if use_si else 1024.0

        unit = ""
        for u in ["", "K", "M", "G", "T", "P", "E", "Z", "Y"]:
            unit = u
            if num < base:
                break
            num /= base

        fmt = "," + (prec or ".0") + "f"
        s = format(num, fmt)
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        return s + unit

    def __format__(self, spec: str = "") -> str:
        if spec == "":
            return int.__format__(self, ",d")

        m = re.match(r"(\d*)(.\d+)?(h|s|e)$", spec)
        if not m:
            return int.__format__(self, spec)

        width, prec, typ = m.groups()
        sign, val = ("-", abs(self)) if self < 0 else ("", self)

        s = PrettyInt.with_exp(val) if typ == "e" else PrettyInt.with_unit(val, prec, typ == "s")
        s = sign + s

        return s.rjust(int(width)) if width else s
