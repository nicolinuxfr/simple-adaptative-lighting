# Simple Adaptive Lighting (Skeleton)

Ce dossier contient un squelette d'integration Home Assistant installable via HACS.

## Objectif
- Exposer une entite `switch` (activation/desactivation)
- Exposer une entite `sensor` avec des attributs type adaptative lighting
- Ne pas modifier le blueprint existant

## Structure
- `custom_components/simple_adaptive_lighting/` : code integration
- `hacs.json` : metadata HACS

## Installation (manuelle)
1. Copier `custom_components/simple_adaptive_lighting` vers ton dossier HA `config/custom_components/`
2. Redemarrer Home Assistant
3. Ajouter l'integration via l'UI
