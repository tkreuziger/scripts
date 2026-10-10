# markdown-to-org

Convert a Markdown file to Org-mode using [Pandoc](https://pandoc.org/).

The converted file is written to an output directory (default: current
directory) with an org-roam-style filename (`YYYY-MM-DD-<slug>.org` by
default; the date format is configurable, see below) and frontmatter:

```org
#+TITLE: <first H1 or the input filename>
#+ID: <uuid>
#+CREATED: <ISO timestamp>
```

## Requirements

- Python >= 3.10
- Pandoc on `PATH` (only invoked at runtime; not a Python dependency)

## Install

```sh
uv tool install ./scripts/markdown-to-org
```

## Usage

```sh
# write the result into the current directory
# -> 2026-10-10-my-great-note.org
markdown-to-org notes.md

# write the result into a specific directory
markdown-to-org notes.md --output-dir ~/org/roam

# use a different timestamp format (any strftime format works)
markdown-to-org notes.md --timestamp-format '%Y%m%d-%H%M%S'

# run without installing (uses PEP 723-style resolving via the project)
uv run --project scripts/markdown-to-org markdown-to-org notes.md
```

The path of the generated `.org` file is printed on success.

### Options

| Option | Description |
| ------ | ----------- |
| `-o, --output-dir <dir>` | Directory for the generated file (default: `.`). |
| `-t, --timestamp-format <format>` | `strftime` format for the date in the filename (default: `%Y-%m-%d`). |

If `pandoc` is not on `PATH`, the command exits with status 1 and a
helpful error message.

## Development

```sh
cd scripts/markdown-to-org
uv run markdown-to-org --help        # run from source
uv build                             # build sdist + wheel
```
