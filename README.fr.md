# Blueprint Home Assistant: Simple Adaptive Lighting

English version: [`README.md`](README.md)


## Utiliser le blueprint

Vous pouvez utiliser ce blueprint sur votre instance Home Assistant en utilisant ce lien direct :

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsimple-adaptative-lightning%2Fgh-pages%2Ffr%2Fadaptive_lighting.yaml)

## Structure

- `template.yaml` : blueprint source avec placeholders `[[...]]`
- `VERSION` : version unique du blueprint (injectee dans la description et `blueprint_revision`)
- `languages/en.json` : dictionnaire de reference (obligatoire, complet)
- `languages/<lang>.json` : traductions par langue (fallback automatique vers `en`)
- `scripts/generate_blueprints.py` : generation + validation
- `dist/<lang>/adaptive_lighting.yaml` : blueprints generes

## Regles de validation

- Toutes les cles du template doivent exister dans `languages/en.json`.
- Les autres langues peuvent omettre des cles (fallback vers `en`).
- Les cles inconnues dans un dictionnaire font echouer le build (anti-typo).

## Generation locale

```bash
python3 scripts/generate_blueprints.py
```

- Genere `dist/en/adaptive_lighting.yaml`, `dist/fr/adaptive_lighting.yaml`, etc.
- Injecte `[[blueprint.version]]` depuis `VERSION`.
- La ligne de version est traduite via `blueprint.version.line` dans chaque `languages/<lang>.json`,
  avec un placeholder `{version}` (exemple : `Version : {version}`).

## CI/CD GitHub Actions

Workflow : `.github/workflows/blueprint-i18n.yml`

- Sur pull request et push : valide template + dictionnaires.
- Sur push vers `main` : regenere et publie `dist/` sur `gh-pages`.

## URLs publiques stables pour Home Assistant

Utilise les URLs `raw` de la branche `gh-pages` :

- Anglais :
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/en/adaptive_lighting.yaml`
- Francais :
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/fr/adaptive_lighting.yaml`

Ces URLs restent stables tant que la branche `gh-pages` et les chemins sont conserves.

## Ajouter une langue

1. Creer `languages/<lang>.json`
2. Ajouter les cles traduites (partiel autorise)
3. Laisser la CI valider et publier
