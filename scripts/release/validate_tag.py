import os
import sys
from pathlib import Path

from packaging.version import InvalidVersion, Version


def write_github_output(name: str, value: str) -> None:
    github_output = os.environ.get("GITHUB_OUTPUT")

    if not github_output:
        print(f"{name}={value}")
        return

    with Path(github_output).open("a", encoding="utf-8") as f:
        f.write(f"{name}={value}\n")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_tag.py TAG")

    tag = sys.argv[1]

    if not tag.startswith("v"):
        raise SystemExit(f"Release tag must start with v: {tag}")

    version = tag[1:]

    if not version:
        raise SystemExit("Release version is empty")

    try:
        parsed = Version(version)
    except InvalidVersion as exc:
        raise SystemExit(f"Invalid PEP 440 release version: {version}") from exc

    if str(parsed) != version:
        raise SystemExit(
            f"Release version must be canonical PEP 440: {version} != {parsed}"
        )

    write_github_output("tag", tag)
    write_github_output("version", version)


if __name__ == "__main__":
    main()
