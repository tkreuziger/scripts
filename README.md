# scripts

A personal collection of small, standalone command-line tools.

Every tool lives in its own directory under [`scripts/`](scripts/) and is a
fully self-contained Python package with its own `pyproject.toml`. Install the
tools you need globally with `uv tool install`.

## Tools

| Tool | Description | Install |
| ---- | ----------- | ------- |
| [`markdown-to-org`](scripts/markdown-to-org/README.md) | Convert Markdown files to Org-mode via Pandoc | `uv tool install ./scripts/markdown-to-org` |

## Usage

From the repository root, install any tool into your global `uv` tool bin:

```sh
uv tool install ./scripts/<tool>
```

Or install all tools at once:

```sh
for tool in scripts/*/; do uv tool install "$tool"; done
```

For a tool that has been published, you can also install it straight from a Git
URL, for example:

```sh
uv tool install --from git+https://github.com/tkreuziger/scripts.git#subdirectory=scripts/markdown-to-org markdown-to-org
```

## Adding a new tool

1. Create `scripts/<tool>/` with a `pyproject.toml`, a `README.md`, and a
   `src/` package that exposes a `main()` callable.
2. Declare a console-script entry point:

   ```toml
   [project.scripts]
   <command> = "<package>.cli:main"
   ```

3. Add the tool to the table above. Workspace membership (`scripts/*`) is
   picked up automatically, so `uv run <command>` works from inside the
   tool's directory (`cd scripts/<tool>`).

## Development

```sh
uv sync                 # create the workspace dev environment (ruff)
uv run ruff check .     # lint everything
```

When developing a tool you've already installed globally, note that `uv
tool install` caches built wheels per package version. After changing a
tool's code, either bump its version in `pyproject.toml` or clear the
cached wheel before reinstalling:

```sh
uv tool install --force ./scripts/<tool> -U   # rebuild from current source
```

(`-U`/`--refresh` re-resolves; `uv cache clean <name>` also works.)

## License

MIT, see [LICENSE](LICENSE).
