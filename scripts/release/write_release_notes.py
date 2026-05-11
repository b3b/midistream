import sys
from pathlib import Path

RELEASE_NOTES_TEMPLATE = """# midistream {tag}

Release for `midistream`.

## Buildozer usage

    requirements = midistream=={version}


## Demo APK

The demo APK demonstrates usage of `midistream` in a Kivy/Android app.

The demo source is available in `examples/demo`.
"""


def write_release_notes(tag: str, version: str, output_path: Path) -> None:
    output_path.write_text(
        RELEASE_NOTES_TEMPLATE.format(tag=tag, version=version),
        encoding="utf-8",
    )


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("Usage: write_release_notes.py TAG VERSION OUTPUT_PATH")

    tag = sys.argv[1]
    version = sys.argv[2]
    output_path = Path(sys.argv[3])

    if not tag:
        raise SystemExit("Tag is empty")

    if not version:
        raise SystemExit("Version is empty")

    write_release_notes(tag, version, output_path)

    print(f"Wrote release notes to {output_path}")


if __name__ == "__main__":
    main()
