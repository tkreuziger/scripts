"""Allow running as ``python -m markdown_to_org``."""

from markdown_to_org.cli import main

if __name__ == "__main__":
    raise SystemExit(main())