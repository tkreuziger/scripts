"""Convert Markdown files to Org-mode using Pandoc.

This tool turns a Markdown file into an Org file (named after the title and
the current timestamp) with org-roam-style frontmatter (``#+TITLE``,
``#+ID``, ``#+CREATED``). It requires the ``pandoc`` binary to be
available on ``PATH``.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

DEFAULT_TIMESTAMP_FORMAT = "%Y-%m-%d"


class PandocNotFoundError(RuntimeError):
    """Raised when the ``pandoc`` binary is not available on PATH."""


def require_pandoc() -> None:
    """Check that pandoc is available; raise :class:`PandocNotFoundError` otherwise."""
    if shutil.which("pandoc") is None:
        raise PandocNotFoundError("pandoc is required but was not found on PATH")


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def get_title(markdown: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def convert(
    input_path: Path,
    output_dir: Path,
    timestamp_format: str = DEFAULT_TIMESTAMP_FORMAT,
) -> Path:
    """Convert *input_path* to an Org file inside *output_dir*.

    *timestamp_format* is a ``strftime`` format used for the date part of
    the output filename.
    """
    require_pandoc()
    markdown = input_path.read_text(encoding="utf-8")

    now = datetime.now()
    title = get_title(markdown, input_path.stem)
    slug = slugify(title)
    document_id = str(uuid.uuid4())

    filename = f"{now:{timestamp_format}}-{slug}.org"
    output = output_dir / filename

    result = subprocess.run(
        [
            "pandoc",
            "--from=markdown",
            "--to=org",
        ],
        input=markdown,
        text=True,
        capture_output=True,
        check=True,
    )

    frontmatter = f"""#+TITLE: {title}
#+ID: {document_id}
#+CREATED: {now.isoformat(timespec="seconds")}

"""

    output_dir.mkdir(parents=True, exist_ok=True)
    output.write_text(frontmatter + result.stdout, encoding="utf-8")
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert a Markdown file to Org-mode using Pandoc.",
        prog="markdown-to-org",
    )
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("."),
    )
    parser.add_argument(
        "-t",
        "--timestamp-format",
        default=DEFAULT_TIMESTAMP_FORMAT,
        help=(
            "strftime format for the date part of the output filename "
            "(default: %(default)s; e.g. '%%Y%%m%%d-%%H%%M%%S' for a "
            "compact date-and-time timestamp)"
        ),
    )
    args = parser.parse_args(argv)

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")

    try:
        output = convert(args.input, args.output_dir, args.timestamp_format)
    except PandocNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip()
        message = f"pandoc failed with exit code {exc.returncode}"
        if detail:
            message += f": {detail}"
        print(f"error: {message}", file=sys.stderr)
        return 1

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())