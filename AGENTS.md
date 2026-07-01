# AGENTS.md

## Dev commands

```bash
# Serve locally (live-reload)
poetry run mkdocs serve --config-file blog/mkdocs.yml

# Build static site
poetry run mkdocs build --config-file blog/mkdocs.yml
```

## Structure

- `blog/mkdocs.yml` — MkDocs config (single top-level config)
- `blog/docs/` — Markdown source content
- `pyproject.toml` — Poetry-managed Python project (requires >=3.14)
- `tests/` — empty (no test framework configured)
- `opencode.json` — OpenCode project config (LSP enabled)
