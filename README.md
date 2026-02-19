# Home Assistant Blueprint: Simple Adaptive Lighting

French version: [`README.fr.md`](README.fr.md)

This repository automatically generates a Home Assistant blueprint in multiple languages from a single template.

## Structure

- `template.yaml`: source blueprint with `[[...]]` placeholders
- `VERSION`: single blueprint version (injected into the description and `blueprint_revision`)
- `languages/en.json`: reference dictionary (required, complete)
- `languages/<lang>.json`: per-language translations (automatic fallback to `en`)
- `scripts/generate_blueprints.py`: generation + validation
- `dist/<lang>/adaptive_lighting.yaml`: generated blueprints

## Validation rules

- All template keys must exist in `languages/en.json`.
- Other languages can omit keys (fallback to `en`).
- Unknown keys in any dictionary fail the build (typo guard).

## Local generation

```bash
python3 scripts/generate_blueprints.py
```

- Generates `dist/en/adaptive_lighting.yaml`, `dist/fr/adaptive_lighting.yaml`, etc.
- Injects `[[blueprint.version]]` from `VERSION`.
- The version line is translated through `blueprint.version.line` in each `languages/<lang>.json`,
  with a `{version}` placeholder (example: `Version: {version}`).

## GitHub Actions CI/CD

Workflow: `.github/workflows/blueprint-i18n.yml`

- On pull requests and pushes: validates template + dictionaries.
- On push to `main`: regenerates and publishes `dist/` to `gh-pages`.

## Stable public URLs for Home Assistant

Use `raw` URLs from the `gh-pages` branch:

- English:
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/en/adaptive_lighting.yaml`
- French:
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/fr/adaptive_lighting.yaml`

These URLs stay stable as long as you keep the `gh-pages` branch and paths.

## Add a new language

1. Create `languages/<lang>.json`
2. Add translated keys (partial is allowed)
3. Let CI validate and publish
