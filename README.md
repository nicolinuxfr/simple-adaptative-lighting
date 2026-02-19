# Simple Adaptive Lighting Blueprint (i18n)

Ce depot genere automatiquement un blueprint Home Assistant en plusieurs langues a partir d'un template unique.

## Structure

- `template.yaml` : blueprint source avec placeholders `[[...]]`
- `languages/en.json` : dictionnaire de reference (obligatoire, complet)
- `languages/<lang>.json` : traductions par langue (fallback auto vers `en`)
- `scripts/generate_blueprints.py` : generation + validation
- `dist/<lang>/adaptive_lighting.yaml` : blueprints generes

## Regles de validation

- Toutes les cles du template doivent exister dans `languages/en.json`.
- Les autres langues peuvent omettre des cles: fallback automatique vers `en`.
- Les cles inconnues dans un dictionnaire provoquent un echec (anti-typo).

## Generation locale

```bash
python3 scripts/generate_blueprints.py
```

- Genere `dist/en/adaptive_lighting.yaml`, `dist/fr/adaptive_lighting.yaml`, etc.

## CI/CD GitHub Actions

Workflow: `.github/workflows/blueprint-i18n.yml`

- Sur PR/push: valide les dictionnaires + template et verifie que `adaptive_lighting.yaml` est a jour.
- Sur push `main`: regenere puis publie `dist/` sur la branche `gh-pages`.

## URLs publiques stables pour Home Assistant

Utilise les URLs `raw` de la branche `gh-pages`:

- Anglais:
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/en/adaptive_lighting.yaml`
- Francais:
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/fr/adaptive_lighting.yaml`

Ces URLs restent stables tant que tu conserves la branche `gh-pages` et les chemins.

## Ajouter une langue

1. Creer `languages/<lang>.json`
2. Ajouter uniquement les cles traduites (ou toutes les cles si tu preferes)
3. Laisser la CI valider et publier
