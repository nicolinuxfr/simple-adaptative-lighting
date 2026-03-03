# Home Assistant Blueprint: Simple Adaptive Lighting

English version: [`README.md`](README.md) — Version française : [`README.fr.md`](README.fr.md)


## Blueprint verwenden

Sie können dieses Blueprint auf Ihrer Home Assistant-Instanz über diesen direkten Link importieren:

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsimple-adaptative-lightning%2Fgh-pages%2Fde%2Fadaptive_lighting.yaml)

Link zum Einfügen in HA: https://raw.githubusercontent.com/nicolinuxfr/simple-adaptative-lightning/gh-pages/de/adaptive_lighting.yaml

## Struktur

- `template.yaml`: Quell-Blueprint mit `[[...]]`-Platzhaltern
- `VERSION`: einzelne Blueprint-Version (in Beschreibung und `blueprint_revision` eingefügt)
- `languages/en.json`: Referenzwörterbuch (erforderlich, vollständig)
- `languages/<lang>.json`: Übersetzungen pro Sprache (automatischer Fallback auf `en`)
- `scripts/generate_blueprints.py`: Generierung + Validierung
- `dist/<lang>/adaptive_lighting.yaml`: generierte Blueprints

## Validierungsregeln

- Alle Template-Schlüssel müssen in `languages/en.json` vorhanden sein.
- Andere Sprachen können Schlüssel weglassen (Fallback auf `en`).
- Unbekannte Schlüssel in einem Wörterbuch lassen den Build fehlschlagen (Tippfehler-Schutz).

## Lokale Generierung

```bash
python3 scripts/generate_blueprints.py
```

- Generiert `dist/en/adaptive_lighting.yaml`, `dist/fr/adaptive_lighting.yaml`, `dist/de/adaptive_lighting.yaml`, usw.
- Fügt `[[blueprint.version]]` aus `VERSION` ein.
- Die Versionszeile wird über `blueprint.version.line` in jeder `languages/<lang>.json` übersetzt,
  mit einem `{version}`-Platzhalter (Beispiel: `Version: {version}`).

## GitHub Actions CI/CD

Workflow: `.github/workflows/blueprint-i18n.yml`

- Bei Pull Requests und Pushes: validiert Template + Wörterbücher.
- Bei Push auf `main`: regeneriert und veröffentlicht `dist/` auf `gh-pages`.

## Stabile öffentliche URLs für Home Assistant

Verwenden Sie `raw`-URLs aus dem `gh-pages`-Branch:

- Englisch:
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/en/adaptive_lighting.yaml`
- Französisch:
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/fr/adaptive_lighting.yaml`
- Deutsch:
  - `https://raw.githubusercontent.com/<owner>/<repo>/gh-pages/de/adaptive_lighting.yaml`

Diese URLs bleiben stabil, solange der `gh-pages`-Branch und die Pfade beibehalten werden.

## Eine neue Sprache hinzufügen

1. `languages/<lang>.json` erstellen
2. Übersetzte Schlüssel hinzufügen (teilweise erlaubt)
3. CI validieren und veröffentlichen lassen
