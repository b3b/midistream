import sys


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_installed_version.py VERSION")

    expected = sys.argv[1]

    if not expected:
        raise SystemExit("Expected version is empty")

    import midistream

    actual = getattr(midistream, "__version__", None)

    if actual != expected:
        raise SystemExit(f"Expected midistream {expected}, got {actual}")

    print(f"Installed midistream: {actual}")


if __name__ == "__main__":
    main()
