# AGENTS.md

## Dev commands

```bash
# Install / update dependencies
poetry install

# Serve locally (live-reload)
poetry run mkdocs serve

# Build static site
poetry run mkdocs build
```

## Structure

- `mkdocs.yml` — MkDocs config (single top-level config, blog em pt-BR)
- `docs/` — Markdown source content (páginas, posts, autor, tags)
- `ext/slugs.py` — Slugify personalizado com suporte a pt-BR
- `hooks/socialmedia.py` — Botões de compartilhar no final dos posts
- `pyproject.toml` — Poetry-managed Python project (requires >=3.14)
- `tests/` — empty (no test framework configured)
- `opencode.json` — OpenCode project config (LSP enabled)
