import sys
from pathlib import Path


VERSION_FILE = Path("midistream/version.py")

VERSION_FILE_TEMPLATE = '''"""Package version.

This file is filled with the actual value during the PyPI package build.
Development version is always "0.0.0".
"""

__version__ = "{version}"
'''


def write_version_file(version: str) -> None:
    VERSION_FILE.write_text(
        VERSION_FILE_TEMPLATE.format(version=version),
        encoding="utf-8",
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: write_version.py VERSION")

    version = sys.argv[1]
    if not version:
        raise SystemExit("Version is empty")

    write_version_file(version)
    print(f"Wrote {VERSION_FILE} with version {version}")


if __name__ == "__main__":
    main()
