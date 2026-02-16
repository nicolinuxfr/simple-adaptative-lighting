# Simple Adaptive Lighting

Custom integration Home Assistant (HACS) pour exposer un controleur d'eclairage adaptatif avec:

- un `switch` principal (activation/desactivation),
- un `sensor` de statut avec attributs (`brightness_pct`, `color_temp_kelvin`, `mode`, etc.),
- une configuration par entree (ex: une entree par piece).

## Installation avec HACS

1. Ajouter le depot comme *Custom repository* (type: `Integration`):
   - `nicolinuxfr/simple-adaptative-lightning`
2. Installer l'integration depuis HACS.
3. Redemarrer Home Assistant.
4. Ajouter l'integration via **Settings > Devices & Services**.

## Structure attendue HACS

- `hacs.json`
- `custom_components/simple_adaptive_lighting/manifest.json`
- `custom_components/simple_adaptive_lighting/*`
