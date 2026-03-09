# Éclairage adaptatif simplifié

Ce *blueprint* pour Home Assistant s’inspire de l’[intégration Adaptive Lighting](https://github.com/basnijholt/adaptive-lighting) et permet d’ajuster des éclairages connectés automatiquement tout au long de la journée et même la nuit. Par rapport à l’intégration, il se veut beaucoup plus simple et offre nettement moins d’options. 

## Utiliser le blueprint

Vous pouvez ajouter ce *blueprint* à votre instance Home Assistant en utilisant ce lien direct :

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsimple-adaptive-lighting-blueprint%2Fgh-pages%2Ffr%2Fadaptive_lighting.yaml)

À défaut, vous pouvez copier ce lien pour le coller dans Home Assistant lors de l’ajout d’un blueprint :

	https://raw.githubusercontent.com/nicolinuxfr/simple-adaptive-lighting-blueprint/gh-pages/fr/adaptive_lighting.yaml

## Configuration

L’automatisation créée à partir du blueprint ne nécessite qu’un seul paramètre : une ou plusieurs lumières. Vous pouvez saisir plusieurs entités différentes ou un groupe Home Assistant. Les autres paramètres peuvent être laissés dans la configuration par défaut ou ajustés selon vos besoins. 

Voici la liste des options et quelques explications si nécessaire : 

- **Paramètres principaux** : choix de la luminosité minimale et maximale, ainsi que de la température de blanc minimale et maximale pour les éclairages. 
- **Contrôle par entité** : en sélectionnant une entité booléenne (de type `input_boolean` ou `binary_sensor`), on peut ajouter un contrôle sur l’automatisation sans la désactiver. L’entité doit être active pour que l’automatisation ajuste les lumières et quand elle est désactivée, les lumières restent sur le dernière réglage automatique.
  - Si vous activez le contrôle par entité, une autre option permet de désactiver automatiquement cette entité dès lors qu'au moins une lumière surveillée affiche de la couleur, y compris une lumière appartenant à un groupe Home Assistant sélectionné. L'automatisation ne fonctionnant qu'avec du blanc, c'est un signe que vous voulez prendre le main et désactiver les adaptations automatiques. C'est à vous de réactiver par la suite l'entité de contrôle, soit à la main, soit dans une autre automatisation.
- **Météo** : en sélectionnant une entité de type météo (*weather*), le comportement de l’automatisation est modifiée en fonction des conditions météorologiques. L’idée est de faire légèrement varier les paramètres pour avoir un éclairage plus faible et plus chaud quand les conditions climatiques sont mauvaises.
- **Mode nuit** : en sélectionnant une entité booléenne (de type `input_boolean` ou `binary_sensor`), on peut prévoir un éclairage fixe spécifique pour la nuit. Lorsque l’entité est active, les ajustements automatiques sont désactivés et les réglages de luminosité et température de couleur sont utilisés à la place. Cela permet d’avoir des réglages de jour suffisamment lumineux pour être confortables, tout en gardant un éclairage de nuit bien plus faible. 

Pour les trois options (contrôle par entité, météo et mode nuit), ne pas sélectionner d’entité revient à désactiver entièrement la fonctionnalité.

## Fonctionnement

L’automatisation s’active dès lors que les lumières sélectionnées s’allument. À partir de là, elle se déclenche toutes les cinq minutes pour ajuster la luminosité et la température du blanc en fonction des paramètres définis, de l’heure et de la courbe calculée automatiquement. Chaque transition est étalée sur dix secondes pour éviter les changements visibles. Pour limiter les problèmes avec certains éclairages, l’automatisation adopte une stratégie en deux temps et alterne entre luminosité et température de blanc à chaque mise à jour. 

Si une entité de contrôle est utilisée, l’adaptation est automatiquement stoppée dès que l’entité est désactivée et elle reprend si elle est réactivée. Le cas échéant, il n’y a pas de délai, les bonnes valeurs sont immédiatement envoyées, avec une progression douce sur 10 secondes. En option, l'entité de contrôle peut être désactivée automatiquement dès lors qu'une lumière surveillée affiche des couleurs, y compris si cette lumière fait partie d'un groupe Home Assistant. 

Si l’adaptation avec la météo est activée, la courbe est légèrement ajustée en fonction des conditions climatiques actuelles. Cette information n’est mise à jour qu’à l’allumage initial des éclairages par souci d’économie des ressources. 

Plusieurs stratégies sont en place pour ajuster légèrement le comportement de l’automatisation selon les situations. Par exemple, la courbe est différente si un seul éclairage est configuré par rapport à une automatisation qui contrôle plusieurs éclairages. 

## Limites

Ce blueprint ne gère volontairement pas certaines fonctionnalités : 

- Pas de gestion des couleurs, uniquement la température du blanc ;
- Pas de réglage de la courbe, les paramètres retenus sont ceux qui conviennent à mes besoins ;
- Pas d’ajustements possibles sur les heures de début et fin, seules les heures de lever et coucher du soleil à la position de votre domicile sont utilisées ;
- Pas de contrôle manuel des éclairages en cas de changement individuel, l’automatisation se déclenchera toujours toutes les cinq minutes et écrasera les changements ;
- Certainement bien d’autres encore.

## Mise en garde

Je n’ai pas directement codé ce *blueprint* moi-même, j’ai utilisé des outils comme Codex et Claude Code pour le créer. Il est ainsi proposé sans garantie, si ce n’est qu’il fonctionne parfaitement chez moi. Je l’ai testé avec de multiples configurations et de nombreux éclairages et je n’ai noté aucun problème. 

Les traductions sont aussi générées automatiquement par ces outils, j’ai écrit tous les textes en français.

## Contributions

Toutes les contributions sont bienvenues, pour corriger des bugs ou ajouter des fonctionnalités. Néanmoins, je tiens à conserver une configuration aussi simple que possible, mon idée n’est pas de reproduire l’intégration Adaptive Lighting. 
